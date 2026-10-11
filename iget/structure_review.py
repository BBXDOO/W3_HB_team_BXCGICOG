"""Read-only structural evidence for Origin reviews; never claim runtime success."""
from __future__ import annotations

import ast
from pathlib import Path

from core.runtime.agents.origin_operations import digest


def inspect_structure(root, paths):
    root = Path(root).resolve()
    evidence, findings, calls, definitions = [], [], set(), []
    for value in dict.fromkeys(paths):
        raw = Path(value)
        path = (root / raw).resolve()
        if raw.is_absolute() or '..' in raw.parts or not path.is_relative_to(root):
            raise ValueError('Review path escapes repository')
        if not path.exists():
            findings.append({'kind': 'missing_path', 'path': value})
            continue
        files = [path] if path.is_file() else sorted(path.rglob('*'))
        for file in files:
            if not file.is_file() or any(part in {'.git', 'node_modules', '__pycache__', '.venv'} for part in file.parts):
                continue
            if not file.resolve().is_relative_to(root):
                findings.append({'kind': 'outside_scope_link', 'path': str(file.relative_to(root))})
                continue
            data = file.read_bytes()
            reference = str(file.relative_to(root))
            evidence.append({'path': reference, 'sha256': digest(data), 'bytes': len(data)})
            if file.suffix != '.py':
                continue
            try:
                tree = ast.parse(data, filename=reference)
            except (SyntaxError, UnicodeError) as exc:
                findings.append({'kind': 'invalid_syntax', 'path': reference, 'reason': str(exc)})
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    name = node.func.id if isinstance(node.func, ast.Name) else getattr(node.func, 'attr', '')
                    calls.add(name)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    definitions.append({'path': reference, 'name': node.name, 'line': node.lineno})
    # Call presence is evidence only: dynamic calls and external callers remain unknown.
    return {'module': 'IGET', 'status': 'REVIEW_REQUIRED' if findings else 'COMPLETED',
            'findings': findings, 'evidence': evidence, 'definitions': definitions,
            'call_names': sorted(calls), 'coverage': 'declared paths, bytes, Python syntax and static call inventory',
            'unknowns': ['Static inventory does not prove an end-to-end execution or a missing dynamic caller.'],
            'source_mutated': False}
