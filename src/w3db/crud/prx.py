"""
W3DB CRUD — PRX domain (Perception Output)

PRX records are derived — they are created by the flow engine, not directly
by user input.  The CRUD layer provides read access and list operations.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from src.w3db.models import PRX
from src.w3db.store import get_store


def create(record: PRX) -> PRX:
    """
    Persist a PRX record (called by the flow engine).

    Raises ValueError if prx_id already exists.
    """
    store = get_store()["prx"]
    if record.prx_id in store:
        raise ValueError(f"PRX record '{record.prx_id}' already exists")
    store[record.prx_id] = record.to_dict()
    return record


def read(prx_id: str) -> Optional[Dict]:
    """Return the raw dict for prx_id, or None if not found."""
    return get_store()["prx"].get(prx_id)


def list_all() -> List[Dict]:
    """Return all PRX records."""
    return list(get_store()["prx"].values())


def list_by_tuf(tuf_id: str) -> List[Dict]:
    """Return all PRX records linked to the given tuf_id."""
    return [r for r in get_store()["prx"].values() if r.get("tuf_id") == tuf_id]
