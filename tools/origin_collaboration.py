"""Origin partner work and structural reports using Orchestration and IGET."""
from __future__ import annotations

import json
import uuid
from pathlib import Path

from core.runtime.agents import get_agent
from core.runtime.agents.origin_operations import OriginFiles, atomic_write, digest
from iget.structure_review import inspect_structure, finding_id
from workflows import orchestration as orc
from tools.origin_support import inspect_origin_work


def collaborate(root, module, result, *, partner=None, structural=False, authority_context=None):
    root = Path(root).resolve()
    task = orc.new_task('W3-ORC-20261011-' + str(uuid.uuid4().int), 'REPORT', 'NORMAL',
                        {'module': module, 'tier': 1}, {'owner_log': result['log_path']},
                        source_id=result['log_path'])
    orc.advance(task, 'INSPECTING', actor='Orchestration', detail='inspect Origin work receipt')
    orc.advance(task, 'QUEUED', actor='Orchestration', detail='select partner')
    partner_result = None
    if partner and partner != module:
        try:
            partner_result = get_agent(partner).execute('Origin partner review', {},
                {'request_type': 'origin_review', 'review_paths': [result['log_path']],
                 'authority_context': {'repo_root': str(root), 'origin_scopes': {
                     partner: [{'path': result['log_path'], 'operations': ['read']}]}}})
        except (ValueError, KeyError, OSError) as exc:
            partner_result = {'status': 'FAILED', 'reason': str(exc)}
    active_partner = partner if partner_result and partner_result.get('status') == 'COMPLETED' else 'Orchestration'
    folder = root / 'repo_events/origin_agents' / module / 'collaboration'
    if not folder.resolve().is_relative_to(root):
        raise ValueError('Collaboration directory escapes repository')
    receipt = folder / (task['task_id'] + '-partner.json')
    record = {'owner': module, 'partner': active_partner, 'requested_partner': partner,
              'partner_result': partner_result, 'owner_log': result['log_path'],
              'owner_log_exists': (root / result['log_path']).is_file()}
    atomic_write(receipt, (json.dumps(record, ensure_ascii=False, indent=2) + '\n').encode())
    ref = str(receipt.relative_to(root))
    # Delivery is a repository handoff receipt, not an external chatbot notification.
    orc.route(task, {'module': active_partner}, actor='Orchestration',
              notify=lambda _: {'delivered': True, 'evidence': ref})
    orc.advance(task, 'ACKNOWLEDGED', actor=active_partner, detail='repository receipt inspected', evidence=ref)
    orc.advance(task, 'IN_PROGRESS', actor=active_partner, detail='inspect evidence and unresolved work')
    findings = list(result.get('findings', []))
    support = None
    if active_partner == 'Orchestration' or result.get('status') != 'COMPLETED':
        task['blocker'] = {'kind': 'partner_unavailable' if result.get('status') == 'COMPLETED' else 'owner_work_incomplete',
                           'owner_log': result['log_path'], 'reason': result.get('reason')}
        orc.advance(task, 'BLOCKED', actor='Orchestration', detail=task['blocker']['kind'])
        support_report = folder / (task['task_id'] + '-support.json')
        orc.assist(task, kind='TOOL', name='W3 repository tools support', actor='Orchestration',
                   handler=lambda _: inspect_origin_work(root, module, result, support_report, authority=authority_context))
        if task['support']:
            support = task['support'][-1]['result']
            findings += support.get('diagnostics', {}).get('findings', [])
        if task['status'] == 'RETURNED':
            orc.advance(task, 'IN_PROGRESS', actor=module, detail='support evidence returned to owner',
                        evidence=support['evidence'])
    audit = None
    if structural:
        fs = OriginFiles(module, {'repo_root': str(root)})
        paths = fs.profile.get('file_capabilities', {}).get('review_paths', [])
        audit = inspect_structure(root, paths)
        findings += audit['findings']
        # Unknown runtime coverage is carried separately, never manufactured as a defect.
    if not record['owner_log_exists']:
        findings.append({'kind': 'missing_owner_receipt', 'path': result['log_path']})
    findings = list({finding_id(item): {**item, 'finding_id': finding_id(item)} for item in findings}.values())
    report = folder / (task['task_id'] + '-review.json')
    payload = {'owner': module, 'partner': active_partner, 'participants': [module, active_partner, 'Orchestration'] + (['IGET'] if structural else []),
               'owner_log': result['log_path'], 'partner_receipt': ref, 'iget': audit,
               'findings': findings, 'structural': structural,
               'unknowns': audit['unknowns'] if audit else [],
               'checks': audit['checks'] if audit else [],
               'signal': audit['signal'] if audit else None,
               'repair_status': 'WAITING_BBX19_SELECTION' if findings else 'NO_REPAIR_PROPOSED',
               'source_mutated': False, 'support': support,
               'support_status': task['status'] if support is not None or task.get('blocker') else 'NOT_REQUIRED'}
    atomic_write(report, (json.dumps(payload, ensure_ascii=False, indent=2) + '\n').encode())
    report_ref = str(report.relative_to(root))
    if task['status'] != 'BLOCKED':
        orc.advance(task, 'VERIFYING', actor='Orchestration', detail='review report persisted', evidence=report_ref)
        orc.advance(task, 'COMPLETED', actor='Orchestration', detail='report delivered; repairs remain separate')
    snapshot = orc.save(task, folder)
    return {'partner': active_partner, 'collaboration_report': report_ref,
            'orchestration_evidence': str(snapshot.relative_to(root)), 'structure_findings': findings,
            'structural_review': structural, 'repair_status': payload['repair_status'],
            'review_unknowns': payload['unknowns'], 'review_checks': payload['checks'],
            'review_signal': payload['signal'],
            'checked_paths': audit['checked_paths'] if audit else [],
            'support_pending': task['status'] == 'BLOCKED',
            'support_evidence': support['evidence'] if support else None}


def validate_repair_selection(root, module, request):
    """A BBX19 selection is admitted only by the owner intake or repo request."""
    if request.get('source') != 'BBX19':
        raise ValueError('Structural repair requires BBX19 selection')
    selection = request.get('payload', {}).get('repair_selection', {})
    fs = OriginFiles(module, {'repo_root': str(root)})
    report_path = fs.path(selection.get('report_path', ''))
    expected_root = (Path(root) / 'repo_events/origin_agents' / module / 'collaboration').resolve()
    if not report_path.is_relative_to(expected_root) or digest(report_path.read_bytes()) != selection.get('report_sha256'):
        raise ValueError('Structural repair report is missing or changed')
    report = json.loads(report_path.read_text())
    selected = set(selection.get('paths', []))
    proposed = {item['path'] for item in report.get('findings', []) if 'path' in item}
    if not selected or not selected <= proposed:
        raise ValueError('BBX19 must select reported paths')
    for operation in request['payload'].get('operations', []):
        for key in ('path', 'destination'):
            if key in operation and operation[key] not in selected:
                raise ValueError('Operation exceeds BBX19 selected repair paths')
    return [{'path': path, 'operations': ['read', 'list', 'create', 'write', 'append', 'edit', 'delete', 'copy', 'move']}
            for path in sorted(selected)]
