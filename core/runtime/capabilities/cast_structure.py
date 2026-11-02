"""Cast IDP v2: bounded source inspection and non-destructive design evidence.

The host chooses the repository. Requests select files inside the existing
manifest read scope; they never select output locations, imports or commands.
AST observations are static evidence, not proof of runtime integration.
"""
from __future__ import annotations

import ast
from collections.abc import Mapping
import hashlib
import json
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[3]
TASKS = {"structural_inspect", "structural_adapt", "capability_learn"}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False).encode()


def execute(task, context):
    if task not in TASKS:
        raise ValueError("unsupported Cast structure task")
    authority = context.get("authority_context", {})
    if not isinstance(authority, Mapping):
        raise ValueError('host authority context must be an object')
    root = Path(authority.get("repo_root", ROOT)).resolve()
    request = context.get("request", {})
    payload = context.get("payload", {})
    if not payload and isinstance(request, Mapping):
        payload = request.get("payload", {})
    if not isinstance(payload, Mapping):
        raise ValueError("Cast inspection payload must be an object")
    paths = payload.get("source_paths")
    if not isinstance(paths, list) or not 1 <= len(paths) <= 32:
        raise ValueError("explicit source_paths of 1 to 32 files required")
    manifest = json.loads((root / 'modules/Cast/module.json').read_text())
    profile_path = root / 'core/identity/profiles/Cast.idp.json'
    profile = json.loads(profile_path.read_text())
    if profile.get('module') != 'Cast' or profile.get('version') != '2.0':
        raise ValueError('Cast IDP v2 identity required')
    scopes = manifest['file_access']['read'] + ['Cast/']

    def inside(name):
        if not isinstance(name, str) or not name or Path(name).is_absolute() or '..' in Path(name).parts:
            raise ValueError('expected repository-relative source path')
        target = (root / name).resolve()
        if not target.is_relative_to(root) or '.git' in target.relative_to(root).parts:
            raise ValueError('source path escapes repository')
        if not any(target == (root / s).resolve() or target.is_relative_to((root / s).resolve()) for s in scopes):
            raise ValueError('source path outside Cast manifest/own context read scope')
        return target

    # Preflight all inputs before creating any output; missing data is not a
    # successful inspection and old runtime memory cannot fill the gap.
    inputs = []
    for name in dict.fromkeys(paths):
        path = inside(name)
        if not path.is_file() or path.stat().st_size > 1024 * 1024:
            raise ValueError('source must be an existing file of at most 1 MiB: ' + name)
        data = path.read_bytes()
        text = data.decode('utf-8')
        row = {'path': name, 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
        if path.suffix == '.py':
            tree = ast.parse(text, filename=name)
            row['symbols'] = [{'name': node.name, 'line': node.lineno,
                               'kind': type(node).__name__} for node in ast.walk(tree)
                              if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
            row['imports'] = [ast.get_source_segment(text, node) for node in ast.walk(tree)
                              if isinstance(node, (ast.Import, ast.ImportFrom))]
            row['calls'] = [{'expression': ast.unparse(node.func), 'line': node.lineno}
                            for node in ast.walk(tree) if isinstance(node, ast.Call)]
        elif path.suffix == '.json':
            value = json.loads(text)
            row['json_type'] = type(value).__name__
            row['keys'] = sorted(value) if isinstance(value, dict) else []
        else:
            row['headings'] = [line for line in text.splitlines() if line.startswith('#')]
        inputs.append(row)

    # Read the designated continuity source rather than claiming engine memory
    # matches are fresh observations for this assignment.
    continuity = root / 'Cast/context/session_summary.md'
    context_ref = None
    if continuity.exists():
        data = inside('Cast/context/session_summary.md').read_bytes()
        context_ref = {'path': 'Cast/context/session_summary.md', 'bytes': len(data),
                       'sha256': hashlib.sha256(data).hexdigest(),
                       'usage': 'historical context reference; not current task evidence'}
    trace = uuid4().hex
    report = {'schema': 'w3.cast.structure_report/1', 'module': 'Cast', 'task': task,
              'request_id': request.get('source_id') or payload.get('request_id'),
              'trace_id': trace, 'idp': {'path': str(profile_path.relative_to(root)),
              'version': profile['version'], 'sha256': hashlib.sha256(profile_path.read_bytes()).hexdigest()},
              'facts': inputs, 'continuity': context_ref,
              'observations': ['Listed symbols/imports/calls describe the inspected source only.'],
              'unknowns': ['Dynamic callers, semantic correctness and end-to-end execution are not established.'],
              'proposals': ([{'action': 'review_extension_points',
                             'basis': [r['path'] for r in inputs],
                             'applied': False}] if task == 'structural_adapt' else []),
              'capability_learning': {'method': 'retain source-bound inspection for comparison',
                                      'automatic_training': False},
              'source_modified': False, 'final_signoff_required': True, 'closed': False}
    pattern = {'schema': 'w3.cast.private_pattern/1', 'request_id': report['request_id'],
               'trace_id': trace, 'basis': [{'path': r['path'], 'sha256': r['sha256']} for r in inputs],
               'pattern': 'Read current source; separate facts, static observations, unknowns and proposed extensions.',
               'source_truth': False, 'report_path': f'modules/Cast/reports/{trace}.json'}
    outputs = [(f'modules/Cast/reports/{trace}.json', report, 'w3.cast.structure_report.json'),
               (f'modules/Cast/artifacts/private/{trace}.json', pattern, 'w3.cast.private_pattern.json')]
    # Verify output containment before mkdir/open, including symlinked parents.
    for name, _, _ in outputs:
        resolved = (root / name).resolve()
        if not resolved.is_relative_to(root / 'modules/Cast'):
            raise ValueError('Cast output escapes its module workspace')
    artifacts = []
    try:
        for name, content, kind in outputs:
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            data = canonical(content) + b'\n'
            with path.open('xb') as stream:
                stream.write(data)
            artifacts.append({'path': name, 'sha256': hashlib.sha256(data).hexdigest(),
                              'bytes': len(data), 'kind': kind})
    except OSError as exc:
        return {'module': 'Cast', 'task': task, 'status': 'REVIEW_REQUIRED',
                'summary': 'Cast output persistence interrupted; inspect retained artifacts before retry.',
                'reason': str(exc), 'artifacts': artifacts, 'mutated': True,
                'traceable': True, 'review': True}
    return {'contract_version': '1.1', 'module': 'Cast', 'task': task,
            'status': 'COMPLETED', 'capability': 'source_structure_inspection',
            'decision': 'inspection_artifacts_created', 'trace_id': trace,
            'summary': f'Inspected {len(inputs)} current source files; retained report and private pattern.',
            'details': report, 'artifacts': artifacts, 'mutated': True, 'traceable': True,
            'review': True, 'source_modified': False,
            'authority': {'decision_allowed': False, 'truth_mutation_allowed': False}}
