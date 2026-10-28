from copy import deepcopy
import json

import pytest

from w3_tool_store.agent_workbench.tools.system_inspection import runner as inspection


def fixture_root(root):
    (root / 'tests').mkdir(exist_ok=True)
    (root / 'entry.py').write_text('VALUE = 1\n')
    (root / 'tests/test_bad.py').write_text('def test_bad():\n    assert False, "first system fails"\n')
    (root / 'tests/test_good.py').write_text('def test_good():\n    assert 2 + 2 == 4\n')
    return (
        ('FIRST', 'entry.py', ('tests/test_bad.py',)),
        ('SECOND', 'entry.py', ('tests/test_good.py',)),
    )


def context():
    return {'payload': {'inspection': 'w3_systems_v1'},
            'request': {'task_id': 'W3-ORC-1-42', 'source_id': 'RQ-INSPECTION'}}


def test_real_failure_has_followup_and_does_not_stop_next_system(monkeypatch, tmp_path):
    monkeypatch.setattr(inspection, 'CATALOG', fixture_root(tmp_path))
    original = (tmp_path / 'entry.py').read_bytes()
    result = inspection.execute(tmp_path, context())
    report = json.loads((tmp_path / result['artifacts'][0]['path']).read_text())
    assert [r['status'] for r in report['systems']] == ['FAIL', 'PASS']
    assert report['overall'] == 'PARTIAL' and report['inspection_state'] == 'FINISHED'
    assert len(report['blockers']) == 1
    assert (tmp_path / report['blockers'][0]).is_file()
    assert (tmp_path / 'entry.py').read_bytes() == original
    assert all(c['passed'] for c in inspection.report_checks(tmp_path, result))
    # A real JUnit change invalidates evidence; the paired check cannot trust PASS.
    xml = tmp_path / report['systems'][1]['evidence'][1]['path']
    xml.write_text(xml.read_text().replace('tests="1"', 'tests="99"'))
    assert not all(c['passed'] for c in inspection.report_checks(tmp_path, result))


def test_missing_entry_is_recorded_and_later_suite_runs(monkeypatch, tmp_path):
    catalog = fixture_root(tmp_path)
    monkeypatch.setattr(inspection, 'CATALOG', (('FIRST', 'missing.py', catalog[0][2]), catalog[1]))
    result = inspection.execute(tmp_path, context())
    report = json.loads((tmp_path / result['artifacts'][0]['path']).read_text())
    assert [r['status'] for r in report['systems']] == ['BLOCKED', 'PASS']
    assert 'missing.py' in report['systems'][0]['reason']
    assert all(c['passed'] for c in inspection.report_checks(tmp_path, result))


def test_timeout_is_bounded_and_does_not_mutate_source(tmp_path):
    fixture_root(tmp_path)
    (tmp_path / 'tests/test_slow.py').write_text('import time\ndef test_slow():\n    time.sleep(30)\n')
    row = inspection.run_suite(tmp_path, tmp_path / 'evidence', 'SLOW', 'entry.py',
                               ('tests/test_slow.py',), timeout=.05)
    assert row['status'] == 'TIMEOUT' and row['source_unchanged']
    assert row['exit_code'] is None and row['elapsed_seconds'] < 10


def test_request_cannot_inject_commands_or_paths(tmp_path):
    injected = context()
    injected['payload']['command'] = 'touch forbidden'
    with pytest.raises(ValueError, match='fixed inspection profile'):
        inspection.execute(tmp_path, injected)
    assert not (tmp_path / inspection.BASE).exists()
    with pytest.raises(ValueError, match='escapes'):
        inspection.inside(tmp_path, '../outside')


def test_interrupted_collection_keeps_prior_row_and_visible_progress(monkeypatch, tmp_path):
    monkeypatch.setattr(inspection, 'CATALOG', fixture_root(tmp_path))
    original = inspection.run_suite
    def interrupt(root, folder, system, entry, tests):
        if system == 'SECOND':
            raise RuntimeError('injected host interruption')
        return original(root, folder, system, entry, tests)
    monkeypatch.setattr(inspection, 'run_suite', interrupt)
    with pytest.raises(RuntimeError, match='interruption'):
        inspection.execute(tmp_path, context())
    latest = json.loads((tmp_path / inspection.BASE / 'latest.json').read_text())
    saved = json.loads((tmp_path / latest['report']).read_text())
    assert latest['inspection_state'] == 'IN_PROGRESS' and latest['finished_at'] is None
    assert saved['systems'][0]['status'] == 'FAIL' and len(saved['blockers']) == 1


def test_skipped_or_empty_suites_never_pass():
    assert inspection.classify(0, {'tests': 0, 'failures': 0, 'errors': 0, 'skipped': 0}) == 'BLOCKED'
    assert inspection.classify(0, {'tests': 1, 'failures': 0, 'errors': 0, 'skipped': 1}) == 'PARTIAL'


def test_root_request_runs_registered_inspection_then_pair_without_replay(monkeypatch, tmp_path):
    from tests.test_runtime_circuit_intake import configure
    from tools import request_cycle as rc
    configure(monkeypatch, tmp_path)
    monkeypatch.setattr(inspection, 'CATALOG', fixture_root(tmp_path))
    source = tmp_path / 'requests/RQ-INSPECTION.md'
    source.parent.mkdir(exist_ok=True)
    source.write_text('---\nrequest_id: RQ-INSPECTION\nrequest_type: runtime_circuit\n'
                      'task_keyword: design\ntarget_module: ChatGPT\nrequester: BBX19\n'
                      'final_signoff_required: true\n---\n```w3-circuit\n'
                      + json.dumps({'workflow': 'system_inspection', 'input': {'payload': {'inspection': 'w3_systems_v1'}}})
                      + '\n```\n')
    result = rc.process(source)
    runtime = result['runtime_result']
    assert runtime['status'] == 'WAITING_HUMAN'
    assert [r['module'] for r in runtime['stage_results']] == ['ChatGPT', 'Gemini']
    assert runtime['agent_result']['decision'] == 'VERIFIED'
    assert 'listed_checks=PARTIAL' in runtime['stage_results'][0]['agent_result']['summary']
    assert rc.process(source)['status'] == 'SKIPPED'
    assert len(list((tmp_path / inspection.BASE / 'runs').iterdir())) == 1
