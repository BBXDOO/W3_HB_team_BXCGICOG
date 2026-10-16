"""Read-only tool used by Orchestration to inspect actual Origin work evidence.

AM:III; derived from workflows/orchestration/README.md and Origin role contracts.
The tool diagnoses work and verifies final file states; it never grants repair
rights, changes owner output, or marks failed owner work as successful.
"""
from __future__ import annotations

import json
from pathlib import Path

from core.runtime.agents.origin_operations import OriginFiles, atomic_write, digest
from tools.check_portable_paths import path_problems
from tools.validate_metadata import validate_file
from tools.validate_modules import ModuleValidator


def inspect_origin_work(root, module, result, report_path, *, authority=None):
    root = Path(root).resolve()
    report_path = Path(report_path).resolve()
    allowed = (root / 'repo_events/origin_agents' / module / 'collaboration').resolve()
    if not allowed.is_relative_to(root) or not report_path.is_relative_to(allowed):
        raise ValueError('Support report must remain in Origin collaboration space')
    findings, checks, tools_used = [], [], []
    receipt = (root / result['log_path']).resolve()
    log_root = (root / 'repo_events/origin_agents' / module / 'logs').resolve()
    try:
        if not log_root.is_relative_to(root) or not receipt.is_relative_to(log_root):
            raise ValueError('Owner receipt outside module log space')
        data = receipt.read_bytes()
        recorded = json.loads(data)
        if recorded.get('module') != module or recorded.get('status') != result.get('status'):
            raise ValueError('Owner receipt identity/status mismatch')
        checks.append({'check': 'owner_receipt', 'path': result['log_path'],
                       'state': 'EVIDENCED', 'sha256': digest(data)})
    except (OSError, ValueError, TypeError) as exc:
        recorded = {}
        findings.append({'kind': 'invalid_owner_receipt', 'path': result['log_path'], 'reason': str(exc)})
    try:
        fs = OriginFiles(module, authority or {'repo_root': str(root)})
        expected = {}
        for operation in recorded.get('operations', []):
            action, path = operation['action'], operation['path']
            if action in {'read', 'copy'} and operation.get('sha256'):
                expected[path] = operation['sha256']
            if action in {'create', 'write', 'append', 'edit'} and operation.get('sha256'):
                expected[path] = operation['sha256']
            if action in {'copy', 'move'} and operation.get('destination'):
                expected[operation['destination']] = operation.get('sha256')
            if action in {'delete', 'move'} and operation.get('mutated'):
                expected[path] = None
        for item in recorded.get('evidence', []):
            if item.get('sha256'):
                expected[item['path']] = item['sha256']
        for value, expected_hash in expected.items():
            try:
                path = fs.path(value)
                fs.require(path, 'read')
                portability = path_problems(value)
                tools_used.append({'tool': 'tools/check_portable_paths.py', 'function': 'path_problems',
                                   'path': value, 'purpose': 'inspect output path portability'})
                checks.append({'check': 'portable_path', 'path': value,
                               'state': 'REVIEW' if portability else 'EVIDENCED', 'notes': portability})
                if expected_hash is not None and path.is_file():
                    errors = []
                    if path.name == 'module.json':
                        _, errors = ModuleValidator(root).validate_module(path)
                        tools_used.append({'tool': 'tools/validate_modules.py', 'function': 'validate_module',
                                           'path': value, 'purpose': 'validate module definition'})
                    elif path.suffix == '.md':
                        errors = validate_file(str(path))
                        tools_used.append({'tool': 'tools/validate_metadata.py', 'function': 'validate_file',
                                           'path': value, 'purpose': 'check approval metadata'})
                    for error in errors:
                        findings.append({'kind': 'repository_tool_finding', 'path': value, 'reason': error})
                if expected_hash is None:
                    matched = not path.exists()
                    actual = None
                else:
                    actual = digest(path.read_bytes())
                    matched = actual == expected_hash
                checks.append({'check': 'final_file_state', 'path': value,
                               'state': 'EVIDENCED' if matched else 'DEFECT',
                               'expected_sha256': expected_hash, 'actual_sha256': actual})
                if not matched:
                    findings.append({'kind': 'output_evidence_mismatch', 'path': value})
            except (OSError, ValueError, PermissionError) as exc:
                findings.append({'kind': 'output_verification_unavailable', 'path': value, 'reason': str(exc)})
    except (OSError, ValueError, KeyError, TypeError) as exc:
        findings.append({'kind': 'support_context_unavailable', 'path': 'core/identity/profiles/' + module + '.idp.json', 'reason': str(exc)})
    owner_completed = result.get('status') == 'COMPLETED'
    payload = {'tool': 'W3 repository tools support', 'owner': module,
               'owner_status': result.get('status'), 'owner_log': result['log_path'],
               'checks': checks, 'findings': findings, 'tools_used': tools_used, 'owner_reason': result.get('reason'),
               'resolved': owner_completed and not findings,
               'next_steps': [] if owner_completed and not findings else [
                   'Inspect the recorded owner error and affected paths.',
                   'Return corrected work to the Origin owner; repairs from review require BBX19 selection.'],
               'source_mutated': False,
               'unknowns': ['Checks verify recorded file outcomes, not all role semantics or external systems.']}
    atomic_write(report_path, (json.dumps(payload, ensure_ascii=False, indent=2) + '\n').encode())
    return {'resolved': payload['resolved'], 'evidence': str(report_path.relative_to(root)),
            'diagnostics': payload}
