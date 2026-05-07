"""
W3DB CRUD — TUF domain (Process State Snapshot)
"""

from __future__ import annotations

from typing import Dict, List, Optional

from src.w3db.models import TUF
from src.w3db.store import get_store


def create(record: TUF) -> TUF:
    """Persist a new TUF record. Raises ValueError if tuf_id already exists."""
    store = get_store()["tuf"]
    if record.tuf_id in store:
        raise ValueError(f"TUF record '{record.tuf_id}' already exists")
    store[record.tuf_id] = record.to_dict()
    return record


def read(tuf_id: str) -> Optional[Dict]:
    """Return the raw dict for tuf_id, or None if not found."""
    return get_store()["tuf"].get(tuf_id)


def update(tuf_id: str, **fields) -> Dict:
    """
    Update mutable fields of an existing TUF record.

    Returns the updated dict.  Raises KeyError if not found.
    """
    store = get_store()["tuf"]
    if tuf_id not in store:
        raise KeyError(f"TUF record '{tuf_id}' not found")
    allowed = {"initial", "final", "confidence", "resolution", "note"}
    for key, value in fields.items():
        if key in allowed:
            store[tuf_id][key] = value
    return store[tuf_id]


def list_all() -> List[Dict]:
    """Return all TUF records."""
    return list(get_store()["tuf"].values())


def list_by_cix(cix_id: str) -> List[Dict]:
    """Return all TUF records linked to the given cix_id."""
    return [r for r in get_store()["tuf"].values() if r.get("cix_id") == cix_id]
