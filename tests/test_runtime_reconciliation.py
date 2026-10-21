"""Post-execution evidence and provenance regressions from PR #295 review."""
from copy import deepcopy
from unittest.mock import patch

import pytest

from core.modules_loader.router import execution_plan
from workflows import orchestration as orc
from workflows.runtime_circuit import WorkflowRuntime


def task():
    return orc.new_task('W3-ORC-20261021-400', 'REQUEST', 'NORMAL',
                        {'module': 'BBX19', 'tier': 0}, {})


def result(job, request, **kw):
    module = execution_plan(job)['run_with']
    return {'status': 'COMPLETED', 'module': module, 'trace_id': 'test-trace',
            'result_validation': {'status': 'valid'},
            'agent_result': {'status': 'COMPLETED', 'module': module,
                             'mutated': False, 'review': False}}


def test_source_cannot_override_recorded_origin(tmp_path):
    seen = []
    def runner(job, request, **kw):
        seen.append(request)
        return result(job, request)
    t = WorkflowRuntime(tmp_path, runner=runner, verifier=lambda *a: {'passed': True}).run(
        task(), [{'task': 'verify', 'request': {'source': 'forged', 'target': 'W3API'}}])
    assert seen[0]['source'] == t['origin']['module']
    assert seen[0]['target'] == 'W3API'


@pytest.mark.parametrize('effective', [{}, {'task': 'verify', 'module': 'Gemini', 'request': None},
                                        {'task': 'design', 'module': 'ChatGPT', 'request': {}}])
def test_bad_effective_stage_rejected_before_resume(tmp_path, effective):
    c = WorkflowRuntime(tmp_path, runner=result, verifier=lambda *a: {'passed': True})
    t = c.run(task(), [{'task': 'verify'}])
    t['status'] = 'QUEUED'
    t['runtime_circuit']['effective_stage'] = effective
    original = deepcopy(t)
    with pytest.raises(ValueError):
        c.continue_work(t)
    assert t == original


def test_bad_runner_diagnostic_preserves_mutation_and_artifacts(tmp_path):
    def runner(job, request, **kw):
        r = result(job, request)
        r['agent_result'].update(mutated=True, artifacts=[{'path': 'created.txt'}])
        r['artifacts'] = [{'path': 'created.txt'}]
        r['diagnostic'] = object()
        return r
    t = WorkflowRuntime(tmp_path, runner=runner, verifier=lambda *a: {'passed': True}).run(
        task(), [{'task': 'design'}])
    assert t['status'] == 'BLOCKED' and t['mutated'] is True
    assert t['runtime_circuit'].get('reconciliation_required') is True
    import json
    from pathlib import Path
    saved = json.loads(Path(t['runtime_circuit']['result_ref']).read_text())
    assert saved['artifacts'] == [{'path': 'created.txt'}]


def test_support_persistence_failure_is_not_silently_retriable(tmp_path):
    c = WorkflowRuntime(tmp_path, runner=result, verifier=lambda *a: {'passed': False})
    t = c.run(task(), [{'task': 'verify'}])
    side_effects = []
    def handler(context):
        side_effects.append('done')
        return {'resolved': True, 'evidence': 'test:done', 'mutated': True}
    real_evidence = c._evidence
    def evidence(task, kind, value):
        if kind == 'support':
            raise OSError('disk failed after handler')
        return real_evidence(task, kind, value)
    with patch.object(c, '_evidence', side_effect=evidence):
        with pytest.raises(RuntimeError) as error:
            c.assist(t, kind='TOOL', name='repair', handler=handler)
    assert error.value.result['resolved'] is True
    assert t['runtime_circuit']['reconciliation_required'] is True
    with pytest.raises(RuntimeError):
        c.assist(t, kind='TOOL', name='repair', handler=handler)
    assert side_effects == ['done']


def test_recover_support_result_without_replaying_adapter(tmp_path):
    c = WorkflowRuntime(tmp_path, runner=result, verifier=lambda *a: {'passed': False})
    t = c.run(task(), [{'task': 'verify'}])
    effects = []
    def handler(ctx):
        effects.append('executed')
        return {'resolved': True, 'evidence': 'test:already-done', 'extra': object()}
    with pytest.raises(RuntimeError) as caught:
        c.assist(t, kind='TOOL', name='repair', handler=handler)
    c.reconcile(t, actor='test-host', evidence='test:confirmed-action', support_result=caught.value.result)
    assert t['status'] == 'RETURNED' and len(t['support']) == 1
    assert t['runtime_circuit']['reconciliation_required'] is False
    assert effects == ['executed']


def test_support_snapshot_failure_retains_attempt_for_reconciliation(tmp_path):
    c = WorkflowRuntime(tmp_path, runner=result, verifier=lambda *a: {'passed': False})
    t = c.run(task(), [{'task': 'verify'}])
    real_save = c._save
    def broken_save(task):
        if task['status'] == 'RETURNED':
            raise OSError('final snapshot failed')
        return real_save(task)
    with patch.object(c, '_save', side_effect=broken_save):
        with pytest.raises(RuntimeError) as caught:
            c.assist(t, kind='TOOL', name='repair', handler=lambda ctx: {'resolved': True, 'evidence': 'test:done'})
    assert t['runtime_circuit']['pending_support']['name'] == 'repair'
    c.reconcile(t, actor='test-host', evidence='test:confirmed', support_result=caught.value.result)
    assert len(t['support']) == 1 and t['status'] == 'RETURNED'


def test_runner_evidence_write_failure_exposes_result_and_blocks_replay(tmp_path):
    calls = []
    def runner(job, request, **kw):
        calls.append(job)
        r = result(job, request); r['agent_result']['mutated'] = True
        r['artifacts'] = [{'path': 'test:created'}]
        return r
    c = WorkflowRuntime(tmp_path, runner=runner, verifier=lambda *a: {'passed': True})
    t = task()
    real = c._evidence
    def broken(task, kind, value):
        if kind == 'result':
            raise OSError('disk')
        return real(task, kind, value)
    with patch.object(c, '_evidence', side_effect=broken):
        with pytest.raises(RuntimeError) as caught:
            c.run(t, [{'task': 'design'}])
    assert caught.value.result['artifacts'] == [{'path': 'test:created'}]
    assert t['mutated'] is True
    with pytest.raises(RuntimeError):
        c.continue_work(t)
    assert calls == ['design']


def test_reloaded_support_uncertainty_refuses_another_invocation(tmp_path):
    import json
    c = WorkflowRuntime(tmp_path, runner=result, verifier=lambda *a: {'passed': False})
    t = c.run(task(), [{'task': 'verify'}])
    real = c._evidence
    def broken(task, kind, value):
        if kind == 'support':
            raise OSError('disk')
        return real(task, kind, value)
    with patch.object(c, '_evidence', side_effect=broken):
        with pytest.raises(RuntimeError):
            c.assist(t, kind='TOOL', name='repair', handler=lambda ctx: {'resolved': True, 'evidence': 'test:done'})
    t = json.loads((tmp_path/'tasks'/f"{t['task_id']}.json").read_text())
    with pytest.raises(RuntimeError):
        c.assist(t, kind='TOOL', name='repair', handler=lambda ctx: pytest.fail('must not replay'))


def test_task_schema_validates_effective_stage_and_reconciliation_metadata(tmp_path):
    import json
    from pathlib import Path
    from jsonschema import Draft202012Validator
    schema = json.loads((Path(__file__).resolve().parents[1]/'workflows/orchestration_task.schema.json').read_text())
    validator = Draft202012Validator(schema)
    c = WorkflowRuntime(tmp_path, runner=result, verifier=lambda *a: {'passed': False})
    t = c.run(task(), [{'task': 'verify'}])
    with pytest.raises(RuntimeError):
        c.assist(t, kind='TOOL', name='repair', handler=lambda ctx: {'resolved': True, 'evidence': 'test:done', 'diagnostic': object()})
    validator.validate(t)
    invalid = deepcopy(t)
    invalid['runtime_circuit']['effective_stage'] = {}
    assert list(validator.iter_errors(invalid))


def test_recovered_unresolved_support_is_not_appended_twice(tmp_path):
    c = WorkflowRuntime(tmp_path, runner=result, verifier=lambda *a: {'passed': False})
    t = c.run(task(), [{'task': 'verify'}])
    real_save = c._save
    def broken(task):
        if task['support']:
            raise OSError('snapshot after support')
        return real_save(task)
    with patch.object(c, '_save', side_effect=broken):
        with pytest.raises(RuntimeError) as caught:
            c.assist(t, kind='TOOL', name='repair', handler=lambda ctx: {'resolved': False, 'evidence': 'test:partial'})
    c.reconcile(t, actor='test-host', evidence='test:verified-partial', support_result=caught.value.result)
    assert len(t['support']) == 1 and t['status'] == 'BLOCKED'


def test_reconcile_unknown_runner_effects_does_not_execute_retry(tmp_path):
    calls = []
    def runner(job, request, **kw):
        calls.append(job)
        r = result(job, request); r['diagnostic'] = object(); return r
    c = WorkflowRuntime(tmp_path, runner=runner, verifier=lambda *a: {'passed': True})
    t = c.run(task(), [{'task': 'design'}])
    with pytest.raises(RuntimeError):
        c.revise_stage(t, request={}, actor='test-host', evidence='test:retry')
    c.reconcile(t, actor='test-host', evidence='test:checked-files')
    assert t['status'] == 'BLOCKED' and calls == ['design']


def test_record_result_failure_propagates_from_orchestration(tmp_path):
    from workflows import orchestration as orc
    t = task()
    t.update(status='BLOCKED', blocker={'reason': 'test'})
    response = {'resolved': True, 'evidence': 'test:done'}
    def fail(result):
        raise OSError('post-handler persistence')
    with pytest.raises(OSError):
        orc.assist(t, kind='TOOL', name='repair', actor='test-host',
                   handler=lambda context: response, record_result=fail)
    assert t['status'] == 'ASSISTING' and not t['support']


def test_runner_snapshot_failure_exposes_original_result(tmp_path):
    c = WorkflowRuntime(tmp_path, runner=result, verifier=lambda *a: {'passed': True})
    t = task()
    real = c._save
    def broken(task):
        if task.get('runtime_circuit', {}).get('result_ref'):
            raise OSError('snapshot after result')
        return real(task)
    with patch.object(c, '_save', side_effect=broken):
        with pytest.raises(RuntimeError) as caught:
            c.run(t, [{'task': 'verify'}])
    assert caught.value.result['status'] == 'COMPLETED'
    assert t['runtime_circuit']['reconciliation_required'] is True
