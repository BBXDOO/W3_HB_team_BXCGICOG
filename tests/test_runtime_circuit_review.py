"""Regression checks found during review of the merged runtime circuit."""
from copy import deepcopy
import json
from unittest.mock import patch

import pytest

from core.modules_loader.router import execution_plan
from core.runtime import engine_v2 as engine
from workflows import orchestration as orc
from workflows.runtime_circuit import WorkflowRuntime


def task():
    return orc.new_task('W3-ORC-20261021-300', 'REQUEST', 'NORMAL',
                        {'module': 'BBX19', 'tier': 0}, {})


def result(job, request, **kw):
    module = execution_plan(job)['run_with']
    return {'status': 'COMPLETED', 'module': module, 'trace_id': 'test-trace',
            'result_validation': {'status': 'valid'},
            'agent_result': {'status': 'COMPLETED', 'module': module,
                             'mutated': False, 'review': False}}


def test_failed_review_flag_must_block_not_wait_for_approval(tmp_path):
    def failed(*a, **kw):
        r = result(*a, **kw)
        r.update(status='FAILED')
        r['agent_result'].update(status='FAILED', review=True)
        return r
    circuit = WorkflowRuntime(tmp_path, runner=failed, verifier=lambda *a: {'passed': True})
    t = circuit.run(task(), [{'task': 'design'}])
    assert t['status'] == 'BLOCKED'


def test_target_is_work_subject_not_executor(tmp_path):
    seen = []
    def run(job, request, **kw):
        seen.append(request)
        return result(job, request)
    circuit = WorkflowRuntime(tmp_path, runner=run, verifier=lambda *a: {'passed': True})
    circuit.run(task(), [{'task': 'verify', 'request': {'target': 'W3API'}}])
    assert seen[0]['target'] == 'W3API'


def test_malformed_request_rejected_before_lifecycle_or_side_effects(tmp_path):
    t = task()
    original = deepcopy(t)
    circuit = WorkflowRuntime(tmp_path, runner=result, verifier=lambda *a: {'passed': True})
    with pytest.raises(ValueError):
        circuit.run(t, [{'task': 'design', 'request': None}])
    assert t == original and not list(tmp_path.iterdir())


def test_review_must_use_original_stage_parameters(tmp_path):
    def reviewed(*a, **kw):
        r = result(*a, **kw); r['agent_result']['review'] = True; return r
    circuit = WorkflowRuntime(tmp_path, runner=reviewed, verifier=lambda *a: {'passed': True})
    stage = {'task': 'design', 'request': {'intent': 'original'}}
    t = circuit.run(task(), [stage])
    with pytest.raises(ValueError):
        circuit.review_stage(t, {'task': 'design', 'request': {'intent': 'changed'}},
                             human='test-human', evidence='test:review')
    assert t['status'] == 'WAITING_HUMAN'


def test_runtime_memory_preserves_effective_status(tmp_path):
    with patch.object(engine, 'search_memory', return_value=[]), \
         patch.object(engine, 'add_memory') as memory, \
         patch.object(engine, 'dispatch', return_value={'status': 'COMPLETED'}):
        r = engine.run('route')
    assert r['status'] == 'REVIEW_REQUIRED'
    saved = json.loads(memory.call_args.kwargs['content'])
    assert saved['status'] == 'REVIEW_REQUIRED'
    assert saved['reported_status'] == 'COMPLETED'


def test_reload_and_continue_after_review_does_not_replay_completed_stage(tmp_path):
    calls = []
    def reviewed(job, request, **kw):
        calls.append((job, deepcopy(request)))
        r = result(job, request)
        if job == 'design':
            r['agent_result']['review'] = True
        return r
    stages = [{'task': 'design', 'request': {'target': 'W3API'}}, {'task': 'verify'}]
    circuit = WorkflowRuntime(tmp_path, runner=reviewed, verifier=lambda *a: {'passed': True})
    t = circuit.run(task(), stages)
    assert t['status'] == 'WAITING_HUMAN'
    snapshot = tmp_path/'tasks'/f"{t['task_id']}.json"
    t = json.loads(snapshot.read_text())
    circuit = WorkflowRuntime(tmp_path, runner=reviewed, verifier=lambda *a: {'passed': True})
    circuit.review_stage(t, stages[0], human='test-human', evidence='test:review-design')
    circuit.continue_work(t)
    assert [job for job, _ in calls] == ['design', 'verify']
    assert calls[1][1]['payload']['module'] == 'ChatGPT'
    assert t['runtime_circuit']['index'] == 1 and t['status'] == 'WAITING_HUMAN'
    assert t['human_approval'] is None
    circuit.review_stage(t, stages[1], human='test-human', evidence='test:review-verify')
    circuit.continue_work(t)
    assert t['status'] == 'COMPLETED'
    circuit.continue_work(t)
    assert len(calls) == 2


def test_support_retry_then_remaining_stages_retains_original_request(tmp_path):
    fixed = False
    calls = []
    def runner(job, request, **kw):
        calls.append((job, deepcopy(request)))
        r = result(job, request)
        if job == 'design' and not fixed:
            r.update(status='FAILED')
        return r
    c = WorkflowRuntime(tmp_path, runner=runner, verifier=lambda *a: {'passed': True})
    t = c.run(task(), [{'task': 'design', 'request': {'payload': {'id': 7}}}, {'task': 'verify'}])
    assert t['status'] == 'BLOCKED'
    def support(context):
        context['destination']['module'] = 'tampered'
        return {'resolved': True, 'evidence': 'test:fixed'}
    c.assist(t, kind='TOOL', name='repair', handler=support)
    assert t['status'] == 'RETURNED' and t['destination']['module'] == 'ChatGPT'
    fixed = True
    c.continue_work(t)
    assert [job for job, _ in calls] == ['design', 'design', 'verify']
    assert calls[0][1] == calls[1][1]
    assert t['status'] == 'COMPLETED'


@pytest.mark.parametrize('bad_result', [None, 'text', {'status': 'COMPLETED', 'agent_result': []},
                                        {'status': 'COMPLETED', 'non_json': object()}])
def test_malformed_runner_results_become_blockers(tmp_path, bad_result):
    c = WorkflowRuntime(tmp_path, runner=lambda *a, **kw: bad_result,
                        verifier=lambda *a: {'passed': True})
    t = c.run(task(), [{'task': 'design'}])
    assert t['status'] == 'BLOCKED'
    for path in tmp_path.rglob('*.json'):
        json.loads(path.read_text())


def test_interrupted_work_is_not_replayed(tmp_path):
    c = WorkflowRuntime(tmp_path, runner=result, verifier=lambda *a: {'passed': True})
    t = c.run(task(), [{'task': 'design'}])
    t['status'] = 'IN_PROGRESS'
    with pytest.raises(ValueError, match='refusing automatic replay'):
        c.continue_work(t)


def test_revised_request_queues_same_owner_with_audit(tmp_path):
    def runner(job, request, **kw):
        r = result(job, request)
        if not request.get('payload', {}).get('fixed'):
            r['status'] = 'REVIEW_REQUIRED'
        return r
    c = WorkflowRuntime(tmp_path, runner=runner, verifier=lambda *a: {'passed': True})
    t = c.run(task(), [{'task': 'verify'}])
    with pytest.raises(ValueError, match='corrected before approval'):
        c.review_stage(t, {'task': 'verify'}, human='test-human', evidence='test:approve')
    c.revise_stage(t, request={'payload': {'fixed': True}}, actor='test-host', evidence='test:context')
    assert t['status'] == 'QUEUED' and t['human_approval'] is None
    c.continue_work(t)
    assert t['status'] == 'WAITING_HUMAN'
    stage = {'task': 'verify', 'request': {'payload': {'fixed': True}}}
    c.review_stage(t, stage, human='test-human', evidence='test:corrected-result')
    c.continue_work(t)
    assert t['status'] == 'COMPLETED' and len(t['route']) == 2
    assert list(tmp_path.rglob('revision-*.json'))


def test_memory_failure_retains_executor_side_effect_evidence():
    executed = {'status': 'COMPLETED', 'module': 'ChatGPT', 'mutated': True,
                'artifacts': [{'path': 'test:created'}]}
    with patch.object(engine, 'search_memory', return_value=[]), \
         patch.object(engine, 'dispatch', return_value=executed), \
         patch.object(engine, 'add_memory', side_effect=OSError('disk')):
        r = engine.run('design')
    assert r['status'] == 'FAILED' and r['execution_status'] == 'COMPLETED'
    assert r['agent_result']['mutated'] is True and r['artifacts'] == executed['artifacts']


def test_cannot_close_before_remaining_explicit_stages(tmp_path):
    def reviewed(*a, **kw):
        r = result(*a, **kw); r['agent_result']['review'] = True; return r
    c = WorkflowRuntime(tmp_path, runner=reviewed, verifier=lambda *a: {'passed': True})
    t = c.run(task(), [{'task': 'design'}, {'task': 'verify'}])
    c.review_stage(t, {'task': 'design'}, human='test-human', evidence='test:review')
    with pytest.raises(ValueError, match='all runtime stages'):
        orc.advance(t, 'COMPLETED', actor='test-host', detail='premature')
    assert t['status'] == 'VERIFYING'


def test_snapshot_state_validation_rejects_out_of_range_cursor(tmp_path):
    c = WorkflowRuntime(tmp_path, runner=result, verifier=lambda *a: {'passed': True})
    t = c.run(task(), [{'task': 'verify'}])
    t['runtime_circuit']['index'] = 99
    with pytest.raises(ValueError, match='stage index'):
        orc.save(t, tmp_path/'bad')


def test_real_gemini_pipeline_finishes_with_subject_and_snapshot(tmp_path):
    def verify(stage, outcome):
        return {'passed': outcome['agent_result'].get('decision') == 'VERIFIED'}
    with patch.object(engine, 'search_memory', return_value=[]), patch.object(engine, 'add_memory'):
        t = WorkflowRuntime(tmp_path, verifier=verify).run(task(), [
            {'task': 'verify', 'request': {'target': 'W3API',
              'payload': {'checks': [True], 'evidence': ['test:fixture']}}},
            {'task': 'audit', 'request': {'target': 'LRC2',
              'payload': {'checks': [True], 'evidence': ['test:audit']}}},
        ])
    assert t['status'] == 'COMPLETED' and t['runtime_circuit']['index'] == 1
    paths = [item['ref'] for item in t['evidence'] if item['actor'] == 'runtime-result']
    assert 'W3API' in json.loads(__import__('pathlib').Path(paths[0]).read_text())['output']
    assert 'LRC2' in json.loads(__import__('pathlib').Path(paths[1]).read_text())['output']


def test_first_stage_receives_task_payload_without_mutating_source(tmp_path):
    t = task()
    t['payload'] = {'chain_id': 'chain-test', 'content': ['log-1']}
    seen = []
    def runner(job, request, **kw):
        seen.append(deepcopy(request))
        request['payload']['content'].append('adapter-change')
        return result(job, request)
    c = WorkflowRuntime(tmp_path, runner=runner, verifier=lambda *a: {'passed': True})
    c.run(t, [{'task': 'verify'}])
    assert seen[0]['payload']['chain_id'] == 'chain-test'
    assert t['payload']['content'] == ['log-1']
