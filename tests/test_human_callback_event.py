import json
import subprocess
from pathlib import Path
import pytest

from tests.test_human_callback import waiting, approve, AUTH
from tools.human_callback import respond
from tools.human_callback_event import process_event
from workflows.human_callback import reconcile_callback, digest
from workflows.runtime_circuit import ReconciliationRequired
from tools.runtime_circuit_intake import make_runtime


def test_owner_can_apply_one_edited_form_without_terminal_flags(monkeypatch, tmp_path):
    request, task, callback = waiting(monkeypatch, tmp_path)
    reply = approve(callback)
    form = tmp_path/task['payload']['human_cycle']['response_path']
    form.write_text(json.dumps(reply))
    checkpoints = []
    def checkpoint():
        snapshot = json.loads((tmp_path/'repo_events/runtime_circuit/tasks'/f"{task['task_id']}.json").read_text())
        assert snapshot['payload']['human_cycle']['callbacks'][digest(reply)]['state'] == 'PENDING'
        assert snapshot['human_approval'] is None
        checkpoints.append(1)
    result = process_event(tmp_path, actor='BBXDOO', owner='BBXDOO', event_name='workflow_dispatch',
        event={}, evidence='github:owner-run', mode='apply', callback=str(form.relative_to(tmp_path)), checkpoint=checkpoint)
    assert result[0]['task_status'] == 'COMPLETED' and checkpoints == [1]
    repeated = process_event(tmp_path, actor='BBXDOO', owner='BBXDOO', event_name='workflow_dispatch',
        event={}, evidence='github:rerun', mode='apply', callback=str(form.relative_to(tmp_path)), checkpoint=checkpoint)
    assert repeated[0]['status'] == 'SKIPPED' and checkpoints == [1]


def test_blank_template_and_nonowner_do_not_approve(monkeypatch, tmp_path):
    _, task, _ = waiting(monkeypatch, tmp_path)
    file = task['payload']['human_cycle']['response_path']
    result = process_event(tmp_path, actor='BBXDOO', owner='BBXDOO', event_name='workflow_dispatch', event={}, evidence='github:run',mode='apply',callback=file)
    assert result[0]['status'] == 'SKIPPED'
    with pytest.raises(ValueError, match='owner'):
        process_event(tmp_path, actor='someone-else', owner='BBXDOO', event_name='workflow_dispatch', event={}, evidence='github:run',mode='apply',callback=file)


def test_remote_checkpoint_failure_prevents_action_and_can_be_reconciled(monkeypatch, tmp_path):
    path, task, callback = waiting(monkeypatch, tmp_path); reply = approve(callback)
    def failure(): raise OSError('remote push rejected')
    with pytest.raises(OSError, match='push'):
        respond(tmp_path,path,reply,authority_context=AUTH,host_evidence='github:run',checkpoint=failure)
    runtime = make_runtime(tmp_path)
    saved = json.loads((runtime.directory/'tasks'/f"{task['task_id']}.json").read_text())
    assert saved['human_approval'] is None and saved['status'] == 'WAITING_HUMAN'
    with pytest.raises(ReconciliationRequired):
        respond(tmp_path,path,reply,authority_context=AUTH,host_evidence='github:run')
    reconcile_callback(runtime,saved,digest(reply),outcome='NOT_APPLIED',authority_context=AUTH,host_evidence='host:confirmed-no-effects')
    result = respond(tmp_path,path,reply,authority_context=AUTH,host_evidence='github:run')
    assert result['task_status'] == 'COMPLETED'


def test_event_cannot_apply_newer_unseen_response(monkeypatch, tmp_path):
    _, task, callback = waiting(monkeypatch, tmp_path)
    path = tmp_path/task['payload']['human_cycle']['response_path']
    path.write_text(json.dumps(approve(callback)))
    monkeypatch.setattr(subprocess, 'check_output', lambda *a, **kw: b'{"different":"older response"}')
    with pytest.raises(ValueError, match='content changed'):
        process_event(tmp_path,actor='BBXDOO',owner='BBXDOO',event_name='workflow_dispatch', event={},evidence='github:run',
            mode='apply',callback=str(path.relative_to(tmp_path)),event_sha='a'*40)


def test_real_owner_push_range_finds_and_applies_edited_response(monkeypatch,tmp_path):
    _, task, callback=waiting(monkeypatch,tmp_path)
    def git(*args):
        return subprocess.check_output(['git','-c','user.name=callback-test','-c','user.email=callback@example.invalid',*args],cwd=tmp_path,text=True).strip()
    git('init','-q');git('add','.');git('commit','-qm','blank form')
    before=git('rev-parse','HEAD')
    path=tmp_path/task['payload']['human_cycle']['response_path']
    path.write_text(json.dumps(approve(callback)))
    git('add','.');git('commit','-qm','owner response')
    after=git('rev-parse','HEAD')
    result=process_event(tmp_path,actor='BBXDOO',owner='BBXDOO',event_name='push',
        event={'before':before,'after':after},evidence='github:owner-push')
    assert result[0]['task_status']=='COMPLETED'
