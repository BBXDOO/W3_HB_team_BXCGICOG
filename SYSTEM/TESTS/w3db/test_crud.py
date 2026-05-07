#!/usr/bin/env python3
"""
W3DB CRUD Unit Tests
====================
Covers create / read / update / list_all / list_by_* for all five domains:
  XIZ, TUF, FBD, WHB, PRX

Run from repo root:
    python SYSTEM/TESTS/w3db/test_crud.py
"""

import sys
import os

# Resolve repo root so ``src.w3db`` imports work from any cwd.
_REPO_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from src.w3db.models import XIZ, TUF, FBD, WHB, PRX
from src.w3db.store import reset_store
from src.w3db.crud import xiz as xiz_crud
from src.w3db.crud import tuf as tuf_crud
from src.w3db.crud import fbd as fbd_crud
from src.w3db.crud import whb as whb_crud
from src.w3db.crud import prx as prx_crud

# ── Helpers ───────────────────────────────────────────────────────────────────

PASS = "PASS"
FAIL = "FAIL"
_results = []


def check(label, expr, expected=True):
    ok = bool(expr) == bool(expected)
    status = PASS if ok else FAIL
    _results.append((status, label))
    print(f"[{status}] {label}")
    return ok


def expect_raise(label, fn, exc_type=Exception):
    try:
        fn()
        _results.append((FAIL, f"{label} — expected {exc_type.__name__}, got none"))
        print(f"[{FAIL}] {label} — expected {exc_type.__name__}, got none")
        return False
    except exc_type:
        _results.append((PASS, label))
        print(f"[{PASS}] {label}")
        return True


# ── XIZ Tests ─────────────────────────────────────────────────────────────────

print("\n=== XIZ CRUD ===")
reset_store()

x1 = XIZ(xiz_id="XIZ-001", tuf_id="TUF-001", action="Checked patient", result="Stable")
xiz_crud.create(x1)

check("XIZ read returns record", xiz_crud.read("XIZ-001") is not None)
check("XIZ read returns correct action", xiz_crud.read("XIZ-001")["action"] == "Checked patient")
check("XIZ list_all has 1 record", len(xiz_crud.list_all()) == 1)
check("XIZ list_by_tuf returns match", len(xiz_crud.list_by_tuf("TUF-001")) == 1)
check("XIZ list_by_tuf returns nothing for wrong tuf", len(xiz_crud.list_by_tuf("TUF-999")) == 0)
check("XIZ read nonexistent returns None", xiz_crud.read("XIZ-999") is None)
expect_raise("XIZ duplicate create raises ValueError", lambda: xiz_crud.create(x1), ValueError)


# ── TUF Tests ─────────────────────────────────────────────────────────────────

print("\n=== TUF CRUD ===")
reset_store()

t1 = TUF(tuf_id="TUF-001", cix_id="CIX-001", initial=0.5, final=0.5, confidence=0.72)
tuf_crud.create(t1)

check("TUF read returns record", tuf_crud.read("TUF-001") is not None)
check("TUF confidence stored correctly", tuf_crud.read("TUF-001")["confidence"] == 0.72)
check("TUF list_all has 1 record", len(tuf_crud.list_all()) == 1)
check("TUF list_by_cix returns match", len(tuf_crud.list_by_cix("CIX-001")) == 1)

# update
tuf_crud.update("TUF-001", note="Updated note", confidence=0.9)
check("TUF update note", tuf_crud.read("TUF-001")["note"] == "Updated note")
check("TUF update confidence", tuf_crud.read("TUF-001")["confidence"] == 0.9)

expect_raise("TUF duplicate create raises ValueError", lambda: tuf_crud.create(t1), ValueError)
expect_raise("TUF update nonexistent raises KeyError", lambda: tuf_crud.update("TUF-999", note="x"), KeyError)


# ── FBD Tests ─────────────────────────────────────────────────────────────────

print("\n=== FBD CRUD ===")
reset_store()

f1 = FBD(
    fbd_id="FBD-001",
    source_tuf="TUF-001",
    first_deviation="state=0.5",
    failure_point="action A",
    conditions="confidence=0.72",
    impact="uncertain outcome",
    line3_patch="IF state=0.5 THEN observe",
)
fbd_crud.create(f1)

check("FBD read returns record", fbd_crud.read("FBD-001") is not None)
check("FBD source_tuf correct", fbd_crud.read("FBD-001")["source_tuf"] == "TUF-001")
check("FBD list_all has 1 record", len(fbd_crud.list_all()) == 1)
check("FBD list_by_tuf returns match", len(fbd_crud.list_by_tuf("TUF-001")) == 1)

fbd_crud.update("FBD-001", impact="critical")
check("FBD update impact", fbd_crud.read("FBD-001")["impact"] == "critical")

expect_raise("FBD duplicate create raises ValueError", lambda: fbd_crud.create(f1), ValueError)


# ── WHB Tests ─────────────────────────────────────────────────────────────────

print("\n=== WHB CRUD ===")
reset_store()

w1 = WHB(law_id="WHB-001", fbd_id="FBD-001", condition="IF confidence < 0.8", action="THEN observe")
whb_crud.create(w1)

check("WHB read returns record", whb_crud.read("WHB-001") is not None)
check("WHB fbd_id correct", whb_crud.read("WHB-001")["fbd_id"] == "FBD-001")
check("WHB list_all has 1 record", len(whb_crud.list_all()) == 1)
check("WHB list_by_fbd returns match", len(whb_crud.list_by_fbd("FBD-001")) == 1)

whb_crud.update("WHB-001", action="THEN escalate")
check("WHB update action", whb_crud.read("WHB-001")["action"] == "THEN escalate")

expect_raise("WHB duplicate create raises ValueError", lambda: whb_crud.create(w1), ValueError)


# ── PRX Tests ─────────────────────────────────────────────────────────────────

print("\n=== PRX CRUD ===")
reset_store()

t_for_prx = TUF(tuf_id="TUF-002", cix_id="CIX-001", initial=0.5, final=0.5, confidence=0.72)
p1 = PRX.derive(t_for_prx, prx_id="PRX-001", scale=2.0)
prx_crud.create(p1)

check("PRX read returns record", prx_crud.read("PRX-001") is not None)
check("PRX tuf_id correct", prx_crud.read("PRX-001")["tuf_id"] == "TUF-002")
check("PRX symbol is ● (confidence=0.72 → state=0.5)", prx_crud.read("PRX-001")["symbol"] == "●")
check("PRX color is YELLOW", prx_crud.read("PRX-001")["color"] == "YELLOW")
check("PRX intensity formula", abs(prx_crud.read("PRX-001")["intensity"] - 0.44) < 0.01)
check("PRX list_all has 1 record", len(prx_crud.list_all()) == 1)
check("PRX list_by_tuf returns match", len(prx_crud.list_by_tuf("TUF-002")) == 1)

expect_raise("PRX duplicate create raises ValueError", lambda: prx_crud.create(p1), ValueError)


# ── TUF.state() derivation ────────────────────────────────────────────────────

print("\n=== TUF state() derivation ===")

check("TUF state()=1.0 when confidence=0.9", TUF("x","y",1,1,confidence=0.9).state() == 1.0)
check("TUF state()=0.5 when confidence=0.72", TUF("x","y",0.5,0.5,confidence=0.72).state() == 0.5)
check("TUF state()=0.0 when confidence=0.2", TUF("x","y",0,0,confidence=0.2).state() == 0.0)
check("TUF state()=0.5 at boundary confidence=0.4", TUF("x","y",0.5,0.5,confidence=0.4).state() == 0.5)
check("TUF state()=0.0 just below boundary 0.4", TUF("x","y",0,0,confidence=0.39).state() == 0.0)


# ── Summary ───────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
total = len(_results)
passed = sum(1 for s, _ in _results if s == PASS)
failed = total - passed
print(f"W3DB CRUD Tests: {passed}/{total} passed")
if failed:
    print("\nFailed checks:")
    for s, label in _results:
        if s == FAIL:
            print(f"  ✕ {label}")
print("=" * 60)

sys.exit(0 if failed == 0 else 1)
