import json
import pytest
from tests.test_orchestration_support import blocked
from tests.test_runtime_circuit import success
from workflows.runtime_circuit import WorkflowRuntime
from workflows.support_catalog import Adapter, SupportCatalog, register_repository_tool, tool_inventory


def test_verified_support_survives_restart_and_requires_explicit_original_retry(tmp_path):
    runtime, work = blocked(tmp_path)
    calls = []
    catalog = SupportCatalog()
    catalog.register(Adapter('repair', 'TOOL', frozenset({'repair'}),
        lambda c: {'resolved': True, 'mutated': True}, lambda *a: {'passed': True}))
    runtime.support_for(work, 'repair', catalog=catalog)
    saved = json.loads((runtime.directory/'tasks'/f"{work['task_id']}.json").read_text())
    assert saved['status'] == 'RETURNED'
    def runner(job, request, **kw):
        calls.append(job); return success(job, request)
    restarted = WorkflowRuntime(runtime.directory, runner=runner, verifier=lambda *a: {'passed': True}, reference_root=tmp_path)
    assert not calls
    restarted.continue_work(saved)
    assert saved['status'] == 'COMPLETED' and calls == ['design']
    restarted.continue_work(saved)
    assert calls == ['design']


def test_any_existing_tools_file_can_have_a_host_adapter(tmp_path):
    root = tmp_path; (root/'tools').mkdir()
    (root/'tools/special.py').write_text('# unusual but legitimate tool')
    catalog = SupportCatalog()
    def handler(context):
        (root/'calculation.txt').write_text(str(sum(context['request']['values'])))
        return {'resolved': True, 'mutated': True}
    register_repository_tool(catalog, root, 'tools/special.py', {'calculate'}, handler,
        lambda c, r: {'passed': (root/'calculation.txt').read_text() == str(sum(c['request']['values']))})
    assert tool_inventory(root, catalog)[0]['registered']
    runtime, work = blocked(root)
    runtime.support_for(work, 'calculate', catalog=catalog, request={'values': [4, 9]})
    assert work['status'] == 'RETURNED' and (root/'calculation.txt').read_text() == '13'
    with pytest.raises(ValueError):
        register_repository_tool(catalog, root, '../outside.py', {'anything'}, handler, lambda *a: {'passed': True})


def test_request_type_and_availability_filter_without_invoking(tmp_path):
    catalog = SupportCatalog(); seen = []
    catalog.register(Adapter('restricted', 'TOOL', frozenset({'repair'}), lambda c: seen.append(c),
        lambda *a: {'passed': True}, request_types=frozenset({'ISSUE'})))
    runtime, work = blocked(tmp_path)
    runtime.support_for(work, 'repair', catalog=catalog, request_type='REQUEST')
    assert not seen and work['status'] == 'BLOCKED'


def test_registered_recipe_runs_from_root_request_through_actual_executors(monkeypatch, tmp_path):
    from tests.test_runtime_circuit_intake import configure, request
    from tools import request_cycle as rc
    configure(monkeypatch, tmp_path)
    path = request(tmp_path)
    source = path.read_text()
    start = source.index('```w3-circuit')
    path.write_text(source[:start] + '```w3-circuit\n' + json.dumps({
        'workflow': 'log_analysis', 'input': {'payload': {'source_file': 'logs.json', 'min_samples': 3}}
    }) + '\n```\n')
    envelope = rc.process(path)
    result = envelope['runtime_result']
    assert result['status'] == 'WAITING_HUMAN'
    assert [item['module'] for item in result['stage_results']] == ['LRC2', 'Gemini']
    assert result['stage_results'][1]['agent_result']['decision'] == 'VERIFIED'
    assert (tmp_path / result['artifacts'][0]['path']).is_file()
    assert rc.process(path)['status'] == 'SKIPPED'


def test_declared_stage_support_is_automatic_but_does_not_replay_owner(tmp_path):
    (tmp_path/'tools').mkdir(); (tmp_path/'tools/validate_metadata.py').write_text('# installed')
    (tmp_path/'note.md').write_text('# An actual readable output\n')
    calls = []
    def runner(job, request, **kw):
        calls.append(job)
        return {'status': 'BLOCKED', 'agent_result': {'mutated': False}, 'result_validation': {'status': 'valid'}}
    runtime = WorkflowRuntime(tmp_path/'evidence', runner=runner, verifier=lambda *a: {'passed': False}, reference_root=tmp_path)
    from tests.test_runtime_circuit import task
    work = runtime.run(task(), [{'task': 'design', 'support': {
        'capability': 'approval_metadata', 'kind': 'TOOL', 'request': {'paths': ['note.md']}}}])
    assert work['status'] == 'RETURNED' and calls == ['design']
    assert work['support'][-1]['result']['verification']['passed']
    assert work['runtime_circuit']['index'] == 0
    # Reloaded unresolved BLOCKED tasks are never implicitly supported again.
    work['status'] = 'BLOCKED'
    runtime.continue_work(work)
    assert calls == ['design'] and len(work['support']) == 1


def test_bad_support_declaration_rejected_before_execution(tmp_path):
    from tests.test_runtime_circuit import task
    calls = []
    runtime = WorkflowRuntime(tmp_path, runner=lambda *a, **kw: calls.append(1), verifier=lambda *a: {'passed': True})
    with pytest.raises(ValueError, match='support'):
        runtime.run(task(), [{'task': 'design', 'support': {'capability': 'anything', 'shell': 'execute me'}}])
    assert not calls
