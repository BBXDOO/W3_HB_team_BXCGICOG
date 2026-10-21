import json
from copy import deepcopy
from pathlib import Path
import pytest
from workflows.support_catalog import Adapter, SupportCatalog, FlowCatalog, tool_inventory
from workflows.runtime_circuit import WorkflowRuntime, ReconciliationRequired
from tools.orchestration_support import default_catalog
from tools.runtime_circuit_intake import parse_spec
from tests.test_runtime_circuit import task, success


def blocked(root):
    runtime = WorkflowRuntime(root/'evidence', runner=success, verifier=lambda *a: {'passed': False}, reference_root=root)
    work = runtime.run(task(), [{'task': 'design', 'request': {'intent': 'preserve me'}}])
    return runtime, work


def test_tool_runs_real_metadata_checks_and_preserves_owner(tmp_path):
    (tmp_path/'tools').mkdir(); (tmp_path/'tools/validate_metadata.py').write_text('# host tool')
    source = tmp_path/'note.md'; source.write_text('approved-by: BBX19\n')
    runtime, work = blocked(tmp_path)
    catalog = default_catalog(tmp_path)
    catalog.support(runtime, work, 'approval_metadata', kind='TOOL', request={'paths': ['note.md']})
    assert work['status'] == 'BLOCKED'
    assert work['support'][-1]['result']['diagnostics']['findings']
    assert source.read_text() == 'approved-by: BBX19\n'
    source.write_text('approved-by: BBX19\nreason: actual human decision\n')
    catalog.support(runtime, work, 'approval_metadata', request={'paths': ['note.md']})
    assert work['status'] == 'RETURNED'
    receipt = work['support'][-1]['result']
    assert receipt['verification']['passed']
    assert work['destination'] == {'module': 'ChatGPT', 'task': 'design'}
    assert json.loads((tmp_path/receipt['evidence']).read_text())['resolved']
    assert work['runtime_circuit']['index'] == 0


def test_pair_replaces_unavailable_partner_and_passes_full_context(tmp_path):
    catalog = SupportCatalog(); seen = []
    def handler(context):
        seen.append(deepcopy(context)); (tmp_path/'answer.txt').write_text(context['stage']['request']['intent'])
        return {'resolved': True, 'mutated': True, 'value': 'preserve me'}
    for module, available in [('Gemini', False), ('Grok', True), ('ChatGPT', True)]:
        catalog.register(Adapter(module, 'SPECIALIST', frozenset({'solve'}), handler,
            lambda c, r: {'passed': (tmp_path/'answer.txt').read_text() == c['stage']['request']['intent']},
            module=module, available=lambda a=available: a))
    runtime, work = blocked(tmp_path)
    catalog.support(runtime, work, 'solve', preferred='Gemini', owner='ChatGPT', kind='SPECIALIST', request={'question': 'context'})
    assert work['status'] == 'RETURNED'
    support = work['support'][-1]
    assert support['name'] == 'Grok'
    assert support['result']['selection']['preferred'] == 'Gemini'
    assert seen[0]['request']['question'] == 'context' and seen[0]['blocker']
    assert seen[0]['source_id'] == work.get('source_id')
    with pytest.raises(ValueError, match='blocker'):
        catalog.support(runtime, work, 'solve')


def test_unknown_capability_remains_blocked(tmp_path):
    runtime, work = blocked(tmp_path)
    SupportCatalog().support(runtime, work, 'unimplemented')
    assert work['status'] == 'BLOCKED' and not work['support']
    assert work['evidence'][-1]['actor'] == 'support-selection'


def test_verifier_rejects_claimed_resolution(tmp_path):
    runtime, work = blocked(tmp_path); catalog = SupportCatalog()
    catalog.register(Adapter('liar', 'TOOL', frozenset({'repair'}),
        lambda c: {'resolved': True, 'mutated': True}, lambda c, r: {'passed': False}))
    catalog.support(runtime, work, 'repair')
    assert work['status'] == 'BLOCKED' and work['mutated']


def test_uncertain_effect_does_not_try_another_partner(tmp_path):
    runtime, work = blocked(tmp_path); calls = []; catalog = SupportCatalog()
    def fail(c):
        calls.append(1); (tmp_path/'effect').write_text('happened'); raise OSError('transport lost')
    catalog.register(Adapter('a', 'TOOL', frozenset({'repair'}), fail, lambda *a: {'passed': True}))
    catalog.register(Adapter('b', 'TOOL', frozenset({'repair'}), lambda c: calls.append(2), lambda *a: {'passed': True}))
    with pytest.raises(ReconciliationRequired): catalog.support(runtime, work, 'repair')
    with pytest.raises(ReconciliationRequired): catalog.support(runtime, work, 'repair')
    assert calls == [1] and (tmp_path/'effect').exists()


def test_support_evidence_failure_retains_actual_result(tmp_path, monkeypatch):
    runtime, work = blocked(tmp_path); catalog = SupportCatalog()
    catalog.register(Adapter('real', 'TOOL', frozenset({'repair'}),
        lambda c: {'resolved': True, 'mutated': True, 'actual': 42}, lambda *a: {'passed': True}))
    original = runtime._evidence
    def evidence(t, kind, value):
        if kind == 'support': raise OSError('disk failure')
        return original(t, kind, value)
    monkeypatch.setattr(runtime, '_evidence', evidence)
    with pytest.raises(ReconciliationRequired) as error: catalog.support(runtime, work, 'repair')
    assert error.value.result['actual'] == 42 and work['mutated']


def test_flow_dependency_order_and_cycle_validation():
    flows = FlowCatalog()
    flows.register('review', [{'id': 'b', 'after': ['a'], 'task': 'verify'}, {'id': 'a', 'task': 'design'}])
    stages = flows.plan('review', {'payload': {'intent': 'actual'}})
    assert [s['module'] for s in stages] == ['ChatGPT', 'Gemini']
    assert 'payload' not in stages[1]['request']
    stages[0]['request'].clear()
    assert flows.plan('review', {})[0]['request'] == {}
    with pytest.raises(ValueError, match='cycle'):
        flows.register('cycle', [{'id': 'x', 'after': ['x'], 'task': 'verify'}])
    with pytest.raises(ValueError): flows.register('wrong-route', [{'id': 'x', 'task': 'design', 'module': 'Gemini'}])


def test_request_can_choose_real_workflow_without_writing_stages():
    spec = parse_spec({'_request_text': '```w3-circuit\n{"workflow":"log_analysis","input":{"payload":{"records":[{"status":"FAILED"}]}}}\n```\n'})
    assert [s['task'] for s in spec['stages']] == ['log_analysis', 'verify']
    assert spec['stages'][0]['request']['payload']['records'][0]['status'] == 'FAILED'
    with pytest.raises(ValueError): parse_spec({'_request_text': '```w3-circuit\n{"workflow":"fake"}\n```\n'})


def test_inventory_does_not_execute_and_path_escape_is_rejected(tmp_path):
    tools = tmp_path/'tools'; tools.mkdir()
    (tools/'danger.py').write_text('raise RuntimeError("must never import")')
    assert tool_inventory(tmp_path) == [{'path': 'tools/danger.py', 'registered': False}]
    (tools/'validate_metadata.py').write_text('')
    runtime, work = blocked(tmp_path)
    with pytest.raises(ReconciliationRequired):
        default_catalog(tmp_path).support(runtime, work, 'approval_metadata', request={'paths': ['../escape.md']})


def test_real_origin_pair_selection_and_byte_syntax_verification(tmp_path):
    from tests.test_origin_operations import OriginOperationsTests
    fixture = OriginOperationsTests(); fixture.setUp()
    root = fixture.root
    source = root/'ChatGPT/read.json'; source.parent.mkdir(exist_ok=True); source.write_text('{"actual": 7}')
    authority = {'origin_scopes': {'Gemini': [{'path': 'ChatGPT/read.json', 'operations': ['read']}]}}
    runtime, work = blocked(root)
    default_catalog(root, authority_context=authority).support(runtime, work, 'file_review',
        preferred='NotInstalled', owner='ChatGPT', kind='SPECIALIST', request={'paths': ['ChatGPT/read.json']})
    assert work['status'] == 'RETURNED'
    result = work['support'][-1]['result']
    assert result['agent_result']['module'] == 'Gemini'
    assert result['agent_result']['evidence'][0]['path'] == 'ChatGPT/read.json'
    assert result['verification']['passed']
