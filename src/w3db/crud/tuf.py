"""
W3DB CRUD — TUF domain helpers.
"""

from __future__ import annotations

from typing import List, Optional

from src.w3db.models import TUF
from src.w3db.store import W3DBStore, get_store


def create_tuf(
    tuf_id: str,
    cix_id: Optional[str] = None,
    initial: str = "0.5",
    final: str = "0.5",
    confidence: float = 0.5,
    resolution: str = "",
    note: str = "",
    store: Optional[W3DBStore] = None,
) -> TUF:
    """Create and persist a new TUF record."""
    s = store or get_store()
    record = TUF(
        tuf_id=tuf_id,
        cix_id=cix_id,
        initial=initial,
        final=final,
        confidence=confidence,
        resolution=resolution,
        note=note,
    )
    return s.create_tuf(record)


def read_tuf(tuf_id: str, store: Optional[W3DBStore] = None) -> Optional[TUF]:
    """Return the TUF record with the given ID, or None."""
    s = store or get_store()
    return s.read_tuf(tuf_id)


def update_tuf(
    tuf_id: str,
    store: Optional[W3DBStore] = None,
    **kwargs,
) -> TUF:
    """Update fields on an existing TUF record."""
    s = store or get_store()
    return s.update_tuf(tuf_id, **kwargs)


def delete_tuf(tuf_id: str, store: Optional[W3DBStore] = None) -> bool:
    """Delete a TUF record. Returns True if deleted, False if not found."""
    s = store or get_store()
    return s.delete_tuf(tuf_id)


def list_tuf(store: Optional[W3DBStore] = None) -> List[TUF]:
    """Return all TUF records."""
    s = store or get_store()
    return s.list_tuf()
