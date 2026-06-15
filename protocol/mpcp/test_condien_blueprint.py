#!/usr/bin/env python3
"""
Condien & Blueprint Foundation Tests
=====================================
MODE  : foundation_check
TARGET: refactor/v0.2

Verifies that the Condien and Blueprint foundations in src/core behave
consistently with the MPCP / W3Lgu concept intent:

  Condien (src/core/condien.py):
    1. Creation / representation
    2. Layer-aware access (READ / DENY)
    3. Active layer cursor
    4. Carry-forward (continuity)
    5. Bounded rebase
    6. W3Lgu serialisation

  Blueprint (src/core/blueprint.py):
    7. Creation from dict
    8. Parsing from W3Lgu KEY:VALUE text (single-line and multi-line)
    9. Required field validation (BlueprintError)
   10. Declarative separation — Blueprint holds no runtime logic
   11. W3Lgu re-serialisation round-trip

Runs standalone (no pytest required) — mirrors existing repo test style.
"""

import sys
import os

# Resolve repo root so `src.*` imports work from any cwd.
# __file__ = <repo>/protocol/mpcp/test_condien_blueprint.py
_REPO_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from src.core.condien import (
    Condien, CondienLayer,
    CONTINUITY_MODES, REBASE_MODES, MEANING_MODES, CONTEXT_MODES,
)
from src.core.blueprint import Blueprint, parse_blueprint, BlueprintError


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


def expect_no_raise(label: str, fn):
    try:
        fn()
        _results.append((PASS, label))
        print(f"[{PASS}] {label}")
        return True
    except Exception as e:
        _results.append((FAIL, f"{label} — raised: {e}"))
        print(f"[{FAIL}] {label} — raised: {e}")
        return False


# ===========================================================================
# 1. Condien — creation and representation
# ===========================================================================

print("\n=== 1. Condien creation and representation ===")

c = Condien(
    name="CORE",
    role="meaning_state_layer",
    layers=["A", "B", "C"],
    meaning_mode="bounded-adaptive",
    context_mode="dynamic",
    continuity="carry-forward",
    rebase="bounded",
    boundary="rot-governed",
    env="preserve",
    modew="REPORT",
    paper="daily_summary",
)

check("Condien name is CORE", c.name == "CORE")
check("Condien role is meaning_state_layer", c.role == "meaning_state_layer")
check("Condien declares 3 layers", c.layers() == ["A", "B", "C"])
check("Condien meaning_mode is bounded-adaptive", c.meaning_mode == "bounded-adaptive")
check("Condien context_mode is dynamic", c.context_mode == "dynamic")
check("Condien continuity is carry-forward", c.continuity == "carry-forward")
check("Condien rebase is bounded", c.rebase == "bounded")
check("Condien boundary is rot-governed", c.boundary == "rot-governed")
check("Condien env is preserve", c.env == "preserve")
check("Condien modew binding is REPORT", c.modew == "REPORT")
check("Condien paper binding is daily_summary", c.paper == "daily_summary")

d = c.to_dict()
check("to_dict has CONDIEN key", "CONDIEN" in d)
check("to_dict CONDIEN == CORE", d["CONDIEN"] == "CORE")
check("to_dict has LAYERS list", isinstance(d["LAYERS"], list))
check("to_dict BOUNDARY == rot-governed", d["BOUNDARY"] == "rot-governed")

# repr should include name and layers
check("repr contains CORE", "CORE" in repr(c))

# Empty name must be rejected
expect_raise(
    "Condien('') raises ValueError",
    lambda: Condien(""),
    ValueError,
)

# Invalid meaning_mode must be rejected
expect_raise(
    "invalid meaning_mode raises ValueError",
    lambda: Condien("X", meaning_mode="wild"),
    ValueError,
    "meaning_mode",
)

# Invalid context_mode must be rejected
expect_raise(
    "invalid context_mode raises ValueError",
    lambda: Condien("X", context_mode="random"),
    ValueError,
    "context_mode",
)


# ===========================================================================
# 2. CondienLayer — access and boundary
# ===========================================================================

print("\n=== 2. CondienLayer access and boundary ===")

layer = CondienLayer(
    name="A",
    data={"allowed": 1, "secret": 2},
    read={"allowed"},
    deny={"secret"},
)

check("layer name A", layer.name == "A")
check("layer can_read allowed", layer.can_read("allowed"))
check("layer cannot read secret", not layer.can_read("secret"))
check("layer read_key allowed returns value", layer.read_key("allowed") == 1)
expect_raise(
    "layer read_key secret denied",
    lambda: layer.read_key("secret"),
    KeyError,
)

layer2 = CondienLayer("B", data={"x": 10})
check("layer with no READ/DENY can read x", layer2.can_read("x"))


# ===========================================================================
# 3. Condien — active layer cursor and carry-forward
# ===========================================================================

print("\n=== 3. Condien active layer cursor and carry-forward ===")

c2 = Condien("CTX", layers=["A", "B"])
check("default active_layer is A", c2.active_layer == "A")
c2.set_active_layer("B")
check("active_layer changed to B", c2.active_layer == "B")
expect_raise(
    "set_active_layer unknown raises KeyError",
    lambda: c2.set_active_layer("Z"),
    KeyError,
)

c2.add_layer("C", data={"v": 3})
check("add_layer includes C", "C" in c2.layers())
check("read_from_layer C.v == 3", c2.read_from_layer("C", "v") == 3)

c3 = Condien("NEXT", layers=["A"])
c3.carry_forward_from(c2)
check("carry_forward stores previous CONDIEN", c3.previous is c2)
check("carry_forward history includes CTX", c3.history[-1] == "CTX")


# ===========================================================================
# 4. Condien — bounded rebase
# ===========================================================================

print("\n=== 4. Condien bounded rebase ===")

c4 = Condien("REB", layers=["A"])
c4.add_layer("A", data={"old": 1})
c4.rebase_layer("A", {"new": 2})
check("rebase_layer replaces old key", "old" not in c4.get_layer("A").data)
check("rebase_layer adds new key", c4.read_from_layer("A", "new") == 2)
expect_raise(
    "rebase_layer missing raises KeyError",
    lambda: c4.rebase_layer("Z", {}),
    KeyError,
)


# ===========================================================================
# 5. Condien — W3Lgu serialisation
# ===========================================================================

print("\n=== 5. Condien W3Lgu serialisation ===")

w3_text = c.to_w3lgu()
check("W3Lgu contains CONDIEN:CORE", "CONDIEN:CORE" in w3_text)
check("W3Lgu contains ROLE:meaning_state_layer", "ROLE:meaning_state_layer" in w3_text)
check("W3Lgu contains BOUNDARY:rot-governed", "BOUNDARY:rot-governed" in w3_text)


# ===========================================================================
# 6. Blueprint — creation and dict behaviour
# ===========================================================================

print("\n=== 6. Blueprint creation and dict behaviour ===")

bp = Blueprint(
    name="REPORT",
    target="daily_summary",
    mode="observe",
    inputs={"source": "logs"},
    outputs={"format": "md"},
    constraints={"no_mutate": True},
)

check("Blueprint name REPORT", bp.name == "REPORT")
check("Blueprint target daily_summary", bp.target == "daily_summary")
check("Blueprint mode observe", bp.mode == "observe")
check("Blueprint inputs.source logs", bp.inputs["source"] == "logs")
check("Blueprint outputs.format md", bp.outputs["format"] == "md")
check("Blueprint constraints.no_mutate true", bp.constraints["no_mutate"] is True)

bp_dict = bp.to_dict()
check("Blueprint to_dict has BLUEPRINT", bp_dict["BLUEPRINT"] == "REPORT")
check("Blueprint to_dict has TARGET", bp_dict["TARGET"] == "daily_summary")
check("Blueprint to_dict has MODE", bp_dict["MODE"] == "observe")


# ===========================================================================
# 7. Blueprint — required field validation
# ===========================================================================

print("\n=== 7. Blueprint required field validation ===")

expect_raise(
    "Blueprint missing name raises BlueprintError",
    lambda: Blueprint(name="", target="x"),
    BlueprintError,
)
expect_raise(
    "Blueprint missing target raises BlueprintError",
    lambda: Blueprint(name="X", target=""),
    BlueprintError,
)
expect_raise(
    "Blueprint invalid mode raises BlueprintError",
    lambda: Blueprint(name="X", target="Y", mode="execute-now"),
    BlueprintError,
)


# ===========================================================================
# 8. Blueprint parser — single-line and multi-line W3Lgu
# ===========================================================================

print("\n=== 8. Blueprint parser from W3Lgu text ===")

single = "BLUEPRINT:REPORT TARGET:daily_summary MODE:observe INPUT:source=logs OUTPUT:format=md CONSTRAINT:no_mutate=true"
parsed_single = parse_blueprint(single)
check("single-line parse name", parsed_single.name == "REPORT")
check("single-line parse target", parsed_single.target == "daily_summary")
check("single-line parse mode", parsed_single.mode == "observe")
check("single-line parse input source", parsed_single.inputs["source"] == "logs")
check("single-line parse output format", parsed_single.outputs["format"] == "md")
check("single-line parse constraint true", parsed_single.constraints["no_mutate"] == "true")

multi = """
BLUEPRINT:CHECK
TARGET:repo
MODE:observe
INPUT:path=src
OUTPUT:format=json
CONSTRAINT:no_write=true
"""
parsed_multi = parse_blueprint(multi)
check("multi-line parse name", parsed_multi.name == "CHECK")
check("multi-line parse target", parsed_multi.target == "repo")
check("multi-line parse input path", parsed_multi.inputs["path"] == "src")

expect_raise(
    "parse_blueprint missing target raises BlueprintError",
    lambda: parse_blueprint("BLUEPRINT:X MODE:observe"),
    BlueprintError,
)


# ===========================================================================
# 9. Blueprint — declarative separation
# ===========================================================================

print("\n=== 9. Blueprint declarative separation ===")

check("Blueprint has no execute method", not hasattr(bp, "execute"))
check("Blueprint has no run method", not hasattr(bp, "run"))
check("Blueprint has no mutate method", not hasattr(bp, "mutate"))


# ===========================================================================
# 10. Blueprint W3Lgu serialisation round-trip
# ===========================================================================

print("\n=== 10. Blueprint W3Lgu serialisation ===")

bp_w3 = bp.to_w3lgu()
check("Blueprint W3Lgu contains BLUEPRINT", "BLUEPRINT:REPORT" in bp_w3)
check("Blueprint W3Lgu contains TARGET", "TARGET:daily_summary" in bp_w3)
check("Blueprint W3Lgu contains MODE", "MODE:observe" in bp_w3)
check("Blueprint W3Lgu contains INPUT", "INPUT:source=logs" in bp_w3)
check("Blueprint W3Lgu contains OUTPUT", "OUTPUT:format=md" in bp_w3)
check("Blueprint W3Lgu contains CONSTRAINT", "CONSTRAINT:no_mutate=True" in bp_w3)

# ===========================================================================
# Summary
# ===========================================================================

passed = sum(1 for status, _ in _results if status == PASS)
total = len(_results)
print("\n" + "=" * 60)
print(f"Condien & Blueprint Foundation Tests: {passed}/{total} passed")
print("=" * 60)

if passed != total:
    raise SystemExit(1)
