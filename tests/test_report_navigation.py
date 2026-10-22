import json
from pathlib import Path

from tests.test_runtime_circuit_intake import configure, request
from tests.test_human_callback import approve, AUTH
from tools import request_cycle as rc
from tools.human_callback import respond
from tools.report_navigation import discussion_url, relative


def test_report_has_response_links_without_mutating_lrc2_artifact(monkeypatch,tmp_path):
    configure(monkeypatch,tmp_path);path=request(tmp_path)
    path.write_text(path.read_text().replace('requester: BBX19','requester: BBX19\ndiscussion_url: https://github.com/BBXDOO/W3_HB_team_BXCGICOG/pull/297'))
    result=rc.process(path)
    report=tmp_path/result['report_path'];text=report.read_text()
    assert 'เปิดฟอร์มตอบรายงานนี้' in text
    assert '../../BBEX-Core/private/callback/responses/' in text
    assert 'https://github.com/BBXDOO/W3_HB_team_BXCGICOG/pull/297' in text
    assert 'คอมเมนต์อย่างเดียวยังไม่บันทึกคำตัดสิน' in text
    artifact=tmp_path/result['artifact_paths'][0]['path'];original=artifact.read_bytes()
    assert rc.process(path)['status']=='SKIPPED'
    assert artifact.read_bytes()==original
    event=tmp_path/'repo_events/RQ-REAL-ANALYSIS_EXECUTION.md'
    assert event.read_text().count('<!-- w3-human-response-links -->')==1
    assert 'เปิดฟอร์มตอบรายงานนี้' in event.read_text()
    callback=json.loads((tmp_path/result['callback_path']).read_text())
    done=respond(tmp_path,path,approve(callback),authority_context=AUTH,host_evidence='human:review')
    assert done['task_status']=='COMPLETED'
    text=report.read_text()
    assert 'ไม่ต้องตรวจรับซ้ำ' in text and 'เปิดฟอร์มตอบรายงานนี้' not in text
    assert artifact.read_bytes()==original


def test_no_related_pr_is_guessed_and_unsafe_links_are_ignored(monkeypatch,tmp_path):
    configure(monkeypatch,tmp_path);path=request(tmp_path)
    result=rc.process(path)
    text=(tmp_path/result['report_path']).read_text()
    assert '/pull/' not in text
    assert discussion_url('javascript:alert(1)') is None
    assert discussion_url('https://github.com/a/b/pull/1) bad') is None


def test_channel_can_be_added_later_without_changing_request_or_replaying(monkeypatch,tmp_path):
    configure(monkeypatch,tmp_path);path=request(tmp_path)
    result=rc.process(path);original=path.read_bytes()
    config=tmp_path/'BBEX-Core/private/callback/channels.json'
    config.write_text(json.dumps({'RQ-REAL-ANALYSIS':{'discussion_url':'https://github.com/a/b/pull/42'}}))
    assert rc.process(path)['status']=='SKIPPED'
    assert path.read_bytes()==original
    assert 'https://github.com/a/b/pull/42' in (tmp_path/result['report_path']).read_text()
    config.write_text('{}')
    assert rc.process(path)['status']=='SKIPPED'
    assert 'https://github.com/a/b/pull/42' not in (tmp_path/result['report_path']).read_text()
