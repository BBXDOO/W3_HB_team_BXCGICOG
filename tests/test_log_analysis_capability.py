from copy import deepcopy
import hashlib
import json
from pathlib import Path

import pytest

from core.runtime import engine_v2
from core.runtime.capabilities.log_analysis import analyze, canonical, execute


def logs():
    statuses = ['COMPLETED', 'FAILED', 'BLOCKED', 'FAILED', 'REVIEW_REQUIRED', 'COMPLETED', 'mystery']
    return [{'id': f'event-{i}', 'module': 'REDR', 'task': 'risk_router', 'status': status,
             'timestamp': f'2026-10-21T00:0{i}:00Z', 'error_code': 'NETWORK' if i in (1, 2, 3) else None}
            for i, status in enumerate(statuses)]


def test_analysis_uses_context_with_known_counts_and_error_patterns():
    records = logs()
    before = deepcopy(records)
    report = analyze(records, min_samples=3)
    group = report['groups'][0]
    assert report['records_total'] == 7
    assert report['categories'] == {'success': 2, 'failure': 2, 'blocked': 1, 'review': 1, 'unknown': 1}
    assert group['risk_window']['maximum_adverse_streak'] == 3
    assert group['risk_window']['advisory_score'] == 5.5
    assert group['success_estimate']['sample_count'] == 4
    assert group['success_estimate']['value'] == .5
    lo, hi = group['success_estimate']['wilson_95_interval']
    assert lo == pytest.approx(.150038989, abs=1e-6)
    assert hi == pytest.approx(.849961011, abs=1e-6)
    assert report['repeated_error_patterns'][0]['record_refs'] == ['event-1', 'event-2', 'event-3']
    assert report['unknown_record_refs'] == ['event-6'] and records == before


def test_small_history_does_not_fabricate_a_prediction():
    report = analyze(logs(), min_samples=5)
    assert report['groups'][0]['observed_success_rate'] == .5
    assert report['groups'][0]['success_estimate']['value'] is None
    changed = logs()[:1]
    changed[0].update(module='PSP2', task='route')
    other = analyze(changed)
    assert other['groups'][0]['module'] == 'PSP2'
    assert other['groups'][0]['records'] == 1 and other['repeated_error_patterns'] == []


def test_memory_bus_json_content_and_unknown_outcomes_are_preserved():
    records = [{'id': 'memory-1', 'source': 'Codex', 'topic': 'ci_repair',
                'content': json.dumps({'status': 'FAILED', 'error': 'missing tool'})},
               {'id': 'memory-2', 'source': 'Codex', 'topic': 'ci_repair', 'content': 'not a result'}]
    report = analyze(records)
    assert report['categories'] == {'failure': 1, 'unknown': 1}
    assert report['groups'][0]['risk_window']['order'] == 'input_order'
    assert report['groups'][0]['success_estimate']['sample_count'] == 1


def test_real_executor_writes_hash_verifiable_source_linked_report(tmp_path):
    payload = {'records': logs(), 'min_samples': 3}
    outcome = execute('log_analysis', {}, {'trace_id': 'trace-test', 'payload': payload,
                      'request': {'task_id': 'W3-ORC-1-100'}}, repo_root=tmp_path)
    assert engine_v2.validate_agent_result('LRC2', outcome)['status'] == 'valid'
    artifact = outcome['artifacts'][0]
    data = (tmp_path/artifact['path']).read_bytes()
    assert hashlib.sha256(data).hexdigest() == artifact['sha256']
    assert json.loads(data)['source_sha256'] == hashlib.sha256(canonical(logs())).hexdigest()
    assert outcome['status'] == 'COMPLETED' and outcome['mutated'] is True
    with pytest.raises(ValueError, match='reconcile'):
        execute('log_analysis', {}, {'trace_id': 'trace-test', 'payload': payload, 'request': {}}, repo_root=tmp_path)


@pytest.mark.parametrize('payload', [{'records': []}, {'records': 'wrong'}, {'records': [{}], 'min_samples': True},
                                   {'source_file': '../outside.json'}])
def test_missing_or_invalid_data_is_not_completed(tmp_path, payload):
    with pytest.raises(ValueError):
        execute('log_analysis', {}, {'payload': payload, 'request': {}}, repo_root=tmp_path)
    assert not list(tmp_path.rglob('*.json'))
