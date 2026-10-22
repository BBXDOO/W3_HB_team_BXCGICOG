from copy import deepcopy
import hashlib
import json
from pathlib import Path

import pytest

from core.memory import memory_bus
from core.runtime import engine_v2
from tools import request_cycle as rc
from tools.runtime_circuit_intake import make_runtime, parse_spec, run_request, task_id
from tests.test_log_analysis_capability import logs


def configure(monkeypatch, root):
    for name, suffix in {'ROOT': '', 'REQUESTS': 'requests', 'RESULTS': 'requests/results',
                         'EVENTS': 'repo_events', 'CHECKIN_DIR': 'logs/check-in',
                         'REQUEST_LOG_DIR': 'logs/request_cycle', 'REQUEST_LOCK_DIR': 'locks'}.items():
        monkeypatch.setattr(rc, name, root/suffix)
    monkeypatch.setattr(memory_bus, 'MEMORY_FILE', root/'test-runtime-memory.json')


def request(root, *, review=True, stages=None):
    source = root/'logs.json'
    source.write_text(json.dumps({'records': logs()}))
    stages = stages or [
        {'task': 'log_analysis', 'module': 'LRC2', 'request': {'payload': {'source_file': 'logs.json', 'min_samples': 3}}},
        {'task': 'verify', 'module': 'Gemini'},
    ]
    path = root/'requests/RQ-REAL-ANALYSIS.md'
    path.parent.mkdir(parents=True, exist_ok=True)
    text = ('---\nrequest_id: RQ-REAL-ANALYSIS\nrequest_type: runtime_circuit\ntask_keyword: log_analysis\n'
            'target_module: LRC2\nrequester: BBX19\nfinal_signoff_required: '+str(review).lower()+'\n---\n'
            '# Analyze recorded failures, risk stacks and success outcomes\n\n```w3-circuit\n'
            +json.dumps({'stages': stages})+'\n```\n')
    path.write_text(text)
    return path


def test_real_root_request_runs_lrc2_gemini_and_human_gate(monkeypatch, tmp_path):
    configure(monkeypatch, tmp_path)
    path = request(tmp_path)
    envelope = rc.process(path)
    outcome = envelope['runtime_result']
    assert outcome['status'] == 'WAITING_HUMAN' and not envelope['closed']
    assert [r['module'] for r in outcome['stage_results']] == ['LRC2', 'Gemini']
    assert outcome['stage_results'][1]['agent_result']['decision'] == 'VERIFIED'
    assert all(c['passed'] for c in outcome['stage_results'][1]['agent_result']['details']['checks'])
    report = json.loads((tmp_path/outcome['artifacts'][0]['path']).read_text())
    assert report['groups'][0]['risk_window']['maximum_adverse_streak'] == 3
    assert report['groups'][0]['success_estimate']['value'] == .5
    assert (tmp_path/envelope['request_log']).exists()
    assert rc.process(path)['status'] == 'SKIPPED'
    snapshot = tmp_path/outcome['orchestration_evidence']
    task = json.loads(snapshot.read_text())
    circuit = make_runtime(tmp_path)
    stage = task['runtime_circuit']['stages'][1]
    circuit.review_stage(task, stage, human='BBX19', evidence='test:actual-review')
    completed = rc.process(path)
    assert completed['runtime_result']['status'] == 'COMPLETED' and completed['closed']
    assert len(list((tmp_path/'modules/LRC2/reports/log_analysis').glob('*.json'))) == 1
    assert rc.process(path)['status'] == 'SKIPPED'


def test_live_memory_input_is_frozen_before_execution_mutates_memory(monkeypatch, tmp_path):
    configure(monkeypatch, tmp_path)
    path = request(tmp_path, review=False)
    data = json.loads((tmp_path/'logs.json').read_text())
    memory_bus.MEMORY_FILE.write_text(json.dumps({**data, 'runtime': {}}))
    text = path.read_text().replace('logs.json', 'test-runtime-memory.json')
    path.write_text(text)
    envelope = rc.process(path)
    assert envelope['runtime_result']['status'] == 'COMPLETED'
    report = json.loads((tmp_path/envelope['artifact_paths'][0]['path']).read_text())
    assert report['records_total'] == 7
    assert len(memory_bus.load_store()['records']) > 7
    assert report['original_source'] == 'test-runtime-memory.json'


def test_tampered_report_cannot_be_approved(monkeypatch, tmp_path):
    configure(monkeypatch, tmp_path)
    path = request(tmp_path)
    envelope = rc.process(path)
    outcome = envelope['runtime_result']
    artifact = tmp_path/outcome['artifacts'][0]['path']
    report = json.loads(artifact.read_text()); report['records_total'] = 999
    artifact.write_text(json.dumps(report))
    task = json.loads((tmp_path/outcome['orchestration_evidence']).read_text())
    with pytest.raises(ValueError, match='postcondition'):
        make_runtime(tmp_path).review_stage(task, task['runtime_circuit']['stages'][1], human='BBX19', evidence='test:review')


def test_unknown_semantic_verifier_does_not_accept_a_file_as_finished_work(monkeypatch, tmp_path):
    configure(monkeypatch, tmp_path)
    stage = {'task': 'reason', 'module': 'Cast', 'request': {'payload': {'observations': ['a fact']}}}
    path = request(tmp_path, review=False, stages=[stage])
    path.write_text(path.read_text().replace('target_module: LRC2', 'target_module: Cast').replace('task_keyword: log_analysis', 'task_keyword: reason'))
    envelope = rc.process(path)
    assert envelope['runtime_result']['status'] != 'COMPLETED'


def test_host_executor_receives_full_context_without_being_replaced_by_template(monkeypatch, tmp_path):
    configure(monkeypatch, tmp_path)
    path = request(tmp_path, review=False, stages=[{'task': 'design', 'module': 'ChatGPT',
                                                  'request': {'payload': {'values': [5, 8]}}}])
    parsed = rc.parse_request(path)
    seen = []
    def executor(task, plan, context):
        seen.append(deepcopy(context))
        value = sum(context['payload']['values'])
        artifact = tmp_path/'computed.txt'; artifact.write_text(str(value))
        return {'status': 'COMPLETED', 'module': 'ChatGPT', 'capability': 'context_calculation',
                'summary': 'Calculated from supplied values', 'review': False, 'mutated': True,
                'artifacts': [{'path': 'computed.txt', 'sha256': hashlib.sha256(artifact.read_bytes()).hexdigest()}]}
    def verify(stage, result):
        return {'passed': (tmp_path/'computed.txt').read_text() == '13'}
    result = run_request(request=parsed, repo_root=tmp_path,
                         executors={'ChatGPT': executor}, verifiers={'design': verify})
    assert result['status'] == 'COMPLETED' and seen[0]['payload']['values'] == [5, 8]
    assert parsed['_request_text'] == seen[0]['request']['request_text']
    assert seen[0]['request']['_request_file'] == 'requests/RQ-REAL-ANALYSIS.md'
    assert not (tmp_path/'modules/ChatGPT/flows').exists()


def test_registered_executor_cannot_claim_another_modules_identity(monkeypatch, tmp_path):
    configure(monkeypatch, tmp_path)
    bad = lambda *a: {'status': 'COMPLETED', 'module': 'Gemini', 'summary': 'wrong actor'}
    outcome = engine_v2.run('design', executors={'ChatGPT': bad})
    assert outcome['status'] == 'REVIEW_REQUIRED'
    assert 'module' in outcome['result_validation']['invalid_fields']


def test_modified_request_id_content_does_not_silently_restart(monkeypatch, tmp_path):
    configure(monkeypatch, tmp_path)
    path = request(tmp_path)
    rc.process(path)
    path.write_text(path.read_text()+'\nChanged requirements\n')
    with pytest.raises(ValueError, match='changed'):
        run_request(request=rc.parse_request(path), repo_root=tmp_path)
    assert len(list((tmp_path/'modules/LRC2/reports/log_analysis').glob('*.json'))) == 1


def test_changed_request_does_not_replace_previous_result(monkeypatch, tmp_path):
    configure(monkeypatch, tmp_path)
    path = request(tmp_path)
    rc.process(path)
    result_path = tmp_path/'requests/results/RQ-REAL-ANALYSIS_RESULT.json'
    before = result_path.read_bytes()
    path.write_text(path.read_text()+'\nChanged work\n')
    with pytest.raises(ValueError, match='changed'):
        rc.process(path)
    assert result_path.read_bytes() == before


def test_concurrent_pending_scans_do_not_reexecute_or_duplicate_checkins(monkeypatch, tmp_path):
    from concurrent.futures import ThreadPoolExecutor
    configure(monkeypatch, tmp_path)
    path = request(tmp_path)
    with ThreadPoolExecutor(max_workers=2) as workers:
        outcomes = list(workers.map(rc.process, [path, path]))
    assert sum(o.get('status') == 'SKIPPED' for o in outcomes) == 1
    assert len(list((tmp_path/'modules/LRC2/reports/log_analysis').glob('*.json'))) == 1
    checkin = tmp_path/'logs/check-in/CID_@R000A1.md'
    assert checkin.read_text().count('• NO.') == 1


def test_final_review_policy_still_stops_on_module_review_request(monkeypatch, tmp_path):
    configure(monkeypatch, tmp_path)
    path = request(tmp_path, review=True, stages=[{'task': 'design', 'module': 'ChatGPT'}, {'task': 'verify'}])
    def executor(job, plan, context):
        return {'status': 'COMPLETED', 'module': 'ChatGPT', 'review': True,
                'summary': 'Needs domain review', 'mutated': False, 'artifacts': []}
    parsed = rc.parse_request(path)
    result = run_request(request=parsed, repo_root=tmp_path, executors={'ChatGPT': executor},
                         verifiers={'design': lambda *a: {'passed': True}})
    assert result['status'] == 'WAITING_HUMAN'
    assert len(result['stage_results']) == 1


def test_saved_request_can_be_reviewed_after_moving_repository(monkeypatch, tmp_path):
    import shutil
    original = tmp_path/'original'; original.mkdir()
    configure(monkeypatch, original)
    path = request(original)
    envelope = rc.process(path)
    snapshot = envelope['runtime_result']['orchestration_evidence']
    task = json.loads((original/snapshot).read_text())
    assert str(original) not in json.dumps(task)
    moved = tmp_path/'moved'
    shutil.copytree(original, moved)
    shutil.rmtree(original)
    configure(monkeypatch, moved)
    task = json.loads((moved/snapshot).read_text())
    stage = task['runtime_circuit']['stages'][1]
    make_runtime(moved).review_stage(task, stage, human='BBX19', evidence='test:review-after-move')
    envelope = rc.process(moved/'requests/RQ-REAL-ANALYSIS.md')
    assert envelope['runtime_result']['status'] == 'COMPLETED'


def test_preparation_failure_leaves_no_incomplete_task_and_retry_works(monkeypatch, tmp_path):
    from workflows.runtime_circuit import WorkflowRuntime
    configure(monkeypatch, tmp_path); path = request(tmp_path)
    original = WorkflowRuntime._prepare
    def fail(*args, **kwargs):
        raise OSError('interrupted before initialization')
    monkeypatch.setattr(WorkflowRuntime, '_prepare', fail)
    with pytest.raises(OSError):
        run_request(request=rc.parse_request(path), repo_root=tmp_path)
    snapshot = tmp_path/'repo_events/runtime_circuit/tasks'/f'{task_id("RQ-REAL-ANALYSIS")}.json'
    assert not snapshot.exists()
    monkeypatch.setattr(WorkflowRuntime, '_prepare', original)
    assert run_request(request=rc.parse_request(path), repo_root=tmp_path)['status'] == 'WAITING_HUMAN'


def test_old_intent_only_snapshot_resumes_without_deleting_it(monkeypatch, tmp_path):
    from workflows import orchestration as orc
    from workflows.human_callback import ensure_intent
    configure(monkeypatch, tmp_path); path = request(tmp_path)
    parsed = rc.parse_request(path); rid = parsed['request_id']
    task = orc.new_task(task_id(rid), 'REQUEST', 'NORMAL', {'module':'BBX19','tier':0},
        {'request_id':rid, 'source_request':parsed['_request_file'],
         'request_sha256':hashlib.sha256(parsed['_request_text'].encode()).hexdigest()}, source_id=rid, human_review_required=True)
    ensure_intent(make_runtime(tmp_path), task, parsed)
    original_intent = task['payload']['human_cycle']['intent']['intent_id']
    result = run_request(request=parsed, repo_root=tmp_path)
    assert result['status'] == 'WAITING_HUMAN' and result['intent_id'] == original_intent
    assert len(result['stage_results']) == 2
