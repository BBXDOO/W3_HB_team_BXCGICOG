import json
from copy import deepcopy
from pathlib import Path
import subprocess
import sys

import pytest

from protocol.mpcp.runtime.paper import PaperPackRuntime, PaperPermit, prepare_paper_pack
from protocol.mpcp.runtime.executor import register
from protocol.mpcp.modew.file_artifact import FileVoidTextModew, verify_text_artifact
from protocol.mpcp.env.boundary import CrossLEnvironmentBoundary
from src.core.condien import Condien


@pytest.fixture
def setup(tmp_path, monkeypatch):
    monkeypatch.setattr('protocol.mpcp.runtime.executor.PILLAR_REGISTRY', {})
    # paper.py imports the same registry object; preserve this owned registration only.
    monkeypatch.setattr('protocol.mpcp.runtime.paper.PILLAR_REGISTRY', __import__(
        'protocol.mpcp.runtime.executor', fromlist=['PILLAR_REGISTRY']).PILLAR_REGISTRY)
    root = tmp_path / 'artifacts'
    register('text-equipment', lambda: FileVoidTextModew(root))
    runtime = PaperPackRuntime(tmp_path / 'journal')
    pack = {'PAPER_PACK_ID': 'PACK-1', 'CHAIN_ID': 'CHAIN-1', 'EVENT_ID': 'EV-1',
            'RESPONSIBLE_MODULE': 'MPCP', 'RETURN_TO': 'MPCP',
            'SCOPE': 'local-file-experiment', 'BOUNDARY': 'host-output-root', 'PAPERS': [
                {'PAPER_ID': pid, 'TASK': 'create ' + pid, 'INTENT': 'render template',
                 'CONTENT': {'template': '# $title\n', 'values': {'title': pid}, 'target': pid + '.md'}}
                for pid in ('P1', 'P2')]}
    routes = {p['PAPER_ID']: 'text-equipment' for p in pack['PAPERS']}
    verify = lambda paper, result: verify_text_artifact(root, paper, result)
    return runtime, pack, routes, verify, root


def grant(runtime, pack, routes, verify, **kwargs):
    report = runtime.run(pack, routes=routes, verify=verify, **kwargs)
    return [PaperPermit(report['pack_hash'], pid, route, 'test:explicit-host-grant') for pid, route in routes.items()]


def test_two_papers_create_real_files_via_file_void_and_return_to_one_event(setup):
    runtime, pack, routes, verify, root = setup
    original = deepcopy(pack)
    permits = grant(runtime, pack, routes, verify)
    result = runtime.run(pack, routes=routes, permits=permits, verify=verify)
    assert result['state'] == 'SUCCESS'
    assert result['event_id'] == 'EV-1' and result['return_to'] == 'MPCP'
    for pid in routes:
        assert (root / (pid + '.md')).read_text() == '# ' + pid + '\n'
        entry = result['papers'][pid]
        assert entry['status'] == 'COMPLETED' and entry['verification']['passed']
        assert entry['result']['mutated'] is True
        void = entry['result']['result']['file_void']
        assert void['source_mutated'] is False
        assert void['manifestation']['write_performed'] is False
        assert entry['result']['result']['write_performed'] is True
        env = entry['result']['env']['before']
        assert env['PAPER_ID'] == pid and env['EVENT_ID'] == 'EV-1'
        assert 'PAPERS' not in env and 'ROT_RULEBOOK' not in env
    assert pack == original
    assert runtime.run(pack, routes=routes, permits=permits, verify=verify) == result


def test_no_permit_waits_and_a_subset_can_be_distributed(setup):
    runtime, pack, routes, verify, root = setup
    permits = grant(runtime, pack, routes, verify)
    assert not root.exists()
    result = runtime.run(pack, routes=routes, permits=permits[:1], verify=verify)
    assert result['state'] == 'WAIT'
    assert result['papers']['P1']['status'] == 'COMPLETED'
    assert result['papers']['P2']['status'] == 'PENDING'
    assert not (root / 'P2.md').exists()


def test_host_can_distribute_to_two_different_worksites(setup):
    runtime, pack, routes, _, root = setup
    secondary = root / 'other-worksite'
    register('other-text-equipment', lambda: FileVoidTextModew(secondary))
    routes['P2'] = 'other-text-equipment'
    verify = lambda p, r: verify_text_artifact(root if p['PAPER_ID'] == 'P1' else secondary, p, r)
    permits = grant(runtime, pack, routes, verify)
    result = runtime.run(pack, routes=routes, permits=permits, verify=verify)
    assert result['state'] == 'SUCCESS'
    assert (root / 'P1.md').exists() and (secondary / 'P2.md').exists()
    assert result['papers']['P1']['modew'] != result['papers']['P2']['modew']


def test_forged_paper_authority_and_changed_permit_do_not_run(setup):
    runtime, pack, routes, verify, root = setup
    permits = grant(runtime, pack, routes, verify)
    invalid = PaperPermit('wrong-work', 'P1', 'text-equipment', 'test:wrong')
    assert runtime.run(pack, routes=routes, permits=[invalid], verify=verify)['state'] == 'WAIT'
    pack['PAPERS'][0]['approved_by'] = 'BBX19'
    with pytest.raises(ValueError, match='UNKNOWN_KEYS'):
        runtime.run(pack, routes=routes, permits=permits, verify=verify)
    assert not root.exists()


def test_preflight_bad_second_paper_never_executes_first(setup):
    runtime, pack, routes, verify, root = setup
    permits = grant(runtime, pack, routes, verify)
    routes['P2'] = 'unknown'
    with pytest.raises(ValueError, match='REGISTERED_HOST_ROUTE_REQUIRED'):
        runtime.run(pack, routes=routes, permits=permits, verify=verify)
    assert not root.exists()


def test_saved_event_cannot_be_rebound_to_changed_commands(setup):
    runtime, pack, routes, verify, root = setup
    permits = grant(runtime, pack, routes, verify)
    pack['PAPERS'][0]['CONTENT']['values']['title'] = 'changed'
    with pytest.raises(ValueError, match='SAVED_WORK_CHANGED'):
        runtime.run(pack, routes=routes, permits=permits, verify=verify)
    assert not root.exists()


def test_interrupted_execution_is_not_replayed(setup):
    runtime, pack, routes, verify, root = setup
    permits = grant(runtime, pack, routes, verify)
    path = next(runtime.directory.glob('*.json'))
    state = json.loads(path.read_text())
    state['papers']['P1']['status'] = 'IN_PROGRESS'
    path.write_text(json.dumps(state))
    result = runtime.run(pack, routes=routes, permits=permits, verify=verify)
    assert result['papers']['P1']['status'] == 'NEEDS_RECONCILIATION'
    assert result['papers']['P2']['status'] == 'COMPLETED'
    assert not (root / 'P1.md').exists()


def test_final_save_failure_retains_effects_and_reconciles_without_rewrite(setup, monkeypatch):
    runtime, pack, routes, verify, root = setup
    permits = grant(runtime, pack, routes, verify)
    save = runtime._save
    failed = []
    def fail_once(path, state):
        if state['papers']['P1']['status'] == 'COMPLETED' and not failed:
            failed.append(True)
            raise OSError('final save failed')
        save(path, state)
    monkeypatch.setattr(runtime, '_save', fail_once)
    result = runtime.run(pack, routes=routes, permits=permits, verify=verify)
    first = result['papers']['P1']
    assert first['status'] == 'NEEDS_RECONCILIATION'
    before = (root / 'P1.md').stat().st_mtime_ns
    fixed = runtime.reconcile(pack, 'P1', observed_result=first['result'],
                              evidence='test:observed-file', verify=verify)
    assert fixed['state'] == 'SUCCESS'
    assert (root / 'P1.md').stat().st_mtime_ns == before


def test_tampered_completed_artifact_is_rechecked_and_never_silently_recreated(setup):
    runtime, pack, routes, verify, root = setup
    permits = grant(runtime, pack, routes, verify)
    runtime.run(pack, routes=routes, permits=permits, verify=verify)
    (root / 'P1.md').write_text('tampered')
    result = runtime.run(pack, routes=routes, permits=permits, verify=verify)
    assert result['state'] == 'WAIT' and result['papers']['P1']['status'] == 'WAITING'
    assert (root / 'P1.md').read_text() == 'tampered'


@pytest.mark.parametrize('target', ['../escape.md', '/escape.md', 'a/../../escape.md', 'out.pdf'])
def test_text_equipment_rejects_escape_or_unsupported_format(setup, target):
    runtime, pack, routes, verify, root = setup
    pack['PAPERS'][0]['CONTENT']['target'] = target
    permits = grant(runtime, pack, routes, verify)
    result = runtime.run(pack, routes=routes, permits=permits, verify=verify)
    assert result['papers']['P1']['status'] == 'STOPPED'
    assert not (root / 'P1.md').exists()
    assert (root / 'P2.md').exists()


def test_reference_resolution_is_explicit_and_preserves_provenance(setup):
    runtime, pack, routes, verify, root = setup
    command = deepcopy(pack['PAPERS'][0]); pack['PAPERS'] = ['Paper-A01.1']
    with pytest.raises(ValueError, match='REFERENCE_RESOLVER_REQUIRED'):
        prepare_paper_pack(pack)
    prepared = prepare_paper_pack(pack, resolve_reference=lambda reference: command)
    assert prepared['SOURCE_REFERENCES']['P1'] == 'Paper-A01.1'
    assert prepare_paper_pack(prepared)['SOURCE_REFERENCES']['P1'] == 'Paper-A01.1'


def test_review_requires_exact_successful_saved_result(setup):
    runtime, pack, routes, verify, root = setup
    class ReviewText(FileVoidTextModew):
        def run(self):
            result = super().run()
            result['review'] = True
            return result
    register('text-equipment', lambda: ReviewText(root))
    permits = grant(runtime, pack, routes, verify)
    result = runtime.run(pack, routes=routes, permits=permits, verify=verify)
    entry = result['papers']['P1']
    assert entry['status'] == 'WAITING_REVIEW'
    changed = deepcopy(entry['result']); changed['reason'] = 'changed'
    with pytest.raises(ValueError, match='EXACT_SAVED_RESULT'):
        runtime.reconcile(pack, 'P1', observed_result=changed, evidence='test:review', verify=verify, review_accepted=True)
    accepted = runtime.reconcile(pack, 'P1', observed_result=entry['result'], evidence='test:review', verify=verify, review_accepted=True)
    assert accepted['papers']['P1']['status'] == 'COMPLETED'
    assert runtime.run(pack, routes=routes, permits=permits, verify=verify)['papers']['P1']['status'] == 'COMPLETED'


def test_two_cli_processes_do_not_execute_papers_twice(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    output = tmp_path / 'run'
    command = [sys.executable, str(repo/'tools/mpcp_papers.py'), '--request',
               str(repo/'tools/agent_sandbox/paper_pack.json'), '--output', str(output), '--execute']
    processes = [subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for _ in range(2)]
    for process in processes:
        stdout, stderr = process.communicate(timeout=20)
        assert process.returncode == 0, (stdout, stderr)
    snapshot = json.loads(next((output/'papers').glob('*.json')).read_text())
    assert all(len(p['history']) == 1 for p in snapshot['papers'].values())


def test_condien_scope_honors_layer_and_key_read_deny():
    c = Condien('context', layers=['A', 'B'], deny_layers=['A'])
    c.add_layer('B', {'visible': 'ok', 'denied': 'not-for-output', 'not_selected': 'x'})
    layer = c.get_layer('B'); layer.read = {'visible', 'denied'}; layer.deny = {'denied'}
    view = CrossLEnvironmentBoundary.scope_condien(c, ('LAYER_B',))
    assert view['layers'] == {'B': {'visible': 'ok'}}
    layer.readable = False
    assert CrossLEnvironmentBoundary.scope_condien(c, ('LAYER_B',))['layers'] == {'B': {}}
    with pytest.raises(PermissionError):
        CrossLEnvironmentBoundary.scope_condien(c, ('LAYER_A',))
