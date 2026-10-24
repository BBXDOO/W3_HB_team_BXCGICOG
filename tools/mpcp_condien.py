#!/usr/bin/env python3
"""Trusted local Condien storage tool: version metadata or explicit snapshot save."""
import argparse
import json
from pathlib import Path
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.core.condien import Condien
from src.core.condien_store import CondienStore


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--store', type=Path, required=True)
    parser.add_argument('--name', help='inspect versions of this context')
    parser.add_argument('--input', type=Path, help='full native Condien state, trusted storage only')
    parser.add_argument('--save', action='store_true', help='explicitly append a version')
    parser.add_argument('--expected-revision', type=int, default=0)
    parser.add_argument('--previous-snapshot', help='explicit predecessor context snapshot')
    args = parser.parse_args()
    try:
        store = CondienStore(args.store)
        if args.save:
            if not args.input:
                raise ValueError('--save requires --input')
            context = Condien.from_state(json.loads(args.input.read_text(encoding='utf-8')))
            saved = store.save(context, expected_revision=args.expected_revision,
                               previous_snapshot_id=args.previous_snapshot)
            result = {'state': 'SUCCESS', 'mutated': True, 'name': saved.condien.name,
                      'snapshot_id': saved.snapshot_id, 'revision': saved.revision}
        else:
            if not args.name or args.input or args.previous_snapshot:
                raise ValueError('inspect requires --name; input/link require --save')
            result = {'state': 'SUCCESS', 'mutated': False, 'name': args.name, 'versions': store.versions(args.name)}
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError, sqlite3.DatabaseError) as exc:
        print(json.dumps({'state': 'STOP', 'error': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
