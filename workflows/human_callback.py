"""One evidence-bound human response: BBEX intent -> BBX19 decision -> runtime.

The calling host authenticates the human. JSON callback data never supplies
trusted authority. Callers serialize the full operation with the request lock.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from core.runtime.agents.bbex_core import BBEXCore
from core.runtime.agents.bbx19 import BBX19Agent
from core.runtime.agents.origin_operations import atomic_write
from workflows import orchestration as orc
from workflows.runtime_circuit import ReconciliationRequired

BASE = 'BBEX-Core/private/callback'
DECISIONS = {'APPROVE', 'REJECT', 'HOLD', 'REVIEW', 'CANCEL'}
MESSAGES = {'ACKNOWLEDGE', 'PROGRESS', 'HELP', 'DELIVER'}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def inside(root, value):
    path = (Path(root).resolve() / value).resolve()
    if not path.is_relative_to(Path(root).resolve()):
        raise ValueError('callback path escapes repository')
    return path


def ensure_intent(runtime, task, request, *, persist=True):
    cycle = task['payload'].get('human_cycle')
    if cycle is not None:
        if not isinstance(cycle, dict) or cycle.get('intent', {}).get('record_type') != 'w3.intent_record':
            raise ValueError('invalid saved human intent cycle')
        return cycle
    original = request['_request_text']
    # Outcome is either explicitly provided or the declared request's stage
    # verification contract. Preserve its provenance rather than invent content.
    outcome = request.get('desired_outcome') or 'ผลตามคำร้องต้นทาง ผ่านการตรวจผลของแต่ละขั้น และเงื่อนไขตรวจรับที่ระบุ'
    intent = BBEXCore(runtime.reference_root or runtime.directory).capture(
        str(task.get('source_id') or task['task_id']), source=str(request.get('requester') or task['origin']['module']),
        intent=original, desired_outcome=str(outcome),
        evidence=[request['_request_file']],
        observations=['Outcome basis: explicit desired_outcome' if request.get('desired_outcome')
                      else 'Outcome basis: source request and declared stage verification contract'],
    )
    task['payload']['human_cycle'] = {'version': 1, 'intent': intent, 'callbacks': {}}
    if persist:
        runtime._save(task)
    return task['payload']['human_cycle']


def binding(runtime, task):
    state = runtime._state(task)
    result = runtime._read_evidence(state['result_ref']) if state['result_ref'] else None
    return {'task_id': task['task_id'], 'request_sha256': task['payload']['request_sha256'],
            'stage_index': state['index'],
            'stage_sha256': digest(state['effective_stage'] or state['stages'][state['index']]),
            'result_sha256': digest(result),
            'intent_id': task['payload']['human_cycle']['intent']['intent_id']}


def prepare(runtime, task, request):
    """Save an editable response linked to the exact stage/result, no approval."""
    cycle = ensure_intent(runtime, task, request)
    if task['status'] not in {'WAITING_HUMAN', 'BLOCKED'}:
        return None
    bound = binding(runtime, task)
    name = f"{BASE}/responses/{task['task_id']}-{digest(bound)[:12]}.json"
    path = inside(runtime.reference_root, name)
    if not path.exists():
        response = {'schema': 'w3.human_callback/1', 'request_id': task.get('source_id'),
                    'binding': bound, 'kind': 'DECISION', 'decision': '',
                    'reason': '', 'annotations': [], 'evidence': []}
        atomic_write(path, (json.dumps(response, ensure_ascii=False, indent=2)+'\n').encode())
    if cycle.get('response_path') != name:
        cycle['response_path'] = name
        runtime._save(task)
    return name


def _authority(authority):
    if (not isinstance(authority, dict) or authority.get('authority') != 'BBX19'
            or authority.get('authority_class') not in {'CREATOR_ORIGIN', 'DELEGATED_CREATOR'}
            or authority.get('verified') is not True or not authority.get('verified_by')):
        raise ValueError('authenticated host authority required, not callback-supplied identity')
    if authority['authority_class'] == 'DELEGATED_CREATOR' and not authority.get('delegation_evidence'):
        raise ValueError('delegated authority requires delegation evidence')


def apply(runtime, task, callback, *, authority_context, host_evidence, checkpoint=None):
    """Apply a response once; ambiguous interrupted work requires reconciliation."""
    _authority(authority_context)
    if not isinstance(host_evidence, str) or not host_evidence.strip():
        raise ValueError('host decision provenance required')
    if not isinstance(callback, dict) or callback.get('schema') != 'w3.human_callback/1':
        raise ValueError('invalid callback schema')
    allowed = {'schema', 'request_id', 'binding', 'kind', 'decision', 'message_type',
               'reason', 'annotations', 'evidence', 'override_intent_review'}
    if set(callback) - allowed:
        raise ValueError('unknown callback fields; authority and executable commands belong to host')
    if callback.get('request_id') != task.get('source_id'):
        raise ValueError('callback belongs to another request')
    cycle = task['payload'].get('human_cycle')
    if not cycle:
        raise ValueError('prepare the saved intent and callback first')
    key = digest(callback)
    previous = cycle['callbacks'].get(key)
    if previous:
        if previous['state'] == 'APPLIED':
            return {'status': 'SKIPPED', 'task_status': task['status'], 'receipt': previous['receipt']}
        if previous['state'] != 'NOT_APPLIED':
            raise ReconciliationRequired('callback was already attempted; inspect its receipt before another action', result=previous)
    runtime._ready(task)
    if any(item.get('state') == 'PENDING' for item in cycle['callbacks'].values()):
        raise ReconciliationRequired('an earlier callback needs reconciliation')
    if callback.get('binding') != binding(runtime, task):
        raise ValueError('stale callback: request, intent, stage or result changed')
    if task['status'] not in {'WAITING_HUMAN', 'BLOCKED'}:
        raise ValueError('callback requires a waiting or blocked task')
    if (not isinstance(callback.get('reason'), str) or not callback['reason'].strip()
            or not isinstance(callback.get('annotations'), list) or not callback['annotations']
            or any(not isinstance(v, str) or not v.strip() for v in callback['annotations'])
            or not isinstance(callback.get('evidence'), list)
            or any(not isinstance(v, str) or not v.strip() for v in callback['evidence'])):
        raise ValueError('reason, annotations and a list of evidence references required')
    kind = callback.get('kind')
    decision = callback.get('decision')
    if kind == 'DECISION':
        if decision not in DECISIONS:
            raise ValueError('unknown decision')
        if decision == 'APPROVE' and task['status'] != 'WAITING_HUMAN':
            raise ValueError('only a human review gate may be approved')
        response = BBX19Agent().execute(str(task.get('source_id')), {}, {
            'source': 'BBX19', 'request_boundary': 'UNTRUSTED_INPUT',
            'target': f"{task['task_id']}:stage:{task['runtime_circuit']['index']}",
            'authority_context': deepcopy(authority_context),
            'payload': {'decision': decision, 'reason': callback['reason'],
                        'annotations': callback['annotations'],
                        'evidence': callback['evidence'] + [host_evidence],
                        'intent_record': cycle['intent'],
                        'override_intent_review': callback.get('override_intent_review') is True}})
        if response['status'] != 'COMPLETED':
            raise ValueError(response['reason'])
    elif kind == 'NOTE' and callback.get('message_type') in MESSAGES:
        if decision:
            raise ValueError('a note cannot also grant a decision')
        response = {'record_type': 'w3.human_note', 'message_type': callback['message_type'],
                    'reason': callback['reason'], 'annotations': callback['annotations'],
                    'evidence': callback['evidence'] + [host_evidence], 'decided_by': None}
    else:
        raise ValueError('unknown response kind or message type')
    receipt = {'schema': 'w3.callback_receipt/1', 'callback_id': key, 'callback': deepcopy(callback),
               'authority': deepcopy(authority_context), 'host_evidence': host_evidence,
               'intent_id': cycle['intent']['intent_id'], 'response': response,
               'before_status': task['status'], 'recorded_at': orc.timestamp()}
    ref = runtime._evidence(task, 'human-callback', receipt)
    cycle['callbacks'][key] = {'state': 'PENDING', 'receipt': ref}
    runtime._save(task)  # durable command receipt before any state transition
    if checkpoint is not None:
        checkpoint()  # remote host persists PENDING before downstream effects
    try:
        if kind == 'DECISION' and decision == 'APPROVE':
            state = runtime._state(task)
            runtime.review_stage(task, state['stages'][state['index']], human='BBX19', evidence=ref)
            runtime.continue_work(task)
        elif kind == 'DECISION' and decision in {'REJECT', 'CANCEL'}:
            orc.advance(task, 'REJECTED' if decision == 'REJECT' else 'CANCELLED',
                        actor='BBX19', detail=callback['reason'], evidence=ref)
        else:
            if kind == 'DECISION' and decision == 'REVIEW':
                task['blocker'] = {'kind': 'human_revision_requested', 'reason': callback['reason'], 'evidence': ref}
                task['human_approval'] = None
                if task['status'] == 'WAITING_HUMAN':
                    orc.advance(task, 'BLOCKED', actor='BBX19', detail='human requested changes', evidence=ref)
            cycle.setdefault('observations', []).append({
                'at': orc.timestamp(), 'kind': kind, 'message_type': callback.get('message_type'),
                'decision': decision, 'text': callback['reason'], 'evidence': ref})
            task['history'].append({'at': orc.timestamp(), 'event': decision if kind == 'DECISION' else callback['message_type'],
                                    'actor': 'BBX19', 'detail': callback['reason']})
        task['evidence'].append({'at': orc.timestamp(), 'actor': 'human-callback', 'ref': ref})
        cycle['callbacks'][key].update(state='APPLIED', after_status=task['status'])
        task['mutated'] = True
        runtime._save(task)
    except Exception:
        # Do not replay a partially applied human action or downstream executor.
        task['runtime_circuit']['callback_reconciliation_required'] = True
        cycle['callbacks'][key]['state'] = 'PENDING'
        try:
            runtime._save(task)
        except Exception:
            pass
        raise
    return {'status': 'APPLIED', 'task_status': task['status'], 'receipt': ref}


def reconcile_callback(runtime, task, callback_id, *, outcome, authority_context, host_evidence):
    """Host records observed effects; never manufacture a completed task."""
    _authority(authority_context)
    if outcome not in {'APPLIED', 'NOT_APPLIED'} or not isinstance(host_evidence, str) or not host_evidence.strip():
        raise ValueError('observed outcome and reconciliation evidence required')
    entry = task['payload'].get('human_cycle', {}).get('callbacks', {}).get(callback_id)
    if not entry or entry['state'] != 'PENDING':
        raise ValueError('pending callback required')
    receipt = runtime._read_evidence(entry['receipt'])
    if outcome == 'NOT_APPLIED' and (task['status'] != receipt['before_status'] or
            (task.get('human_approval') or {}).get('evidence') == entry['receipt']):
        raise ValueError('task already advanced; reconcile actual task effects before declaring not applied')
    if outcome == 'APPLIED' and receipt['callback'].get('decision') == 'APPROVE' and (
            task.get('human_approval') or {}).get('evidence') != entry['receipt']:
        raise ValueError('approval evidence has not been recorded in task')
    ref = runtime._evidence(task, 'callback-reconciliation', {
        'callback_id': callback_id, 'outcome': outcome, 'evidence': host_evidence,
        'authority': authority_context, 'observed_task_status': task['status']})
    state = task['runtime_circuit']
    # Older receipts used the runtime flag for callback-only persistence failures.
    # Migrate only states where no runtime execution/support is in flight.
    if (state.get('reconciliation_required') and not state.get('callback_reconciliation_required')
            and task['status'] in {'WAITING_HUMAN', 'COMPLETED', 'REJECTED', 'CANCELLED'}
            and not state.get('pending_support')):
        state['reconciliation_required'] = False
    state['callback_reconciliation_required'] = False
    entry.update(state=outcome, reconciliation=ref)
    task['evidence'].append({'at': orc.timestamp(), 'actor': 'callback-reconciliation', 'ref': ref})
    task['history'].append({'at': orc.timestamp(), 'actor': 'BBX19', 'event': 'CALLBACK_RECONCILED', 'detail': outcome})
    runtime._save(task)
    return {'status': outcome, 'task_status': task['status'], 'receipt': ref}
