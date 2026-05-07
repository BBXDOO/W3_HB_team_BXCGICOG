#!/usr/bin/env python3
"""
W3DB Relation Flow Integration Tests
======================================
Verifies the end-to-end flow:
    INPUT → XIZ → TUF → FBD → WHB → PRX

Run from repo root:
    python SYSTEM/TESTS/w3db/test_flow.py
"""

import sys
import os

_REPO_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from src.w3db.models import XIZ, TUF
from src.w3db.store import reset_store, get_store
from src.w3db.flow import run_flow, run_flow_from_input, FlowResult
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


# ── Test 1: Uncertain outcome (confidence=0.72 → state=0.5, deviation) ────────

print("\n=== Test 1: Uncertain flow (deviation detected) ===")
reset_store()

result = run_flow_from_input(
    cix_id="CIX-001",
    action="Checked patient",
    result="Stable",
    confidence=0.72,
    xiz_id="XIZ-001",
    tuf_id="TUF-001",
)

check("FlowResult is FlowResult instance", isinstance(result, FlowResult))
check("state == 0.5 (uncertain)", result.state == 0.5)
check("deviation_detected == True", result.deviation_detected is True)
check("XIZ persisted", xiz_crud.read("XIZ-001") is not None)
check("TUF persisted", tuf_crud.read("TUF-001") is not None)
check("FBD created (deviation)", result.fbd is not None)
check("WHB created (deviation)", result.whb is not None)
check("PRX created (always)", result.prx is not None)

# Check store integrity
check("XIZ in store", len(xiz_crud.list_all()) == 1)
check("TUF in store", len(tuf_crud.list_all()) == 1)
check("FBD in store", len(fbd_crud.list_all()) == 1)
check("WHB in store", len(whb_crud.list_all()) == 1)
check("PRX in store", len(prx_crud.list_all()) == 1)

# PRX perception for uncertain state
check("PRX symbol is ●", result.prx["symbol"] == "●")
check("PRX color is YELLOW", result.prx["color"] == "YELLOW")

# FBD → WHB referential integrity
check("WHB.fbd_id == FBD.fbd_id", result.whb["fbd_id"] == result.fbd["fbd_id"])

# XIZ → TUF referential integrity
check("XIZ.tuf_id == TUF.tuf_id", result.xiz["tuf_id"] == result.tuf["tuf_id"])


# ── Test 2: True outcome (confidence=0.9 → state=1.0, no deviation) ──────────

print("\n=== Test 2: True flow (no deviation) ===")
reset_store()

result2 = run_flow_from_input(
    cix_id="CIX-001",
    action="Follow-up complete",
    result="Resolved",
    confidence=0.9,
)

check("state == 1.0 (true)", result2.state == 1.0)
check("deviation_detected == False", result2.deviation_detected is False)
check("FBD NOT created when no deviation", result2.fbd is None)
check("WHB NOT created when no deviation", result2.whb is None)
check("PRX created even with no deviation", result2.prx is not None)
check("PRX symbol is ▲ for state=1.0", result2.prx["symbol"] == "▲")
check("PRX color is RED for state=1.0", result2.prx["color"] == "RED")

# No FBD/WHB in store
check("FBD store empty", len(fbd_crud.list_all()) == 0)
check("WHB store empty", len(whb_crud.list_all()) == 0)


# ── Test 3: Failure outcome (confidence=0.2 → state=0.0) ─────────────────────

print("\n=== Test 3: Failure flow (state=0.0) ===")
reset_store()

result3 = run_flow_from_input(
    cix_id="CIX-002",
    action="Emergency intervention",
    result="Critical",
    confidence=0.2,
)

check("state == 0.0 (fail/stable)", result3.state == 0.0)
check("deviation_detected == True for state=0.0", result3.deviation_detected is True)
check("FBD created for failure", result3.fbd is not None)
check("PRX symbol is ■ for state=0.0", result3.prx["symbol"] == "■")
check("PRX color is GREEN for state=0.0", result3.prx["color"] == "GREEN")


# ── Test 4: run_flow referential integrity guard ──────────────────────────────

print("\n=== Test 4: Referential integrity enforcement ===")
reset_store()

mismatched_xiz = XIZ(xiz_id="XIZ-X", tuf_id="TUF-WRONG", action="a", result="b")
mismatched_tuf = TUF(tuf_id="TUF-REAL", cix_id="CIX-001", initial=0.5, final=0.5, confidence=0.5)

expect_raise(
    "run_flow raises ValueError on tuf_id mismatch",
    lambda: run_flow(mismatched_xiz, mismatched_tuf),
    ValueError,
)


# ── Test 5: Idempotency guard (duplicate XIZ) ─────────────────────────────────

print("\n=== Test 5: Idempotency — duplicate XIZ rejected ===")
reset_store()

run_flow_from_input(
    cix_id="CIX-001",
    action="First run",
    result="ok",
    confidence=0.72,
    xiz_id="XIZ-DUP",
    tuf_id="TUF-DUP",
)

dup_xiz = XIZ(xiz_id="XIZ-DUP", tuf_id="TUF-DUP2", action="dup", result="dup")
dup_tuf = TUF(tuf_id="TUF-DUP2", cix_id="CIX-001", initial=0.5, final=0.5, confidence=0.5)
expect_raise(
    "Second run_flow with same xiz_id raises ValueError",
    lambda: run_flow(dup_xiz, dup_tuf),
    ValueError,
)


# ── Test 6: FlowResult.to_dict() completeness ────────────────────────────────

print("\n=== Test 6: FlowResult.to_dict() structure ===")
reset_store()

result6 = run_flow_from_input(
    cix_id="CIX-001", action="Scan", result="Normal", confidence=0.72
)
d = result6.to_dict()

for key in ("xiz", "tuf", "fbd", "whb", "prx", "state", "deviation_detected"):
    check(f"to_dict contains key '{key}'", key in d)


# ── Test 7: Multiple runs accumulate correctly ────────────────────────────────

print("\n=== Test 7: Multiple flow runs accumulate store records ===")
reset_store()

for i in range(3):
    run_flow_from_input(
        cix_id=f"CIX-{i}",
        action=f"action_{i}",
        result=f"result_{i}",
        confidence=0.5 + i * 0.2,  # 0.5, 0.7, 0.9
    )

check("3 XIZ records", len(xiz_crud.list_all()) == 3)
check("3 TUF records", len(tuf_crud.list_all()) == 3)
check("3 PRX records", len(prx_crud.list_all()) == 3)
# confidence 0.5 → state=0.5 (dev), 0.7 → 0.5, 0.9 → 1.0
# deviations for confidence 0.5 and 0.7 (2 FBD/WHB)
check("2 FBD records (deviations for c<0.8)", len(fbd_crud.list_all()) == 2)
check("2 WHB records", len(whb_crud.list_all()) == 2)


# ── Summary ───────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
total = len(_results)
passed = sum(1 for s, _ in _results if s == PASS)
failed = total - passed
print(f"W3DB Flow Tests: {passed}/{total} passed")
if failed:
    print("\nFailed checks:")
    for s, label in _results:
        if s == FAIL:
            print(f"  ✕ {label}")
print("=" * 60)

sys.exit(0 if failed == 0 else 1)
