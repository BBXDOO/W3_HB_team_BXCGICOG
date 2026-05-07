"""
W3DB CRUD — PRX domain helpers.
"""

from __future__ import annotations

from typing import List, Optional

from src.w3db.models import PRX, TUF
from src.w3db.store import W3DBStore, get_store


def create_prx(
    prx_id: str,
    tuf_id: str,
    symbol: str = "●",
    color: str = "YELLOW",
    intensity: float = 0.0,
    scale: float = 2.0,
    store: Optional[W3DBStore] = None,
) -> PRX:
    """Create and persist a new PRX record with explicit values."""
    s = store or get_store()
    record = PRX(
        prx_id=prx_id,
        tuf_id=tuf_id,
        symbol=symbol,
        color=color,
        intensity=intensity,
        scale=scale,
    )
    return s.create_prx(record)


def create_prx_from_tuf(
    prx_id: str,
    tuf: TUF,
    scale: float = 2.0,
    store: Optional[W3DBStore] = None,
) -> PRX:
    """Derive and persist a PRX record from a TUF instance."""
    s = store or get_store()
    record = PRX.from_tuf(prx_id, tuf, scale=scale)
    return s.create_prx(record)


def read_prx(prx_id: str, store: Optional[W3DBStore] = None) -> Optional[PRX]:
    """Return the PRX record with the given ID, or None."""
    s = store or get_store()
    return s.read_prx(prx_id)


def update_prx(
    prx_id: str,
    store: Optional[W3DBStore] = None,
    **kwargs,
) -> PRX:
    """Update fields on an existing PRX record."""
    s = store or get_store()
    return s.update_prx(prx_id, **kwargs)


def delete_prx(prx_id: str, store: Optional[W3DBStore] = None) -> bool:
    """Delete a PRX record. Returns True if deleted, False if not found."""
    s = store or get_store()
    return s.delete_prx(prx_id)


def list_prx(store: Optional[W3DBStore] = None) -> List[PRX]:
    """Return all PRX records."""
    s = store or get_store()
    return s.list_prx()
