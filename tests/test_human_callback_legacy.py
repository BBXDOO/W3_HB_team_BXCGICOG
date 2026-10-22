import json
import pytest

from tests.test_runtime_circuit_intake import configure
from tests.test_human_callback import approve, AUTH
from tools import request_cycle as rc
from tools.human_callback import respond


def document_request(root):
    (root/'BBX19/notes').mkdir(parents=True)
    (root/'BBX19/notes/README.md').write_text('# Notes\n')
    (root/'requests').mkdir()
    path=root/'requests/RQ-DOC-CALLBACK.md'
    path.write_text('---\nrequest_id: RQ-DOC-CALLBACK\nrequest_type: document_creation\n'
                    'task_keyword: governance\ntarget_module: Copilot-Gm\nrequester: BBX19\n'
                    'document_kind: thai_markdown_guide\nartifact_path: BBX19/notes/THAI_MARKDOWN_GUIDE.md\n'
                    'final_signoff_required: true\n---\n# Create the Thai Markdown guide\n')
    return path


def test_existing_document_result_joins_same_callback_without_rewriting_artifact(monkeypatch,tmp_path):
    configure(monkeypatch,tmp_path);path=document_request(tmp_path)
    initial=rc.process(path)
    assert initial['runtime_result']['status']=='WAITING_HUMAN'
    artifact=tmp_path/initial['artifact_path']; original=artifact.read_bytes()
    prepared=respond(tmp_path,path,prepare_only=True)
    form=json.loads((tmp_path/prepared['callback_path']).read_text())
    result=respond(tmp_path,path,approve(form),authority_context=AUTH,host_evidence='human:document-review')
    assert result['task_status']=='COMPLETED' and result['audit']['closed']
    assert artifact.read_bytes()==original
    assert len(list((tmp_path/'repo_events/runtime_circuit').glob('*/adopted-root-result-*.json')))==1
    assert rc.process(path)['status']=='SKIPPED'


def test_legacy_unfinished_human_request_can_be_answered_but_not_falsely_closed(monkeypatch,tmp_path):
    configure(monkeypatch,tmp_path)
    (tmp_path/'requests').mkdir();path=tmp_path/'requests/RQ-VISION-CALLBACK.md'
    path.write_text('---\nrequest_id: RQ-VISION-CALLBACK\nrequest_type: brainstorm\n'
        'task_keyword: vision\ntarget_module: BBX19\nrequester: BBX19\nfinal_signoff_required: true\n---\n# Need an actual inventory report\n')
    initial=rc.process(path)
    assert initial['runtime_result']['status']=='REVIEW_REQUIRED'
    prepared=respond(tmp_path,path,prepare_only=True)
    callback=json.loads((tmp_path/prepared['callback_path']).read_text())
    note=approve(callback);note.update(kind='NOTE',decision='',message_type='ACKNOWLEDGE')
    result=respond(tmp_path,path,note,authority_context=AUTH,host_evidence='human:ack')
    assert result['task_status']=='WAITING_HUMAN' and not result['audit']['closed']
    with pytest.raises(ValueError,match='unresolved'):
        respond(tmp_path,path,approve(callback),authority_context=AUTH,host_evidence='human:review')
