#!/usr/bin/env python3
"""
W3DB CRUD Unit Tests
====================
Tests for all five domain CRUD helpers:
  XIZ, TUF, FBD, WHB, PRX

Runs standalone (no pytest required) — mirrors MPCP runtime_sanity_sweep style.
"""

import sys
import os

# Resolve repo root so `src.*` imports work from any cwd.
_REPO_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from src.w3db.store import W3DBStore
from src.w3db.crud.xiz import create_xiz, read_xiz, update_xiz, delete_xiz, list_xiz
from src.w3db.crud.tuf import create_tuf, read_tuf, update_tuf, delete_tuf, list_tuf
from src.w3db.crud.fbd import create_fbd, read_fbd, update_fbd, delete_fbd, list_fbd
from src.w3db.crud.whb import create_whb, read_whb, update_whb, delete_whb, list_whb
from src.w3db.crud.prx import (
    create_prx, create_prx_from_tuf, read_prx, update_prx, delete_prx, list_prx,
)
from src.w3db.models import TUF

# ---------------------------------------------------------------------------
# Test harness (same style as MPCP runtime_sanity_sweep.py)
# ---------------------------------------------------------------------------

PASS = "PASS"
FAIL = "FAIL"
_results = []


def check(label: str, expr, expected=True):
    ok = bool(expr) == bool(expected)
    status = PASS if ok else FAIL
    _results.append((status, label))
    print(f"[{status}] {label}")
    return ok


def expect_raise(label: str, fn, exc_type=Exception, substring=None):
    try:
        fn()
        _results.append((FAIL, f"{label} — expected {exc_type.__name__}, got none"))
        print(f"[{FAIL}] {label} — expected {exc_type.__name__}, got none")
        return False
    except exc_type as e:
        if substring and substring not in str(e):
            _results.append((FAIL, f"{label} — missing {substring!r} in: {e}"))
            print(f"[{FAIL}] {label} — missing {substring!r} in: {e}")
            return False
        _results.append((PASS, label))
        print(f"[{PASS}] {label}")
        return True


# ---------------------------------------------------------------------------
# Each test section uses an isolated store
# ---------------------------------------------------------------------------

print("\n=== 1. XIZ CRUD ===")
s = W3DBStore()

xiz = create_xiz("XIZ-001", "Checked patient", "2026-01-01T00:00:00Z", result="Stable", store=s)
check("create_xiz returns XIZ", xiz.xiz_id == "XIZ-001")
check("read_xiz finds record", read_xiz("XIZ-001", store=s) is not None)
check("list_xiz length == 1", len(list_xiz(store=s)) == 1)

update_xiz("XIZ-001", result="Improved", store=s)
check("update_xiz changes result", read_xiz("XIZ-001", store=s).result == "Improved")

check("delete_xiz returns True", delete_xiz("XIZ-001", store=s))
check("read_xiz after delete returns None", read_xiz("XIZ-001", store=s) is None)
check("delete_xiz missing returns False", delete_xiz("XIZ-001", store=s) is False)

# Duplicate create
create_xiz("XIZ-DUP", "dup", "2026-01-01T00:00:00Z", store=s)
expect_raise(
    "create_xiz duplicate raises KeyError",
    lambda: create_xiz("XIZ-DUP", "dup2", "2026-01-01T00:00:00Z", store=s),
    KeyError,
)

# Immutable guard
s2 = W3DBStore()
create_xiz("XIZ-IMM", "action", "2026-01-01T00:00:00Z", immutable=True, store=s2)
expect_raise(
    "update_xiz immutable raises PermissionError",
    lambda: update_xiz("XIZ-IMM", result="x", store=s2),
    PermissionError,
)


print("\n=== 2. TUF CRUD ===")
s = W3DBStore()

tuf = create_tuf("TUF-001", cix_id="CIX-001", initial="0.5", final="1", confidence=0.8, store=s)
check("create_tuf returns TUF", tuf.tuf_id == "TUF-001")
check("read_tuf finds record", read_tuf("TUF-001", store=s) is not None)
check("list_tuf length == 1", len(list_tuf(store=s)) == 1)

update_tuf("TUF-001", note="updated", store=s)
check("update_tuf changes note", read_tuf("TUF-001", store=s).note == "updated")

check("delete_tuf returns True", delete_tuf("TUF-001", store=s))
check("read_tuf after delete returns None", read_tuf("TUF-001", store=s) is None)

# Invalid state
expect_raise(
    "TUF with invalid initial raises ValueError",
    lambda: create_tuf("TUF-BAD", initial="INVALID", store=W3DBStore()),
    ValueError,
)

# Invalid confidence
expect_raise(
    "TUF with confidence > 1 raises ValueError",
    lambda: create_tuf("TUF-CONF", confidence=1.5, store=W3DBStore()),
    ValueError,
)


print("\n=== 3. FBD CRUD ===")
s = W3DBStore()

fbd = create_fbd("FBD-001", "TUF-001", failure="Red", conditions="x > 0", store=s)
check("create_fbd returns FBD", fbd.fbd_id == "FBD-001")
check("read_fbd finds record", read_fbd("FBD-001", store=s) is not None)
check("list_fbd length == 1", len(list_fbd(store=s)) == 1)

update_fbd("FBD-001", impact="High", store=s)
check("update_fbd changes impact", read_fbd("FBD-001", store=s).impact == "High")

check("delete_fbd returns True", delete_fbd("FBD-001", store=s))
check("read_fbd after delete returns None", read_fbd("FBD-001", store=s) is None)

# Invalid failure level
expect_raise(
    "FBD with invalid failure raises ValueError",
    lambda: create_fbd("FBD-BAD", "TUF-001", failure="Purple", store=W3DBStore()),
    ValueError,
)


print("\n=== 4. WHB CRUD ===")
s = W3DBStore()

whb = create_whb("WHB-001", "FBD-001", condition="IF x > 0", action="THEN alert", store=s)
check("create_whb returns WHB", whb.law_id == "WHB-001")
check("read_whb finds record", read_whb("WHB-001", store=s) is not None)
check("list_whb length == 1", len(list_whb(store=s)) == 1)

update_whb("WHB-001", action="THEN escalate", store=s)
check("update_whb changes action", read_whb("WHB-001", store=s).action == "THEN escalate")

check("delete_whb returns True", delete_whb("WHB-001", store=s))
check("read_whb after delete returns None", read_whb("WHB-001", store=s) is None)


print("\n=== 5. PRX CRUD ===")
s = W3DBStore()

prx = create_prx("PRX-001", "TUF-001", symbol="▲", color="RED", intensity=1.0, store=s)
check("create_prx returns PRX", prx.prx_id == "PRX-001")
check("read_prx finds record", read_prx("PRX-001", store=s) is not None)
check("list_prx length == 1", len(list_prx(store=s)) == 1)

update_prx("PRX-001", intensity=0.9, store=s)
check("update_prx changes intensity", read_prx("PRX-001", store=s).intensity == 0.9)

check("delete_prx returns True", delete_prx("PRX-001", store=s))
check("read_prx after delete returns None", read_prx("PRX-001", store=s) is None)

# from_tuf helper
s2 = W3DBStore()
tuf2 = create_tuf("TUF-PRX", confidence=0.72, store=s2)
prx2 = create_prx_from_tuf("PRX-FROM-TUF", tuf2, store=s2)
check("create_prx_from_tuf tuf_id set", prx2.tuf_id == "TUF-PRX")
check("create_prx_from_tuf symbol is ◆ for mid-range", prx2.symbol == "◆")
check("create_prx_from_tuf intensity > 0", prx2.intensity > 0)

# Invalid symbol / color
expect_raise(
    "PRX with invalid symbol raises ValueError",
    lambda: create_prx("PRX-BAD", "T", symbol="X", color="RED", store=W3DBStore()),
    ValueError,
)
expect_raise(
    "PRX with invalid color raises ValueError",
    lambda: create_prx("PRX-BAD2", "T", symbol="▲", color="PINK", store=W3DBStore()),
    ValueError,
)


print("\n=== 6. Store.clear() and stats() ===")
s = W3DBStore()
create_xiz("X1", "a", "ts", store=s)
create_tuf("T1", store=s)
check("stats before clear xiz==1", s.stats()["xiz"] == 1)
check("stats before clear tuf==1", s.stats()["tuf"] == 1)
s.clear()
check("stats after clear all zero", all(v == 0 for v in s.stats().values()))


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

print("\n" + "=" * 60)
total = len(_results)
passed = sum(1 for st, _ in _results if st == PASS)
failed = total - passed
print(f"W3DB CRUD Tests: {passed}/{total} passed")
if failed:
    print("\nFailed checks:")
    for st, label in _results:
        if st == FAIL:
            print(f"  ✕ {label}")
print("=" * 60)

sys.exit(0 if failed == 0 else 1)
