"""AM:III structural observations, derived from IGET 0.5 and signal guidance.

References: iget/README.md, iget/docs/SIGNAL_SYSTEM.md, docs/governance/AMS.md.
The PR scorer is unchanged; this surface reuses ProofTracer for local evidence.
"""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

from .proof import ProofTracer


def finding_id(item):
    """Stable across rounds and changes to explanatory text."""
    key = [item.get('kind'), item.get('path'), item.get('check')]
    return 'IGET-' + hashlib.sha256(json.dumps(key, sort_keys=True).encode()).hexdigest()[:16]


def inspect_structure(root, paths):
    root = Path(root).resolve()
    tracer = ProofTracer()
    paths = list(dict.fromkeys(paths))
    tracer.record('structure_scope', 'Inspect declared paths without executing source', paths, 'iget:scope')
    evidence, findings, calls, definitions, checked = [], [], set(), [], []
    seen = set()
    for value in paths:
        raw = Path(value)
        path = (root / raw).resolve()
        if raw.is_absolute() or '..' in raw.parts or not path.is_relative_to(root) or '.git' in raw.parts:
            raise ValueError('Review path escapes repository or enters Git internals')
        if not path.exists():
            checked.append(value)
            findings.append({'kind': 'missing_path', 'path': value})
            continue
        files = [path] if path.is_file() else sorted(path.rglob('*'))
        # An existing empty directory is still an observed path.
        checked.append(value)
        for file in files:
            if any(part in {'.git', 'node_modules', '__pycache__', '.venv'} for part in file.relative_to(root).parts):
                continue
            reference = str(file.relative_to(root))
            if reference in seen:
                continue
            seen.add(reference)
            if not file.resolve().is_relative_to(root):
                findings.append({'kind': 'outside_scope_link', 'path': reference})
                checked.append(reference)
                continue
            if not file.is_file():
                continue
            checked.append(reference)
            try:
                data = file.read_bytes()
            except OSError as exc:
                findings.append({'kind': 'unreadable_file', 'path': reference, 'reason': str(exc)})
                continue
            evidence.append({'path': reference, 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)})
            try:
                if file.suffix == '.json':
                    json.loads(data)
                if file.suffix != '.py':
                    continue
                tree = ast.parse(data, filename=reference)
            except (SyntaxError, UnicodeError, ValueError) as exc:
                findings.append({'kind': 'invalid_syntax', 'path': reference, 'reason': str(exc)})
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    name = node.func.id if isinstance(node.func, ast.Name) else getattr(node.func, 'attr', '')
                    calls.add(name)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    definitions.append({'path': reference, 'name': node.name, 'line': node.lineno})
    findings = [{**item, 'finding_id': finding_id(item)} for item in findings]
    tracer.record('structure_observed', 'Read bytes and record static checks',
                  {'files': len(evidence), 'checked_paths': checked}, 'iget:observation')
    tracer.record('structure_findings', 'Observed defects within declared scope', findings, 'iget:findings')
    unknowns = ['Static inventory does not prove an end-to-end execution or a missing dynamic caller.']
    tracer.record('structure_limits', 'Runtime circuit remains unverified by static inspection', unknowns, 'iget:unknown')
    return {'module': 'IGET', 'status': 'REVIEW_REQUIRED' if findings else 'COMPLETED',
            'findings': findings, 'evidence': evidence, 'definitions': definitions,
            'checked_paths': sorted(set(checked)), 'call_names': sorted(calls),
            'coverage': 'declared paths, bytes, Python/JSON syntax and static call inventory',
            'unknowns': unknowns, 'checks': [
                {'check': 'declared_files', 'state': 'DEFECT' if findings else 'EVIDENCED'},
                {'check': 'runtime_circuit', 'state': 'UNVERIFIED', 'reason': unknowns[0]}],
            'signal': {'color': 'yellow', 'reason': 'defects_require_review' if findings else 'static_checks_only_runtime_unverified'},
            'proof': tracer.to_mpcp_result(), 'source_mutated': False}


def reconcile_findings(previous, current, checked_paths, at):
    """Keep one identity per defect; resolve only when its path was rechecked.

    'circuit_verification_required' was a synthetic limitation, not a defect.
    Migrate it out of the defect ledger; reports continue to expose that limit.
    """
    records = {item.get('finding_id') or finding_id(item): dict(item) for item in previous
               if item.get('kind') != 'circuit_verification_required'}
    observed = {finding_id(item): item for item in current
                if item.get('kind') != 'circuit_verification_required'}
    for key, item in observed.items():
        old = records.get(key, {})
        records[key] = {**old, **item, 'finding_id': key, 'status': 'OPEN',
                        'first_seen': old.get('first_seen', at), 'last_seen': at,
                        'occurrences': old.get('occurrences', 0) + 1,
                        'resolution': None, 'last_checked': at}
    checked = set(checked_paths)
    for key, item in records.items():
        if key in observed or item.get('status') == 'RESOLVED':
            continue
        if item.get('path') in checked:
            item.update(status='RESOLVED', last_checked=at,
                        resolution={'at': at, 'reason': 'defect_absent_on_recheck'})
        else:
            item['status'] = 'NOT_RECHECKED'
    return list(records.values())
