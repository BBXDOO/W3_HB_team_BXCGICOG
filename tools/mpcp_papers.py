#!/usr/bin/env python3
"""Run event-bound Papers with the local File.void text capability only."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from protocol.mpcp.modew.file_artifact import FileVoidTextModew, verify_text_artifact
from protocol.mpcp.runtime.executor import register
from protocol.mpcp.runtime.paper import PaperPackRuntime, PaperPermit, prepare_paper_pack


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--request', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--execute', action='store_true', help='grant exact local text work in this request')
    args = parser.parse_args()
    try:
        pack = prepare_paper_pack(json.loads(args.request.read_text(encoding='utf-8')))
        output = args.output.resolve()
        output.mkdir(parents=True, exist_ok=True)
        root = output / 'artifacts'
        runtime = PaperPackRuntime(output / 'papers')
        register('file-void-text', lambda: FileVoidTextModew(root))
        routes = {paper['PAPER_ID']: 'file-void-text' for paper in pack['PAPERS']}
        verify = lambda paper, result: verify_text_artifact(root, paper, result)
        with (output / 'trace.log').open('a', encoding='utf-8') as log, redirect_stdout(log):
            result = runtime.run(pack, routes=routes, verify=verify)
            if args.execute:
                permits = [PaperPermit(result['pack_hash'], pid, route,
                                       'trusted-local-cli:--execute') for pid, route in routes.items()]
                result = runtime.run(pack, routes=routes, permits=permits, verify=verify)
        (output / 'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps({'state': result['state'], 'papers': {pid: entry['status'] for pid, entry in result['papers'].items()},
                          'result': str(output / 'result.json')}, ensure_ascii=False))
        return 0 if result['state'] == 'SUCCESS' else 2
    except (OSError, ValueError, KeyError) as exc:
        print(json.dumps({'state': 'STOP', 'error': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
