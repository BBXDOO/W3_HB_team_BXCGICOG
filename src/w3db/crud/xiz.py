"""
W3DB CRUD — XIZ domain (Execution Trace)

XIZ records are immutable once written: create is allowed, update is not.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from src.w3db.models import XIZ
from src.w3db.store import get_store


def create(record: XIZ) -> XIZ:
    """
    Persist a new XIZ record.

    Raises ValueError if xiz_id already exists (immutability enforced).
    """
    store = get_store()["xiz"]
    if record.xiz_id in store:
        raise ValueError(f"XIZ record '{record.xiz_id}' already exists (immutable)")
    store[record.xiz_id] = record.to_dict()
    return record


def read(xiz_id: str) -> Optional[Dict]:
    """Return the raw dict for xiz_id, or None if not found."""
    return get_store()["xiz"].get(xiz_id)


def list_all() -> List[Dict]:
    """Return all XIZ records as a list of dicts."""
    return list(get_store()["xiz"].values())


def list_by_tuf(tuf_id: str) -> List[Dict]:
    """Return all XIZ records linked to the given tuf_id."""
    return [r for r in get_store()["xiz"].values() if r.get("tuf_id") == tuf_id]
