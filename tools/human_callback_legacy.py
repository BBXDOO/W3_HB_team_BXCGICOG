"""Adopt existing root result receipts into the same human response circuit.

No owner executor is invoked and no source request/result receipt is rewritten
by adoption. Document results are reverified against the actual file.
"""
import hashlib
import json

from workflows import orchestration as orc
from workflows.runtime_circuit import WorkflowRuntime
from tools.runtime_circuit_intake import task_id


def adopt(root, request, runtime):
    from tools.request_cycle import safe_id
    snapshot = runtime.directory/'tasks'/f"{task_id(str(request['request_id']))}.json"
    if snapshot.exists():
        return json.loads(snapshot.read_text())
    path = root/'requests/results'/f"{safe_id(str(request['request_id']))}_RESULT.json"
    raw = path.read_bytes(); envelope = json.loads(raw)
    result = envelope['runtime_result']
    if result.get('status') in {'COMPLETED', 'REJECTED', 'CANCELLED'}:
        raise ValueError('legacy request is already terminal; keep its historical receipt')
    task = orc.new_task(task_id(str(request['request_id'])), 'REQUEST', 'NORMAL',
        {'module': str(request.get('requester') or 'requests/'), 'tier': 0},
        {'source_request': request['_request_file'], 'request_sha256': hashlib.sha256(request['_request_text'].encode()).hexdigest(),
         'adopted_legacy': {'source_result_path': str(path.relative_to(root)),
                            'source_result_sha256': hashlib.sha256(raw).hexdigest(), 'original_status': result.get('status')}},
        source_id=str(request['request_id']), human_review_required=True)
    stage = WorkflowRuntime._stage({'task': str(request['task_keyword']), 'request': {'request_text': request['_request_text']}})
    runtime._prepare(task, [stage], review_policy='final')
    source_ref = runtime._evidence(task, 'adopted-root-result', envelope)
    observed = {**result, 'result_validation': result.get('result_validation', {'status': 'review_required'})}
    if request.get('request_type') == 'document_creation' and result.get('gemini_result', {}).get('status') == 'COMPLETED':
        # These are existing allocation/verification receipts, not a new action.
        observed = {'status': 'COMPLETED', 'result_validation': {'status': 'valid'},
                    'agent_result': {'module': stage['module'], 'capability': 'adopted_document_result',
                        'artifact_path': result['artifact_path'], 'artifact_sha256': result['artifact_sha256'],
                        'source_receipt': source_ref, 'status': 'COMPLETED', 'mutated': result.get('mutated', False)},
                    'artifacts': result.get('artifacts', [])}
    observed_ref = runtime._evidence(task, 'result', observed)
    state = task['runtime_circuit']; state.update(effective_stage=stage, result_ref=observed_ref)
    task['evidence'].append({'at': orc.timestamp(), 'actor': 'runtime-result', 'ref': observed_ref})
    orc.advance(task, 'INSPECTING', actor='Orchestration', detail='adopt existing root result; no executor replay')
    orc.advance(task, 'QUEUED', actor='Orchestration', detail='bind existing owner receipt')
    orc.route(task, {'module':stage['module'],'task':stage['task']}, actor='Orchestration',
              notify=lambda _: {'delivered': True, 'evidence': source_ref})
    orc.advance(task, 'ACKNOWLEDGED', actor='local-receipt-import', detail='existing receipt read; no new module acknowledgement', evidence=source_ref)
    orc.advance(task, 'IN_PROGRESS', actor='local-receipt-import', detail='inspect recorded outcome')
    if result.get('status') == 'BLOCKED':
        task['blocker'] = {'reason': result.get('output') or result.get('reason') or 'legacy work remains blocked'}
        orc.advance(task, 'BLOCKED', actor='Orchestration', detail='preserve existing blocker', evidence=source_ref)
    else:
        orc.advance(task, 'VERIFYING', actor='local-receipt-import', detail='existing result awaits substantive verification', evidence=source_ref)
        orc.advance(task, 'WAITING_HUMAN', actor='Orchestration', detail='existing human gate moved to unified response', evidence=source_ref)
    task['mutated'] = result.get('mutated') is True
    runtime._save(task)
    return task
