"""
W3DB CRUD — WHB domain helpers.
"""

from __future__ import annotations

from typing import List, Optional

from src.w3db.models import WHB
from src.w3db.store import W3DBStore, get_store


def create_whb(
    law_id: str,
    fbd_id: str,
    condition: str = "",
    action: str = "",
    store: Optional[W3DBStore] = None,
) -> WHB:
    """Create and persist a new WHB record."""
    s = store or get_store()
    record = WHB(
        law_id=law_id,
        fbd_id=fbd_id,
        condition=condition,
        action=action,
    )
    return s.create_whb(record)


def read_whb(law_id: str, store: Optional[W3DBStore] = None) -> Optional[WHB]:
    """Return the WHB record with the given ID, or None."""
    s = store or get_store()
    return s.read_whb(law_id)


def update_whb(
    law_id: str,
    store: Optional[W3DBStore] = None,
    **kwargs,
) -> WHB:
    """Update fields on an existing WHB record."""
    s = store or get_store()
    return s.update_whb(law_id, **kwargs)


def delete_whb(law_id: str, store: Optional[W3DBStore] = None) -> bool:
    """Delete a WHB record. Returns True if deleted, False if not found."""
    s = store or get_store()
    return s.delete_whb(law_id)


def list_whb(store: Optional[W3DBStore] = None) -> List[WHB]:
    """Return all WHB records."""
    s = store or get_store()
    return s.list_whb()
