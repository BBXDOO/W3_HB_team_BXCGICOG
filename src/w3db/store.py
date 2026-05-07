"""
W3DB In-Memory Store
--------------------
Lightweight dict-based store for each domain.

Each domain has its own namespace (dict keyed by primary ID).
The store is instantiated once per process and shared by all CRUD modules.

Usage:
    from src.w3db.store import get_store
    store = get_store()
    store["xiz"]["XIZ-001"] = {...}
"""

from __future__ import annotations

from typing import Any, Dict, Optional

# Domain keys
DOMAINS = ("xiz", "tuf", "fbd", "whb", "prx")

# Module-level singleton
_store: Optional[Dict[str, Dict[str, Any]]] = None


def get_store() -> Dict[str, Dict[str, Any]]:
    """Return (and lazily create) the global in-memory store."""
    global _store
    if _store is None:
        _store = {domain: {} for domain in DOMAINS}
    return _store


def reset_store() -> None:
    """Clear the store — use in tests to isolate state between cases."""
    global _store
    _store = {domain: {} for domain in DOMAINS}
