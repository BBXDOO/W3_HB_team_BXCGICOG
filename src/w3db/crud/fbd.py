"""
W3DB CRUD — FBD domain helpers.
"""

from __future__ import annotations

from typing import List, Optional

from src.w3db.models import FBD
from src.w3db.store import W3DBStore, get_store


def create_fbd(
    fbd_id: str,
    tuf_id: str,
    first_deviation: str = "",
    failure_point: str = "",
    failure: str = "Yellow",
    conditions: str = "",
    impact: str = "",
    line3_patch: str = "",
    store: Optional[W3DBStore] = None,
) -> FBD:
    """Create and persist a new FBD record."""
    s = store or get_store()
    record = FBD(
        fbd_id=fbd_id,
        tuf_id=tuf_id,
        first_deviation=first_deviation,
        failure_point=failure_point,
        failure=failure,
        conditions=conditions,
        impact=impact,
        line3_patch=line3_patch,
    )
    return s.create_fbd(record)


def read_fbd(fbd_id: str, store: Optional[W3DBStore] = None) -> Optional[FBD]:
    """Return the FBD record with the given ID, or None."""
    s = store or get_store()
    return s.read_fbd(fbd_id)


def update_fbd(
    fbd_id: str,
    store: Optional[W3DBStore] = None,
    **kwargs,
) -> FBD:
    """Update fields on an existing FBD record."""
    s = store or get_store()
    return s.update_fbd(fbd_id, **kwargs)


def delete_fbd(fbd_id: str, store: Optional[W3DBStore] = None) -> bool:
    """Delete a FBD record. Returns True if deleted, False if not found."""
    s = store or get_store()
    return s.delete_fbd(fbd_id)


def list_fbd(store: Optional[W3DBStore] = None) -> List[FBD]:
    """Return all FBD records."""
    s = store or get_store()
    return s.list_fbd()
