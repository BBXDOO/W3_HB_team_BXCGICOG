"""
W3DB CRUD — XIZ domain helpers.

All functions operate on the provided store (or the default singleton).
"""

from __future__ import annotations

from typing import List, Optional

from src.w3db.models import XIZ
from src.w3db.store import W3DBStore, get_store


def create_xiz(
    xiz_id: str,
    action: str,
    timestamp: str,
    result: str = "",
    tuf_id: Optional[str] = None,
    immutable: bool = False,
    store: Optional[W3DBStore] = None,
) -> XIZ:
    """Create and persist a new XIZ record."""
    s = store or get_store()
    record = XIZ(
        xiz_id=xiz_id,
        action=action,
        timestamp=timestamp,
        result=result,
        tuf_id=tuf_id,
        immutable=immutable,
    )
    return s.create_xiz(record)


def read_xiz(xiz_id: str, store: Optional[W3DBStore] = None) -> Optional[XIZ]:
    """Return the XIZ record with the given ID, or None."""
    s = store or get_store()
    return s.read_xiz(xiz_id)


def update_xiz(
    xiz_id: str,
    store: Optional[W3DBStore] = None,
    **kwargs,
) -> XIZ:
    """Update mutable fields on an existing XIZ record."""
    s = store or get_store()
    return s.update_xiz(xiz_id, **kwargs)


def delete_xiz(xiz_id: str, store: Optional[W3DBStore] = None) -> bool:
    """Delete an XIZ record. Returns True if deleted, False if not found."""
    s = store or get_store()
    return s.delete_xiz(xiz_id)


def list_xiz(store: Optional[W3DBStore] = None) -> List[XIZ]:
    """Return all XIZ records."""
    s = store or get_store()
    return s.list_xiz()
