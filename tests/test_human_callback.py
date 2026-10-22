from copy import deepcopy
import json
from pathlib import Path
import pytest

from tools import request_cycle as rc
from tools.human_callback import authority, respond, review_request
from tools.runtime_circuit_intake import make_runtime
from workflows import human_callback as flow
from workflows.runtime_circuit import ReconciliationRequired
from tests.test_runtime_circuit_intake import configure, request


def waiting(monkeypatch, root):
    configure(monkeypatch, root)
    path = request(root)
    result = rc.process(path)['runtime_result']
    task = json.loads((root/result['orchestration_evidence']).read_text())
    callback = json.loads((root/result['callback_path']).read_text())
    return path, task, callback


def approve(callback, decision='APPROVE'):
    result = deepcopy(callback)
    result.update(decision=decision, reason='ตรวจผลตามขอบเขตที่มอบหมายแล้ว',
                  annotations=['รับเฉพาะผลรอบนี้ เป้าหมายส่วนที่เหลือยังคงอยู่'],
                  evidence=['human-comment:actual-review'])
    return result


AUTH = authority('BBX19', 'human-comment:actual-review')


def test_one_response_links_intent_decision_and_orchestration(monkeypatch, tmp_path):
    path, task, callback = waiting(monkeypatch, tmp_path)
    assert callback['decision'] == '' and task['human_approval'] is None
    intent = task['payload']['human_cycle']['intent']
    assert intent['record_type'] == 'w3.intent_record'
    assert path.read_text().strip() == intent['intent']
    assert intent['execution']['performed'] is False
    reply = approve(callback)
    result = respond(tmp_path, path, reply, authority_context=AUTH, host_evidence='human-comment:actual-review')
    assert result['task_status'] == 'COMPLETED' and result['audit']['closed']
    receipt = json.loads((tmp_path/result['receipt']).read_text())
    decision = receipt['response']['decision_record']
    assert decision['intent_link']['intent_id'] == intent['intent_id']
    assert decision['decision'] == 'APPROVE' and decision['decided_by'] == 'BBX19'
    assert receipt['callback']['binding']['stage_index'] == 1
    saved = json.loads((tmp_path/result['audit']['orchestration_evidence']).read_text())
    assert saved['human_approval']['evidence'] == result['receipt']
    assert len([e for e in saved['evidence'] if e['actor'] == 'runtime-result']) == 2
    repeated = respond(tmp_path, path, reply, authority_context=AUTH, host_evidence='human-comment:actual-review')
    assert repeated['status'] == 'SKIPPED' and repeated['audit']['status'] == 'SKIPPED'


@pytest.mark.parametrize('decision,expected,closed', [('HOLD','WAITING_HUMAN',False),
    ('REVIEW','BLOCKED',False), ('REJECT','REJECTED',True), ('CANCEL','CANCELLED',True)])
def test_nonapproval_decisions_have_real_task_effects(monkeypatch, tmp_path, decision, expected, closed):
    path, task, callback = waiting(monkeypatch, tmp_path)
    result = respond(tmp_path, path, approve(callback, decision), authority_context=AUTH, host_evidence='human-comment:actual-review')
    assert result['task_status'] == expected and result['audit']['closed'] == closed
    state = json.loads((tmp_path/result['audit']['orchestration_evidence']).read_text())
    assert state['human_approval'] is None
    if decision == 'REVIEW':
        assert state['blocker']['kind'] == 'human_revision_requested'


def test_note_records_ack_progress_help_delivery_without_approval(monkeypatch, tmp_path):
    path, task, callback = waiting(monkeypatch, tmp_path)
    for message in ['ACKNOWLEDGE', 'PROGRESS', 'HELP', 'DELIVER']:
        note = approve(callback); note.update(kind='NOTE', decision='', message_type=message)
        result = respond(tmp_path, path, note, authority_context=AUTH, host_evidence='human-comment:note')
        assert result['task_status'] == 'WAITING_HUMAN'
        receipt = json.loads((tmp_path/result['receipt']).read_text())
        assert receipt['response']['decided_by'] is None


def test_callback_cannot_claim_authority_or_target_different_work(monkeypatch, tmp_path):
    path, task, callback = waiting(monkeypatch, tmp_path)
    for change in [{'authority_context': AUTH}, {'request_id': 'another'}, {'binding': {}}]:
        reply = {**approve(callback), **change}
        with pytest.raises(ValueError):
            respond(tmp_path,path,reply,authority_context=AUTH,host_evidence='human-comment:actual-review')
    with pytest.raises(ValueError, match='authenticated'):
        respond(tmp_path,path,approve(callback),authority_context={},host_evidence='human-comment:actual-review')
    assert json.loads((tmp_path/'repo_events/runtime_circuit/tasks'/f"{task['task_id']}.json").read_text())['human_approval'] is None


def test_tampered_report_does_not_become_approved(monkeypatch, tmp_path):
    path, task, callback = waiting(monkeypatch, tmp_path)
    artifact = next((tmp_path/'modules/LRC2/reports/log_analysis').glob('*.json'))
    report = json.loads(artifact.read_text()); report['records_total'] = 999; artifact.write_text(json.dumps(report))
    with pytest.raises(ValueError, match='postcondition'):
        respond(tmp_path,path,approve(callback),authority_context=AUTH,host_evidence='human-comment:actual-review')
    saved = json.loads((tmp_path/'repo_events/runtime_circuit/tasks'/f"{task['task_id']}.json").read_text())
    assert saved['human_approval'] is None and saved['status'] == 'WAITING_HUMAN'
    with pytest.raises(ReconciliationRequired):
        respond(tmp_path,path,approve(callback),authority_context=AUTH,host_evidence='human-comment:actual-review')


def test_old_review_cli_uses_same_decision_and_intent_records(monkeypatch, tmp_path):
    path, task, _ = waiting(monkeypatch, tmp_path)
    result = review_request(tmp_path,path,human='BBX19',evidence='human-comment:legacy')
    assert result['task_status'] == 'COMPLETED'
    receipt = json.loads((tmp_path/result['receipt']).read_text())
    assert receipt['response']['decision_record']['intent_link']['intent_id'] == task['payload']['human_cycle']['intent']['intent_id']


def test_source_change_and_blank_reply_do_not_apply(monkeypatch, tmp_path):
    path, _, callback = waiting(monkeypatch, tmp_path)
    with pytest.raises(ValueError):
        respond(tmp_path,path,callback,authority_context=AUTH,host_evidence='human-comment:actual-review')
    path.write_text(path.read_text()+'\nchanged intent\n')
    with pytest.raises(ValueError, match='source request changed'):
        respond(tmp_path,path,approve(callback),authority_context=AUTH,host_evidence='human-comment:actual-review')


def test_revised_stage_invalidates_old_callback(monkeypatch, tmp_path):
    path, task, callback = waiting(monkeypatch, tmp_path)
    runtime = make_runtime(tmp_path)
    runtime.revise_stage(task, request={'target': 'revised'}, actor='BBX19',evidence='human-comment:revise')
    with pytest.raises(ValueError, match='stale'):
        respond(tmp_path,path,approve(callback),authority_context=AUTH,host_evidence='human-comment:actual-review')


def test_save_failure_after_action_never_replays_approval(monkeypatch, tmp_path):
    path, task, callback = waiting(monkeypatch, tmp_path)
    runtime = make_runtime(tmp_path); original = runtime._save; calls = []
    def save(work):
        calls.append(work['status'])
        if work['status'] == 'COMPLETED': raise OSError('disk full')
        return original(work)
    monkeypatch.setattr(runtime, '_save', save)
    with pytest.raises(Exception):
        respond(tmp_path,path,approve(callback),authority_context=AUTH,host_evidence='human-comment:actual-review',runtime=runtime)
    with pytest.raises(ReconciliationRequired):
        respond(tmp_path,path,approve(callback),authority_context=AUTH,host_evidence='human-comment:actual-review')


def test_delegation_is_explicit():
    with pytest.raises(ValueError, match='delegation'):
        authority('BBX19','comment:1',actor='Codex')
    grant = authority('BBX19','comment:1',actor='Codex',delegation_evidence='user instruction:delegate')
    assert grant['authority_class'] == 'DELEGATED_CREATOR'
