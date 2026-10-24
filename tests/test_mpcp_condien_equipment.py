import json
from pathlib import Path
import sqlite3
import subprocess
import sys

import pytest

from src.core.condien import Condien
from src.core.condien_store import CondienStore
from protocol.mpcp.env.boundary import CrossLEnvironmentBoundary
from protocol.mpcp.lib.registry import LibraryRegistry


ROOT = Path(__file__).resolve().parents[1]


def context(name='CONTEXT'):
    c = Condien(name, layers=['A', 'B', 'C', 'D'], read_layers=['B', 'C'], deny_layers=['D'],
                continuity='carry-forward', modew='REPORT', paper='PAPER-1')
    c.write_layer('B', 'title', 'ข้อมูลทดสอบ')
    c.write_layer('B', 'excluded', 'synthetic value')
    c.get_layer('B').deny.add('excluded')
    c.carry('next', {'task': 'continue'})
    return c


def test_full_state_roundtrip_keeps_native_semantics_without_changing_inspection():
    c = context()
    state = c.to_state()
    restored = Condien.from_state(state)
    assert restored.to_state() == state and restored.to_dict() == c.to_dict()
    assert restored.recall('next') == {'task': 'continue'}
    assert 'layers' not in restored.to_dict()  # identity inspection is not a full data dump
    with pytest.raises(KeyError):
        restored.read_from_layer('B', 'excluded')
    with pytest.raises(PermissionError):
        restored.get_layer('D')
    state['layers'][1]['data']['title'] = 'changed'
    assert restored.read_from_layer('B', 'title') == 'ข้อมูลทดสอบ'


def test_store_restores_layers_and_carry_after_a_new_process(tmp_path):
    store = CondienStore(tmp_path / 'context.sqlite')
    c = context(); saved = store.save(c)
    program = ('import json,sys; from src.core.condien_store import CondienStore; '
               'from protocol.mpcp.env.boundary import CrossLEnvironmentBoundary; '
               's=CondienStore(sys.argv[1]).load("CONTEXT"); '
               'print(json.dumps({"carry":s.condien.recall("next"),'
               '"scope":CrossLEnvironmentBoundary.scope_condien(s.condien,("LAYER_B",)),"id":s.snapshot_id}))')
    result = subprocess.run([sys.executable, '-c', program, str(store.path)], cwd=ROOT,
                            check=True, capture_output=True, text=True)
    view = json.loads(result.stdout)
    assert view['id'] == saved.snapshot_id
    assert view['carry'] == {'task': 'continue'}
    assert view['scope']['layers'] == {'B': {'title': 'ข้อมูลทดสอบ'}}


def test_immutable_versions_and_stale_writer_conflict(tmp_path):
    store = CondienStore(tmp_path / 'context.sqlite')
    first = store.save(context())
    first.condien.write_layer('B', 'title', 'new')
    second = store.save(first.condien, expected_revision=1)
    assert second.revision == 2
    assert store.load('CONTEXT', revision=1).condien.read_from_layer('B', 'title') == 'ข้อมูลทดสอบ'
    assert store.load('CONTEXT').snapshot_id == second.snapshot_id
    with pytest.raises(ValueError, match='REVISION_CONFLICT'):
        store.save(context(), expected_revision=1)
    assert len(store.versions('CONTEXT')) == 2


def test_previous_context_link_survives_restart(tmp_path):
    store = CondienStore(tmp_path / 'context.sqlite')
    first = store.save(context('PREVIOUS'))
    next_context = context('NEXT')
    next_context.carry_forward_from(first.condien)
    with pytest.raises(ValueError, match='EXPLICIT_PREVIOUS_SNAPSHOT_REQUIRED'):
        store.save(next_context)
    saved = store.save(next_context, previous_snapshot_id=first.snapshot_id)
    loaded = CondienStore(store.path).load_snapshot(saved.snapshot_id)
    assert loaded.condien.previous.to_state() == first.condien.to_state()
    assert loaded.condien.history == ['PREVIOUS']
    assert loaded.previous_snapshot_id == first.snapshot_id


def test_unsaved_predecessor_changes_cannot_hide_behind_an_old_reference(tmp_path):
    store = CondienStore(tmp_path / 'context.sqlite')
    old = context('PREVIOUS'); saved = store.save(old)
    old.write_layer('B', 'title', 'unsaved')
    new = context('NEXT'); new.carry_forward_from(old)
    with pytest.raises(ValueError, match='PREVIOUS_STATE_MISMATCH'):
        store.save(new, previous_snapshot_id=saved.snapshot_id)


def test_corrupted_snapshot_is_not_treated_as_context(tmp_path):
    store = CondienStore(tmp_path / 'context.sqlite')
    saved = store.save(context())
    with sqlite3.connect(store.path) as db:
        db.execute('UPDATE snapshots SET body=? WHERE snapshot_id=?', ('{}', saved.snapshot_id))
    with pytest.raises(ValueError, match='SNAPSHOT_HASH_MISMATCH'):
        store.load('CONTEXT')


def test_reading_missing_store_does_not_create_database(tmp_path):
    store = CondienStore(tmp_path / 'missing.sqlite')
    with pytest.raises(FileNotFoundError):
        store.load('missing')
    assert not store.path.exists()


@pytest.mark.parametrize('value', [float('nan'), {'not-json'}, (1, 2), {1: 'key coercion'}])
def test_storage_refuses_lossy_or_non_json_data_before_writing(tmp_path, value):
    c = context(); c.write_layer('B', 'unsupported', value)
    store = CondienStore(tmp_path / 'context.sqlite')
    with pytest.raises((ValueError, TypeError)):
        store.save(c)
    assert not store.path.exists()


def test_unknown_state_fields_and_layer_identity_do_not_disappear():
    state = context().to_state(); state['extra'] = 'not understood'
    with pytest.raises(ValueError, match='STATE_FIELDS_INVALID'):
        Condien.from_state(state)
    state = context().to_state(); state['identity']['LAYERS'] = ['B']
    with pytest.raises(ValueError, match='LAYER_IDENTITY_MISMATCH'):
        Condien.from_state(state)


def test_equipment_registry_distinguishes_declared_names_from_real_builders(monkeypatch):
    from protocol.mpcp.runtime import executor
    monkeypatch.setattr(executor, 'PILLAR_REGISTRY', {})
    registry = LibraryRegistry()
    assert 'storage' in registry.library_group('core')
    assert not registry.equipment_report(['storage'])['storage']['available']
    calls = []
    builder = lambda: calls.append('constructed')
    registry.register_equipment('real', builder, group='core', capabilities=['scoped_context_read'])
    assert registry.equipment_report(['real'])['real']['available']
    with pytest.raises(ValueError, match='EQUIPMENT_UNAVAILABLE'):
        registry.activate_equipment(['real', 'missing'])
    assert executor.PILLAR_REGISTRY == {} and calls == []
    registry.activate_equipment(['real'])
    assert executor.PILLAR_REGISTRY['real'] is builder and calls == []
    with pytest.raises(ValueError, match='UNIQUE_EQUIPMENT'):
        registry.register_equipment('real', builder, group='core', capabilities=['x'])


def test_equipment_cannot_silently_replace_another_host_route(monkeypatch):
    from protocol.mpcp.runtime import executor
    monkeypatch.setattr(executor, 'PILLAR_REGISTRY', {'owned': lambda: None})
    registry = LibraryRegistry()
    registry.register_equipment('owned', lambda: None, group='core', capabilities=['x'])
    with pytest.raises(ValueError, match='ROUTE_ALREADY_OWNED'):
        registry.activate_equipment(['owned'])


def test_core_model_does_not_require_storage_equipment_to_be_installed():
    program = '''import builtins
original = builtins.__import__
def no_sqlite(name, *args, **kwargs):
    if name == "sqlite3":
        raise ImportError("SQLite equipment is absent")
    return original(name, *args, **kwargs)
builtins.__import__ = no_sqlite
from src.core.condien import Condien
from src.core.blueprint import Blueprint
from protocol.mpcp.lib.registry import LibraryRegistry
assert Condien("core-only").name == "core-only"
'''
    subprocess.run([sys.executable, '-c', program], cwd=ROOT, check=True, capture_output=True, text=True)


def test_storage_cli_then_paper_cli_reads_only_allowed_persisted_values(tmp_path):
    db = tmp_path / 'context.sqlite'
    seed = subprocess.run([sys.executable, str(ROOT/'tools/mpcp_condien.py'), '--store', str(db),
                           '--input', str(ROOT/'tools/agent_sandbox/condien_state.json'), '--save'],
                          cwd=ROOT, check=True, capture_output=True, text=True)
    snapshot_id = json.loads(seed.stdout)['snapshot_id']
    output = tmp_path / 'paper'
    cmd = [sys.executable, str(ROOT/'tools/mpcp_papers.py'), '--request',
           str(ROOT/'tools/agent_sandbox/condien_paper.json'), '--output', str(output),
           '--condien-store', str(db), '--condien-name', 'EQUIPMENT-CONTEXT', '--execute']
    subprocess.run(cmd, cwd=ROOT, check=True, capture_output=True, text=True)
    result = json.loads((output/'result.json').read_text())
    assert result['state'] == 'SUCCESS'
    assert result['condien_snapshot']['snapshot_id'] == snapshot_id
    returned = result['papers']['READ-B']['result']['result']
    assert returned['context']['layers'] == {'B': {'title': 'บริบทที่กลับมาใช้ต่อได้'}}
    assert returned['context_ref'] == 'condien:' + snapshot_id
    assert result['equipment']['condien-view']['available']
    assert 'synthetic excluded example' not in (output/'result.json').read_text()


def test_concurrent_storage_writers_keep_one_revision(tmp_path):
    db = tmp_path/'context.sqlite'
    # Create the schema and version 1 before competing for expected revision 1.
    CondienStore(db).save(context())
    program = ('import sys; from src.core.condien_store import CondienStore; '
               's=CondienStore(sys.argv[1]); c=s.load("CONTEXT").condien; '
               's.save(c,expected_revision=1)')
    workers = [subprocess.Popen([sys.executable, '-c', program, str(db)], cwd=ROOT,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(2)]
    codes = []
    for worker in workers:
        worker.communicate(timeout=20); codes.append(worker.returncode)
    assert sorted(codes) == [0, 1]
    assert len(CondienStore(db).versions('CONTEXT')) == 2
