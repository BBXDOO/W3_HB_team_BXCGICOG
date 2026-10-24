"""SQLite equipment for Condien continuity; append-only versions, explicit links.

Full states include restricted data and are for trusted local storage only.
Loading restores the Condien object; callers still use its layer/key access law.
No storage call grants execution authority or silently updates prior versions.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import sqlite3

from .condien import Condien


def _encode(value):
    encoded = json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)
    if json.loads(encoded) != value:
        raise ValueError("CONDIEN_STORE:NON_LOSSLESS_JSON_STATE")
    return encoded


def _hash(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


@dataclass(frozen=True)
class StoredCondien:
    condien: Condien
    revision: int
    snapshot_id: str
    previous_snapshot_id: str | None


class CondienStore:
    def __init__(self, path: Path):
        self.path = Path(path).resolve()

    def _connect(self, *, write=False):
        if write:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            db = sqlite3.connect(str(self.path), timeout=15)
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('''CREATE TABLE IF NOT EXISTS snapshots (
                snapshot_id TEXT PRIMARY KEY, name TEXT NOT NULL, revision INTEGER NOT NULL,
                body TEXT NOT NULL, previous_id TEXT REFERENCES snapshots(snapshot_id),
                UNIQUE(name,revision))''')
            return db
        if not self.path.is_file():
            raise FileNotFoundError(self.path)
        return sqlite3.connect(self.path.as_uri() + '?mode=ro', uri=True, timeout=15)

    def save(self, condien: Condien, *, expected_revision=0, previous_snapshot_id=None) -> StoredCondien:
        if type(expected_revision) is not int or expected_revision < 0:
            raise ValueError('CONDIEN_STORE:EXPECTED_REVISION_REQUIRED')
        state = condien.to_state()
        # Validate native semantics and lossless representation before opening storage.
        Condien.from_state(state)
        _encode(state)
        if state['previous_name'] and not previous_snapshot_id:
            raise ValueError('CONDIEN_STORE:EXPLICIT_PREVIOUS_SNAPSHOT_REQUIRED')
        db = self._connect(write=True)
        try:
            db.execute('BEGIN IMMEDIATE')
            latest = db.execute('SELECT COALESCE(MAX(revision),0) FROM snapshots WHERE name=?', (condien.name,)).fetchone()[0]
            if latest != expected_revision:
                raise ValueError('CONDIEN_STORE:REVISION_CONFLICT')
            if previous_snapshot_id:
                previous = self._read(db, previous_snapshot_id, set())
                if previous.condien.name != state['previous_name']:
                    raise ValueError('CONDIEN_STORE:PREVIOUS_NAME_MISMATCH')
                if condien.previous is not None and condien.previous.to_state() != previous.condien.to_state():
                    raise ValueError('CONDIEN_STORE:PREVIOUS_STATE_MISMATCH')
            body = _encode({'schema': 'w3.condien.snapshot.1', 'revision': latest + 1,
                            'base_revision': latest, 'previous_snapshot_id': previous_snapshot_id, 'state': state})
            sid = _hash(body)
            db.execute('INSERT INTO snapshots VALUES (?,?,?,?,?)', (sid, condien.name, latest + 1, body, previous_snapshot_id))
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
        return self.load_snapshot(sid)

    def _read(self, db, snapshot_id, seen):
        # Iterative reconstruction keeps long continuity chains independent of
        # Python's call-stack limit.
        loaded = []
        seen = set(seen)
        while snapshot_id is not None:
            if snapshot_id in seen:
                raise ValueError('CONDIEN_STORE:CYCLIC_HISTORY')
            seen.add(snapshot_id)
            row = db.execute('SELECT name,revision,body,previous_id FROM snapshots WHERE snapshot_id=?', (snapshot_id,)).fetchone()
            if row is None:
                raise KeyError(snapshot_id)
            if _hash(row[2]) != snapshot_id:
                raise ValueError('CONDIEN_STORE:SNAPSHOT_HASH_MISMATCH')
            data = json.loads(row[2])
            if (data['schema'] != 'w3.condien.snapshot.1' or data['revision'] != row[1]
                    or data['base_revision'] != row[1] - 1 or data['previous_snapshot_id'] != row[3]
                    or data['state']['identity']['CONDIEN'] != row[0]):
                raise ValueError('CONDIEN_STORE:SNAPSHOT_IDENTITY_MISMATCH')
            c = Condien.from_state(data['state'])
            if row[3] is None and data['state']['previous_name'] is not None:
                raise ValueError('CONDIEN_STORE:PREVIOUS_SNAPSHOT_MISSING')
            loaded.append(StoredCondien(c, row[1], snapshot_id, row[3]))
            snapshot_id = row[3]
        for current, previous in zip(loaded, loaded[1:]):
            if current.condien.to_state()['previous_name'] != previous.condien.name:
                raise ValueError('CONDIEN_STORE:PREVIOUS_NAME_MISMATCH')
            current.condien.previous = previous.condien
        return loaded[0]

    def load_snapshot(self, snapshot_id: str) -> StoredCondien:
        db = self._connect()
        try:
            return self._read(db, snapshot_id, set())
        finally:
            db.close()

    def load(self, name: str, *, revision=None) -> StoredCondien:
        db = self._connect()
        try:
            query = 'SELECT snapshot_id FROM snapshots WHERE name=?'
            args = [name]
            if revision is not None:
                if type(revision) is not int or revision < 1:
                    raise ValueError('CONDIEN_STORE:REVISION_INVALID')
                query += ' AND revision=?'
                args.append(revision)
            row = db.execute(query + ' ORDER BY revision DESC LIMIT 1', args).fetchone()
            if row is None:
                raise KeyError(name)
            return self._read(db, row[0], set())
        finally:
            db.close()

    def versions(self, name: str) -> list[dict]:
        db = self._connect()
        try:
            return [{'snapshot_id': sid, 'revision': revision, 'previous_snapshot_id': previous}
                    for sid, revision, previous in db.execute(
                        'SELECT snapshot_id,revision,previous_id FROM snapshots WHERE name=? ORDER BY revision', (name,))]
        finally:
            db.close()
