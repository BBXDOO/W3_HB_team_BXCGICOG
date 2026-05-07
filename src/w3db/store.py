"""
W3DB In-Memory Store
--------------------
A single shared in-process store for all five domains.
Domain dicts are keyed by their respective ID fields.

Thread-safety note:
  This implementation uses plain dicts with no internal locking.
  It is safe for single-threaded use.  For multi-threaded or async
  production workloads either:
    (a) replace W3DBStore with a thread-safe backend (database, Redis, …), or
    (b) wrap all calls with an external threading.Lock.
  Callers are responsible for external synchronization when sharing a
  single W3DBStore instance across threads.
"""

from __future__ import annotations

from typing import Dict, Optional, List

from src.w3db.models import XIZ, TUF, FBD, WHB, PRX


class W3DBStore:
    """Holds all five domain collections in memory."""

    def __init__(self) -> None:
        self._xiz: Dict[str, XIZ] = {}
        self._tuf: Dict[str, TUF] = {}
        self._fbd: Dict[str, FBD] = {}
        self._whb: Dict[str, WHB] = {}
        self._prx: Dict[str, PRX] = {}

    # ------------------------------------------------------------------
    # XIZ
    # ------------------------------------------------------------------

    def create_xiz(self, record: XIZ) -> XIZ:
        if record.xiz_id in self._xiz:
            raise KeyError(f"XIZ record already exists: {record.xiz_id!r}")
        self._xiz[record.xiz_id] = record
        return record

    def read_xiz(self, xiz_id: str) -> Optional[XIZ]:
        return self._xiz.get(xiz_id)

    def update_xiz(self, xiz_id: str, **kwargs) -> XIZ:
        record = self._xiz.get(xiz_id)
        if record is None:
            raise KeyError(f"XIZ record not found: {xiz_id!r}")
        if record.immutable:
            raise PermissionError(f"XIZ record {xiz_id!r} is immutable and cannot be updated")
        for key, value in kwargs.items():
            if not hasattr(record, key):
                raise AttributeError(f"XIZ has no attribute {key!r}")
            setattr(record, key, value)
        return record

    def delete_xiz(self, xiz_id: str) -> bool:
        if xiz_id not in self._xiz:
            return False
        del self._xiz[xiz_id]
        return True

    def list_xiz(self) -> List[XIZ]:
        return list(self._xiz.values())

    # ------------------------------------------------------------------
    # TUF
    # ------------------------------------------------------------------

    def create_tuf(self, record: TUF) -> TUF:
        if record.tuf_id in self._tuf:
            raise KeyError(f"TUF record already exists: {record.tuf_id!r}")
        self._tuf[record.tuf_id] = record
        return record

    def read_tuf(self, tuf_id: str) -> Optional[TUF]:
        return self._tuf.get(tuf_id)

    def update_tuf(self, tuf_id: str, **kwargs) -> TUF:
        record = self._tuf.get(tuf_id)
        if record is None:
            raise KeyError(f"TUF record not found: {tuf_id!r}")
        for key, value in kwargs.items():
            if not hasattr(record, key):
                raise AttributeError(f"TUF has no attribute {key!r}")
            setattr(record, key, value)
        return record

    def delete_tuf(self, tuf_id: str) -> bool:
        if tuf_id not in self._tuf:
            return False
        del self._tuf[tuf_id]
        return True

    def list_tuf(self) -> List[TUF]:
        return list(self._tuf.values())

    # ------------------------------------------------------------------
    # FBD
    # ------------------------------------------------------------------

    def create_fbd(self, record: FBD) -> FBD:
        if record.fbd_id in self._fbd:
            raise KeyError(f"FBD record already exists: {record.fbd_id!r}")
        self._fbd[record.fbd_id] = record
        return record

    def read_fbd(self, fbd_id: str) -> Optional[FBD]:
        return self._fbd.get(fbd_id)

    def update_fbd(self, fbd_id: str, **kwargs) -> FBD:
        record = self._fbd.get(fbd_id)
        if record is None:
            raise KeyError(f"FBD record not found: {fbd_id!r}")
        for key, value in kwargs.items():
            if not hasattr(record, key):
                raise AttributeError(f"FBD has no attribute {key!r}")
            setattr(record, key, value)
        return record

    def delete_fbd(self, fbd_id: str) -> bool:
        if fbd_id not in self._fbd:
            return False
        del self._fbd[fbd_id]
        return True

    def list_fbd(self) -> List[FBD]:
        return list(self._fbd.values())

    # ------------------------------------------------------------------
    # WHB
    # ------------------------------------------------------------------

    def create_whb(self, record: WHB) -> WHB:
        if record.law_id in self._whb:
            raise KeyError(f"WHB record already exists: {record.law_id!r}")
        self._whb[record.law_id] = record
        return record

    def read_whb(self, law_id: str) -> Optional[WHB]:
        return self._whb.get(law_id)

    def update_whb(self, law_id: str, **kwargs) -> WHB:
        record = self._whb.get(law_id)
        if record is None:
            raise KeyError(f"WHB record not found: {law_id!r}")
        for key, value in kwargs.items():
            if not hasattr(record, key):
                raise AttributeError(f"WHB has no attribute {key!r}")
            setattr(record, key, value)
        return record

    def delete_whb(self, law_id: str) -> bool:
        if law_id not in self._whb:
            return False
        del self._whb[law_id]
        return True

    def list_whb(self) -> List[WHB]:
        return list(self._whb.values())

    # ------------------------------------------------------------------
    # PRX
    # ------------------------------------------------------------------

    def create_prx(self, record: PRX) -> PRX:
        if record.prx_id in self._prx:
            raise KeyError(f"PRX record already exists: {record.prx_id!r}")
        self._prx[record.prx_id] = record
        return record

    def read_prx(self, prx_id: str) -> Optional[PRX]:
        return self._prx.get(prx_id)

    def update_prx(self, prx_id: str, **kwargs) -> PRX:
        record = self._prx.get(prx_id)
        if record is None:
            raise KeyError(f"PRX record not found: {prx_id!r}")
        for key, value in kwargs.items():
            if not hasattr(record, key):
                raise AttributeError(f"PRX has no attribute {key!r}")
            setattr(record, key, value)
        return record

    def delete_prx(self, prx_id: str) -> bool:
        if prx_id not in self._prx:
            return False
        del self._prx[prx_id]
        return True

    def list_prx(self) -> List[PRX]:
        return list(self._prx.values())

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """Remove all records from all domains (useful in tests)."""
        self._xiz.clear()
        self._tuf.clear()
        self._fbd.clear()
        self._whb.clear()
        self._prx.clear()

    def stats(self) -> Dict[str, int]:
        """Return record counts per domain."""
        return {
            "xiz": len(self._xiz),
            "tuf": len(self._tuf),
            "fbd": len(self._fbd),
            "whb": len(self._whb),
            "prx": len(self._prx),
        }


# ---------------------------------------------------------------------------
# Module-level singleton (shared across the process)
# ---------------------------------------------------------------------------

_DEFAULT_STORE: Optional[W3DBStore] = None


def get_store() -> W3DBStore:
    """Return (and lazily create) the process-wide default store."""
    global _DEFAULT_STORE
    if _DEFAULT_STORE is None:
        _DEFAULT_STORE = W3DBStore()
    return _DEFAULT_STORE
