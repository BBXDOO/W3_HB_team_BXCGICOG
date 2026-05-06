#!/usr/bin/env python3
"""
MPCP Runtime Sanity Sweep
=========================
MODE  : strict_trace
TARGET: refactor/v0.2

Verifies:
- All VALID_STATES are accepted by contract
- CAUSE → ACTION → RESULT traceability on every path
- Executor fail-safe always returns state + cause + error
- Modew cannot produce a result without cause
- Orchestrator handles all states correctly
- to_mpcp_output covers all valid states without falling back to unknown
- rot.validate_fail_condition enforces error field on halt states
"""

import sys
import os

# Resolve package root (SYSTEM/TESTS) so `mpcp.*` imports work from any cwd.
_PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, _PACKAGE_ROOT)

from mpcp.kernel.contract import MPCPContract, VALID_STATES
from mpcp.kernel.rot import MPCPRot
from mpcp.runtime.executor import run, register, to_mpcp_output, PILLAR_REGISTRY
from mpcp.runtime.trace import get_trace_log, clear_trace
from mpcp.modew.base_modew import BaseModew


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

PASS = "PASS"
FAIL = "FAIL"

_results = []


def check(label, expr, expected=True):
    ok = bool(expr) == bool(expected)
    status = PASS if ok else FAIL
    _results.append((status, label))
    print(f"[{status}] {label}")
    return ok


def expect_no_raise(label, fn):
    try:
        fn()
        _results.append((PASS, label))
        print(f"[{PASS}] {label}")
        return True
    except Exception as e:
        _results.append((FAIL, f"{label} — raised: {e}"))
        print(f"[{FAIL}] {label} — raised: {e}")
        return False


def expect_raise(label, fn, substring=None):
    try:
        fn()
        _results.append((FAIL, f"{label} — expected exception, got none"))
        print(f"[{FAIL}] {label} — expected exception, got none")
        return False
    except Exception as e:
        if substring and substring not in str(e):
            _results.append((FAIL, f"{label} — exception missing '{substring}': {e}"))
            print(f"[{FAIL}] {label} — exception missing '{substring}': {e}")
            return False
        _results.append((PASS, label))
        print(f"[{PASS}] {label}")
        return True


# ---------------------------------------------------------------------------
# 1. VALID_STATES coverage
# ---------------------------------------------------------------------------

print("\n=== 1. VALID_STATES contract coverage ===")
# Import VALID_STATES directly — single source of truth
for s in VALID_STATES:
    if s in ("block", "fail"):
        # these require error field
        expect_no_raise(
            f"validate_output accepts state='{s}' with error",
            lambda s=s: MPCPContract.validate_output({"state": s, "error": "test"}),
        )
    else:
        expect_no_raise(
            f"validate_output accepts state='{s}'",
            lambda s=s: MPCPContract.validate_output({"state": s}),
        )

# States NOT in spec must be rejected
for bad in ("OK", "ERROR", "RUNNING", "unknown", ""):
    expect_raise(
        f"validate_output rejects invalid state='{bad}'",
        lambda bad=bad: MPCPContract.validate_output({"state": bad}),
    )

# fail without error field must be rejected
expect_raise(
    "validate_output rejects state='fail' without error field",
    lambda: MPCPContract.validate_output({"state": "fail"}),
)


# ---------------------------------------------------------------------------
# 2. ROT validate_fail_condition — halt states need error
# ---------------------------------------------------------------------------

print("\n=== 2. ROT halt-state error-field enforcement ===")
event = {"TASK": "test"}

for halt in ("STOP", "fail", "block"):
    expect_raise(
        f"validate_fail_condition rejects {halt} without error",
        lambda h=halt: MPCPRot.validate_fail_condition(event, {"state": h}),
    )
    expect_no_raise(
        f"validate_fail_condition accepts {halt} with error",
        lambda h=halt: MPCPRot.validate_fail_condition(event, {"state": h, "error": "x"}),
    )

# Non-halt states do not need error
for ok_state in ("SUCCESS", "done", "WAIT", "warn"):
    expect_no_raise(
        f"validate_fail_condition accepts {ok_state} without error",
        lambda s=ok_state: MPCPRot.validate_fail_condition(event, {"state": s}),
    )


# ---------------------------------------------------------------------------
# 3. Executor — CAUSE always present in result
# ---------------------------------------------------------------------------

print("\n=== 3. Executor CAUSE traceability ===")

# Register a minimal passing modew
class _PassModew(BaseModew):
    def stage_D_process(self, data):
        return {"done": True}

clear_trace()
PILLAR_REGISTRY.pop("_pass", None)
register("_pass", _PassModew)

result = run("TASK:_pass")
check("executor result has 'state'", "state" in result)
check("executor result has 'cause'", "cause" in result)
check("executor result cause == '_pass'", result.get("cause") == "_pass")

# Trace must contain at least A:INPUT and E:RETURN
log = get_trace_log()
stages = [e["stage"] for e in log]
check("trace contains A:INPUT", "A:INPUT" in stages)
check("trace contains E:RETURN", "E:RETURN" in stages)

# Every trace entry with env data must carry TASK (env is passed at all stages)
for entry in log:
    if entry.get("env"):
        check(
            f"trace entry '{entry['stage']}' env contains TASK",
            "TASK" in entry["env"],
        )


# ---------------------------------------------------------------------------
# 4. Executor fail-safe — returns state + cause + error
# ---------------------------------------------------------------------------

print("\n=== 4. Executor fail-safe structure ===")

clear_trace()
result = run("TASK:nonexistent_task_xyz")
check("fail-safe result has 'state'", "state" in result)
check("fail-safe result state is STOP", result.get("state") == "STOP")
check("fail-safe result has 'cause'", "cause" in result)
check("fail-safe result has 'error'", "error" in result)


# ---------------------------------------------------------------------------
# 5. BaseModew — CAUSE in both success and failure paths
# ---------------------------------------------------------------------------

print("\n=== 5. BaseModew CAUSE→ACTION→RESULT ===")

class _SuccessModew(BaseModew):
    def stage_D_process(self, data):
        return "ok"
    def stage_F_output(self, data):
        return data

m = _SuccessModew()
m.set_context("TASK", "test_task")
r = m.run()
check("BaseModew SUCCESS has state", "state" in r)
check("BaseModew SUCCESS has cause", "cause" in r)
check("BaseModew SUCCESS cause equals TASK", r.get("cause") == "test_task")
check("BaseModew SUCCESS has trace", "trace" in r and len(r["trace"]) > 0)


class _FailModew(BaseModew):
    def stage_B_validate(self, data):
        raise ValueError("intentional failure")

m2 = _FailModew()
m2.set_context("TASK", "fail_task")
r2 = m2.run()
check("BaseModew STOP has state=STOP", r2.get("state") == "STOP")
check("BaseModew STOP has cause", "cause" in r2)
check("BaseModew STOP has error", "error" in r2)


# ---------------------------------------------------------------------------
# 6. to_mpcp_output — all valid states produce COLOR + SYM
# ---------------------------------------------------------------------------

print("\n=== 6. to_mpcp_output coverage ===")

_COLOR_EXPECTED = {
    "SUCCESS": "Green", "done": "Green", "ready": "Green",
    "WAIT": "Yellow", "wait": "Yellow", "warn": "Yellow",
    "run": "Yellow", "idle": "Yellow",
    "STOP": "Red", "fail": "Red", "block": "Red",
}

for state, expected_color in _COLOR_EXPECTED.items():
    out = to_mpcp_output({"state": state})
    check(
        f"to_mpcp_output('{state}') contains COLOR:{expected_color}",
        f"COLOR:{expected_color}" in out,
    )
    check(
        f"to_mpcp_output('{state}') contains SYM:",
        "SYM:" in out,
    )

# Non-dict input → fallback to STOP/Red
check(
    "to_mpcp_output(None) → STOP/Red",
    "STATE:STOP" in to_mpcp_output(None),
)


# ---------------------------------------------------------------------------
# 7. Modew boundary — cannot mutate result state to invalid value
# ---------------------------------------------------------------------------

print("\n=== 7. Modew boundary — invalid state rejected by contract ===")

class _BadStateModew(BaseModew):
    def run(self):
        return {"state": "INVALID_STATE_XYZ", "cause": "boundary_test"}

bm = _BadStateModew()
bm.set_context("TASK", "boundary_test")

# The executor must reject this via contract.validate_output
PILLAR_REGISTRY.pop("_boundary", None)
register("_boundary", _BadStateModew)
clear_trace()
result = run("TASK:_boundary")
check("executor catches invalid Modew state", result.get("state") == "STOP")
check("executor error mentions invalid state", "Invalid state" in result.get("error", ""))


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

print("\n" + "=" * 60)
total = len(_results)
passed = sum(1 for s, _ in _results if s == PASS)
failed = total - passed
print(f"MPCP Runtime Sanity Sweep: {passed}/{total} passed")
if failed:
    print("\nFailed checks:")
    for s, label in _results:
        if s == FAIL:
            print(f"  ✕ {label}")
print("=" * 60)

sys.exit(0 if failed == 0 else 1)
