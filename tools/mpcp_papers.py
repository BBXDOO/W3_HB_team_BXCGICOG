#!/usr/bin/env python3
"""Run event-bound Papers with host-installed local equipment."""
import argparse
from contextlib import redirect_stdout
import json
import sqlite3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from protocol.mpcp.modew.file_artifact import FileVoidTextModew, verify_text_artifact
from protocol.mpcp.modew.condien_view import CondienViewModew
from protocol.mpcp.lib.registry import LibraryRegistry
from protocol.mpcp.env.boundary import CrossLEnvironmentBoundary
from protocol.mpcp.runtime.paper import PaperPackRuntime, PaperPermit, prepare_paper_pack
from src.core.condien_store import CondienStore


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--request', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--execute', action='store_true', help='grant exact local equipment work in this request')
    parser.add_argument('--condien-store', type=Path, help='trusted local context database')
    parser.add_argument('--condien-name', help='context to load from the store')
    parser.add_argument('--condien-revision', type=int, help='pin an existing context revision')
    args = parser.parse_args()
    try:
        pack = prepare_paper_pack(json.loads(args.request.read_text(encoding='utf-8')))
        stored = None
        if args.condien_store or args.condien_name or args.condien_revision is not None:
            if not args.condien_store or not args.condien_name:
                raise ValueError('both --condien-store and --condien-name are required')
            stored = CondienStore(args.condien_store).load(args.condien_name, revision=args.condien_revision)
            for paper in pack['PAPERS']:
                reference = 'condien:' + stored.snapshot_id
                if paper.get('CONTEXT_REF', reference) != reference:
                    raise ValueError('Paper CONTEXT_REF differs from selected snapshot')
                paper['CONTEXT_REF'] = reference
        output = args.output.resolve()
        output.mkdir(parents=True, exist_ok=True)
        root = output / 'artifacts'
        runtime = PaperPackRuntime(output / 'papers')
        libraries = LibraryRegistry()
        libraries.register_equipment('file-void-text', lambda: FileVoidTextModew(root), group='core',
                                     capabilities=['template_text', 'file_void_handoff', 'external_text_write'])
        libraries.register_equipment('condien-view', CondienViewModew, group='core',
                                     capabilities=['scoped_context_read'])
        # Only these host-installed routes exist; request data cannot import code.
        routes = {p['PAPER_ID']: p.get('MODEW', 'file-void-text') for p in pack['PAPERS']}
        equipment = libraries.activate_equipment(routes.values())
        def verify(paper, result):
            if routes[paper['PAPER_ID']] == 'file-void-text':
                return verify_text_artifact(root, paper, result)
            reads = CrossLEnvironmentBoundary._strings(paper.get('READ'), 'READ')
            denies = CrossLEnvironmentBoundary._strings(paper.get('DENY'), 'DENY')
            expected = CrossLEnvironmentBoundary.scope_condien(stored.condien, reads, denies) if stored else None
            return {'passed': expected is not None and result.get('result') == {
                'context': expected, 'context_ref': paper.get('CONTEXT_REF')}, 'check': 'exact_scoped_context'}
        context = {'condien': stored.condien} if stored else {}
        with (output / 'trace.log').open('a', encoding='utf-8') as log, redirect_stdout(log):
            result = runtime.run(pack, routes=routes, verify=verify, **context)
            if args.execute:
                permits = [PaperPermit(result['pack_hash'], pid, route,
                                       'trusted-local-cli:--execute') for pid, route in routes.items()]
                result = runtime.run(pack, routes=routes, permits=permits, verify=verify, **context)
        result['equipment'] = equipment
        if stored:
            result['condien_snapshot'] = {'snapshot_id': stored.snapshot_id, 'revision': stored.revision}
        (output / 'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps({'state': result['state'], 'papers': {pid: entry['status'] for pid, entry in result['papers'].items()},
                          'result': str(output / 'result.json')}, ensure_ascii=False))
        return 0 if result['state'] == 'SUCCESS' else 2
    except (OSError, ValueError, KeyError, TypeError, sqlite3.DatabaseError) as exc:
        print(json.dumps({'state': 'STOP', 'error': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
