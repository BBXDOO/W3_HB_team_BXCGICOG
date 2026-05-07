"""
W3DB CRUD — FBD domain (Failed Boundary Detection)
"""

from __future__ import annotations

from typing import Dict, List, Optional

from src.w3db.models import FBD
from src.w3db.store import get_store


def create(record: FBD) -> FBD:
    """Persist a new FBD record. Raises ValueError if fbd_id already exists."""
    store = get_store()["fbd"]
    if record.fbd_id in store:
        raise ValueError(f"FBD record '{record.fbd_id}' already exists")
    store[record.fbd_id] = record.to_dict()
    return record


def read(fbd_id: str) -> Optional[Dict]:
    """Return the raw dict for fbd_id, or None if not found."""
    return get_store()["fbd"].get(fbd_id)


def update(fbd_id: str, **fields) -> Dict:
    """Update mutable fields of an existing FBD record."""
    store = get_store()["fbd"]
    if fbd_id not in store:
        raise KeyError(f"FBD record '{fbd_id}' not found")
    allowed = {"first_deviation", "failure_point", "conditions", "impact", "line3_patch"}
    for key, value in fields.items():
        if key in allowed:
            store[fbd_id][key] = value
    return store[fbd_id]


def list_all() -> List[Dict]:
    """Return all FBD records."""
    return list(get_store()["fbd"].values())


def list_by_tuf(tuf_id: str) -> List[Dict]:
    """Return all FBD records linked to the given source_tuf."""
    return [r for r in get_store()["fbd"].values() if r.get("source_tuf") == tuf_id]
