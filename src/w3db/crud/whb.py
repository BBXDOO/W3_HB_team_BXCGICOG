"""
W3DB CRUD — WHB domain (Contextual Law / LINE 3)
"""

from __future__ import annotations

from typing import Dict, List, Optional

from src.w3db.models import WHB
from src.w3db.store import get_store


def create(record: WHB) -> WHB:
    """Persist a new WHB record. Raises ValueError if law_id already exists."""
    store = get_store()["whb"]
    if record.law_id in store:
        raise ValueError(f"WHB record '{record.law_id}' already exists")
    store[record.law_id] = record.to_dict()
    return record


def read(law_id: str) -> Optional[Dict]:
    """Return the raw dict for law_id, or None if not found."""
    return get_store()["whb"].get(law_id)


def update(law_id: str, **fields) -> Dict:
    """Update mutable fields of an existing WHB record."""
    store = get_store()["whb"]
    if law_id not in store:
        raise KeyError(f"WHB record '{law_id}' not found")
    allowed = {"condition", "action"}
    for key, value in fields.items():
        if key in allowed:
            store[law_id][key] = value
    return store[law_id]


def list_all() -> List[Dict]:
    """Return all WHB records."""
    return list(get_store()["whb"].values())


def list_by_fbd(fbd_id: str) -> List[Dict]:
    """Return all WHB records linked to the given fbd_id."""
    return [r for r in get_store()["whb"].values() if r.get("fbd_id") == fbd_id]
