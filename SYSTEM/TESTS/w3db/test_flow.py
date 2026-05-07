#!/usr/bin/env python3
"""
W3DB Flow Integration Tests
============================
Tests for the automatic relation flow:
  INPUT -> XIZ -> TUF -> FBD -> WHB -> PRX

Runs standalone (no pytest required).
"""

import sys
import os

_REPO_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from src.w3db.store import W3DBStore
from src.w3db.flow import run_flow
from src.w3db.config import W3DBConfig
from src.w3db.models import OBSERVATION_STATES

# ---------------------------------------------------------------------------
# Test harness
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


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def fresh() -> W3DBStore:
    return W3DBStore()


# ---------------------------------------------------------------------------
# 1. Basic flow — all records created
# ---------------------------------------------------------------------------

print("\n=== 1. Basic flow — all five records created ===")
s = fresh()
result = run_flow("Patient arrived — BP 140/90", cix_id="CIX-001", confidence=0.72, store=s)

check("run_flow returns xiz key", "xiz" in result)
check("run_flow returns tuf key", "tuf" in result)
check("run_flow returns fbd key", "fbd" in result)
check("run_flow returns whb key", "whb" in result)
check("run_flow returns prx key", "prx" in result)
check("run_flow returns output key", "output" in result)

check("store has 1 XIZ", s.stats()["xiz"] == 1)
check("store has 1 TUF", s.stats()["tuf"] == 1)
check("store has 1 FBD", s.stats()["fbd"] == 1)
check("store has 1 WHB", s.stats()["whb"] == 1)
check("store has 1 PRX", s.stats()["prx"] == 1)


# ---------------------------------------------------------------------------
# 2. Relations are correctly linked
# ---------------------------------------------------------------------------

print("\n=== 2. Relation linking ===")
s = fresh()
res = run_flow("Test event", cix_id="CIX-A", confidence=0.8, store=s)

xiz = res["xiz"]
tuf = res["tuf"]
fbd = res["fbd"]
whb = res["whb"]
prx = res["prx"]

check("XIZ.tuf_id == TUF.tuf_id", xiz.tuf_id == tuf.tuf_id)
check("FBD.tuf_id == TUF.tuf_id", fbd.tuf_id == tuf.tuf_id)
check("WHB.fbd_id == FBD.fbd_id", whb.fbd_id == fbd.fbd_id)
check("PRX.tuf_id == TUF.tuf_id", prx.tuf_id == tuf.tuf_id)
check("TUF.cix_id == CIX-A", tuf.cix_id == "CIX-A")


# ---------------------------------------------------------------------------
# 3. Confidence → TUF state mapping
# ---------------------------------------------------------------------------

print("\n=== 3. Confidence → TUF state mapping ===")
_cases = [
    (1.0, "1"),
    (0.75, "1"),
    (0.5, "0.5"),
    (0.3, "0.5"),
    (0.25, "0"),
    (0.0, "0"),
]
for conf, expected_state in _cases:
    s = fresh()
    res = run_flow("state mapping test", confidence=conf, store=s)
    tuf = res["tuf"]
    check(
        f"confidence={conf} → TUF.final={expected_state!r}",
        tuf.final == expected_state,
    )
    check(
        f"TUF.final={tuf.final!r} is in OBSERVATION_STATES",
        tuf.final in OBSERVATION_STATES,
    )


# ---------------------------------------------------------------------------
# 4. FBD failure level mapping
# ---------------------------------------------------------------------------

print("\n=== 4. FBD failure level from confidence ===")
_fbd_cases = [
    (0.9, "Green"),
    (0.5, "Yellow"),
    (0.1, "Red"),
]
for conf, expected_failure in _fbd_cases:
    s = fresh()
    res = run_flow("fbd test", confidence=conf, store=s)
    fbd = res["fbd"]
    check(
        f"confidence={conf} → FBD.failure={expected_failure!r}",
        fbd.failure == expected_failure,
    )


# ---------------------------------------------------------------------------
# 5. PRX derived from TUF (perception mapping)
# ---------------------------------------------------------------------------

print("\n=== 5. PRX perception mapping ===")
_prx_cases = [
    (1.0, "▲", "RED"),
    (0.0, "■", "GREEN"),
    (0.5, "●", "YELLOW"),
    (0.72, "◆", "BLUE"),
]
for conf, exp_sym, exp_color in _prx_cases:
    s = fresh()
    res = run_flow("prx test", confidence=conf, store=s)
    prx = res["prx"]
    check(
        f"confidence={conf} → PRX.symbol={exp_sym!r}",
        prx.symbol == exp_sym,
    )
    check(
        f"confidence={conf} → PRX.color={exp_color!r}",
        prx.color == exp_color,
    )
    check(
        f"confidence={conf} → PRX.intensity >= 0",
        prx.intensity >= 0,
    )


# ---------------------------------------------------------------------------
# 6. WHB condition and action generated
# ---------------------------------------------------------------------------

print("\n=== 6. WHB law generation ===")
s = fresh()
res = run_flow("whb test", confidence=0.1, store=s)
whb = res["whb"]
check("WHB.condition starts with IF", whb.condition.startswith("IF"))
check("WHB.action starts with THEN", whb.action.startswith("THEN"))


# ---------------------------------------------------------------------------
# 7. Output dict structure
# ---------------------------------------------------------------------------

print("\n=== 7. Output dict structure ===")
s = fresh()
res = run_flow("output test", confidence=0.6, store=s)
out = res["output"]
for key in ("cix", "xiz", "tuf", "fbd", "whb", "prx"):
    check(f"output contains key={key!r}", key in out)

check("output.tuf contains confidence", "confidence" in out["tuf"])
check("output.prx contains symbol", "symbol" in out["prx"])
check("output.prx contains intensity", "intensity" in out["prx"])


# ---------------------------------------------------------------------------
# 8. Multiple runs produce independent records (no ID collision)
# ---------------------------------------------------------------------------

print("\n=== 8. Multiple independent runs ===")
s = fresh()
run_flow("run A", confidence=0.3, store=s)
run_flow("run B", confidence=0.7, store=s)
run_flow("run C", confidence=0.5, store=s)

check("3 XIZ records after 3 runs", s.stats()["xiz"] == 3)
check("3 TUF records after 3 runs", s.stats()["tuf"] == 3)
check("3 FBD records after 3 runs", s.stats()["fbd"] == 3)
check("3 WHB records after 3 runs", s.stats()["whb"] == 3)
check("3 PRX records after 3 runs", s.stats()["prx"] == 3)


# ---------------------------------------------------------------------------
# 9. Explicit IDs are honoured
# ---------------------------------------------------------------------------

print("\n=== 9. Explicit ID assignment ===")
s = fresh()
res = run_flow(
    "explicit id test",
    xiz_id="XIZ-EXPLICIT",
    tuf_id="TUF-EXPLICIT",
    fbd_id="FBD-EXPLICIT",
    whb_id="WHB-EXPLICIT",
    prx_id="PRX-EXPLICIT",
    store=s,
)
check("explicit XIZ id used", res["xiz"].xiz_id == "XIZ-EXPLICIT")
check("explicit TUF id used", res["tuf"].tuf_id == "TUF-EXPLICIT")
check("explicit FBD id used", res["fbd"].fbd_id == "FBD-EXPLICIT")
check("explicit WHB id used", res["whb"].law_id == "WHB-EXPLICIT")
check("explicit PRX id used", res["prx"].prx_id == "PRX-EXPLICIT")


# ---------------------------------------------------------------------------
# 10. Config — immutable_xiz=True in prod config
# ---------------------------------------------------------------------------

print("\n=== 10. Config: immutable_xiz=True (prod) ===")
cfg = W3DBConfig(env="prod", immutable_xiz=True)
s = fresh()
res = run_flow("prod flow", confidence=0.5, config=cfg, store=s)
check("XIZ is immutable in prod config", res["xiz"].immutable is True)


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

print("\n" + "=" * 60)
total = len(_results)
passed = sum(1 for st, _ in _results if st == PASS)
failed = total - passed
print(f"W3DB Flow Tests: {passed}/{total} passed")
if failed:
    print("\nFailed checks:")
    for st, label in _results:
        if st == FAIL:
            print(f"  ✕ {label}")
print("=" * 60)

sys.exit(0 if failed == 0 else 1)
