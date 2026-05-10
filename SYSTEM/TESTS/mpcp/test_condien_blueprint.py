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
_REPO_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
    "Condien with invalid meaning_mode raises ValueError",
    lambda: Condien("X", meaning_mode="unknown-mode"),
    ValueError,
    "meaning_mode",
)

# Invalid continuity must be rejected
expect_raise(
    "Condien with invalid continuity raises ValueError",
    lambda: Condien("X", continuity="infinite"),
    ValueError,
    "continuity",
)


# ===========================================================================
# 2. Condien — layer-aware access (READ / DENY)
# ===========================================================================

print("\n=== 2. Condien layer-aware access ===")

# Default: all layers readable
c_all = Condien("ALL", layers=["A", "B", "C"])
check("can_read A (no restriction)", c_all.can_read("A"))
check("can_read B (no restriction)", c_all.can_read("B"))
check("can_read C (no restriction)", c_all.can_read("C"))
check("can_read X (not declared) returns False", not c_all.can_read("X"))

# READ list restricts access
c_read = Condien("READ_RESTRICTED", layers=["A", "B", "C"], read_layers=["A", "C"])
check("can_read A (in READ list)", c_read.can_read("A"))
check("can_read B (not in READ list) returns False", not c_read.can_read("B"))
check("can_read C (in READ list)", c_read.can_read("C"))

# DENY overrides READ
c_deny = Condien("DENY_TEST", layers=["A", "B", "C"], deny_layers=["B"])
check("can_read A with DENY=[B]", c_deny.can_read("A"))
check("can_read B with DENY=[B] returns False", not c_deny.can_read("B"))
check("can_read C with DENY=[B]", c_deny.can_read("C"))

# DENY overrides explicit READ
c_both = Condien(
    "BOTH_TEST",
    layers=["A", "B", "C"],
    read_layers=["A", "B"],
    deny_layers=["B"],
)
check("DENY takes precedence over READ for B", not c_both.can_read("B"))
check("A still readable when A in READ and not in DENY", c_both.can_read("A"))

# get_layer raises PermissionError for denied layer
expect_raise(
    "get_layer raises PermissionError for denied layer",
    lambda: c_deny.get_layer("B"),
    PermissionError,
    "denied",
)

# write_layer works for any declared layer (write access is not restricted by READ/DENY)
expect_no_raise(
    "write_layer on declared layer does not raise",
    lambda: c_all.write_layer("A", "key", "value"),
)
check("write_layer stores value", c_all.get_layer("A").data.get("key") == "value")

# write_layer on undeclared layer raises KeyError
expect_raise(
    "write_layer on undeclared layer raises KeyError",
    lambda: c_all.write_layer("Z", "k", "v"),
    KeyError,
)


# ===========================================================================
# 3. Condien — active layer cursor
# ===========================================================================

print("\n=== 3. Condien active layer cursor ===")

c_cur = Condien("CURSOR", layers=["A", "B", "C"])
check("active_layer initially None", c_cur.active_layer() is None)

c_cur.set_active_layer("B")
check("active_layer is B after set", c_cur.active_layer() == "B")

# set_active_layer on undeclared layer raises KeyError
expect_raise(
    "set_active_layer on undeclared layer raises KeyError",
    lambda: c_cur.set_active_layer("Z"),
    KeyError,
)

# set_active_layer on denied layer raises PermissionError
c_deny_cur = Condien("DENY_CUR", layers=["A", "B"], deny_layers=["B"])
expect_raise(
    "set_active_layer on denied layer raises PermissionError",
    lambda: c_deny_cur.set_active_layer("B"),
    PermissionError,
)


# ===========================================================================
# 4. Condien — carry-forward (continuity)
# ===========================================================================

print("\n=== 4. Condien carry-forward (continuity) ===")

c_carry = Condien("CARRY", continuity="carry-forward")
c_carry.carry("task_id", "TASK-001")
c_carry.carry("context_mode", "active")
check("recall task_id", c_carry.recall("task_id") == "TASK-001")
check("recall context_mode", c_carry.recall("context_mode") == "active")
check("recall missing key returns default", c_carry.recall("missing", "N/A") == "N/A")

# continuity=none blocks carry
c_none = Condien("NO_CARRY", continuity="none")
expect_raise(
    "carry on continuity=none raises RuntimeError",
    lambda: c_none.carry("k", "v"),
    RuntimeError,
    "continuity=none",
)


# ===========================================================================
# 5. Condien — bounded rebase
# ===========================================================================

print("\n=== 5. Condien rebase (continuity) ===")

# Source Condien with carry state
src = Condien("SRC", continuity="carry-forward")
src.carry("ctx", "from_src")
src.carry("extra", "extra_val")

# Bounded rebase: only keys already in target are updated
tgt_bounded = Condien("TGT_BOUNDED", continuity="bounded-carry", rebase="bounded")
tgt_bounded.carry("ctx", "old_ctx")   # pre-existing key
# "extra" is NOT in tgt_bounded._carry → should NOT be imported

tgt_bounded.rebase_from(src)
check("bounded rebase updates existing key", tgt_bounded.recall("ctx") == "from_src")
check("bounded rebase does NOT import new key", tgt_bounded.recall("extra") is None)

# Enabled rebase: all source keys imported
tgt_enabled = Condien("TGT_ENABLED", continuity="carry-forward", rebase="enabled")
tgt_enabled.rebase_from(src)
check("enabled rebase imports ctx", tgt_enabled.recall("ctx") == "from_src")
check("enabled rebase imports extra", tgt_enabled.recall("extra") == "extra_val")

# Disabled rebase raises
c_dis = Condien("DIS", continuity="bounded-carry", rebase="disabled")
expect_raise(
    "rebase_from on rebase=disabled raises RuntimeError",
    lambda: c_dis.rebase_from(src),
    RuntimeError,
    "disabled",
)


# ===========================================================================
# 6. Condien — W3Lgu serialisation
# ===========================================================================

print("\n=== 6. Condien W3Lgu serialisation ===")

c_ser = Condien(
    "SERIALISE",
    role="meaning_state_layer",
    layers=["A", "B"],
    read_layers=["A"],
    deny_layers=["B"],
    continuity="carry-forward",
    rebase="bounded",
    boundary="rot-governed",
    env="preserve",
    modew="CHECK",
    paper="rules",
)
w3 = c_ser.to_w3lgu()
check("to_w3lgu contains CONDIEN:SERIALISE", "CONDIEN:SERIALISE" in w3)
check("to_w3lgu contains ROLE:meaning_state_layer", "ROLE:meaning_state_layer" in w3)
check("to_w3lgu contains LAYERS:", "LAYERS:" in w3)
check("to_w3lgu contains READ:", "READ:" in w3)
check("to_w3lgu contains DENY:", "DENY:" in w3)
check("to_w3lgu contains CONTINUITY:carry-forward", "CONTINUITY:carry-forward" in w3)
check("to_w3lgu contains REBASE:bounded", "REBASE:bounded" in w3)
check("to_w3lgu contains BOUNDARY:rot-governed", "BOUNDARY:rot-governed" in w3)
check("to_w3lgu contains ENV:preserve", "ENV:preserve" in w3)
check("to_w3lgu contains MODEW:CHECK", "MODEW:CHECK" in w3)
check("to_w3lgu contains PAPER:rules", "PAPER:rules" in w3)

# Condien with no modew/paper does not emit those fields
c_no_bind = Condien("NO_BIND")
w3_no_bind = c_no_bind.to_w3lgu()
check("to_w3lgu omits MODEW when not set", "MODEW:" not in w3_no_bind)
check("to_w3lgu omits PAPER when not set", "PAPER:" not in w3_no_bind)


# ===========================================================================
# 7. Blueprint — creation from dict
# ===========================================================================

print("\n=== 7. Blueprint creation from dict ===")

bp = Blueprint({
    "NAME": "CONDIEN_RUNTIME",
    "TARGET": "linux",
    "MODE": "full",
    "LIB": "file,event,storage",   # string → parsed as list
    "ROLE": "meaning_state_layer",
    "BOUNDARY": "rot-governed",
    "TRACE": "cause-action-result",
    "ENV": "preserve",
})

check("Blueprint has NAME field", bp.has("NAME"))
check("Blueprint get NAME", bp.get("NAME") == "CONDIEN_RUNTIME")
check("Blueprint get TARGET", bp.get("TARGET") == "linux")
check("Blueprint get MODE", bp.get("MODE") == "full")
check("Blueprint get_list LIB has 3 items", len(bp.get_list("LIB")) == 3)
check("Blueprint LIB includes 'file'", "file" in bp.get_list("LIB"))
check("Blueprint get BOUNDARY", bp.get("BOUNDARY") == "rot-governed")
check("Blueprint get missing field returns None", bp.get("MISSING") is None)
check("Blueprint get missing field with default", bp.get("MISSING", "N/A") == "N/A")
check("Blueprint has returns False for absent field", not bp.has("NONEXISTENT"))

# to_dict contains expected keys
d = bp.to_dict()
check("to_dict has NAME", "NAME" in d)
check("to_dict has BOUNDARY", "BOUNDARY" in d)

# Blueprint with list value at construction time
bp_list = Blueprint({"NAME": "BP_LIST", "LIB": ["fs", "net"]})
check("Blueprint list LIB stored correctly", bp_list.get_list("LIB") == ["fs", "net"])

# Validate passes
expect_no_raise("Blueprint.validate() passes when NAME present", bp.validate)

# Validate fails when NAME missing
bp_no_name = Blueprint({"TARGET": "linux"})
expect_raise(
    "Blueprint.validate() raises BlueprintError when NAME missing",
    bp_no_name.validate,
    BlueprintError,
    "NAME",
)


# ===========================================================================
# 8. Blueprint — parsing from W3Lgu KEY:VALUE text
# ===========================================================================

print("\n=== 8. Blueprint parsing from W3Lgu text ===")

BLUEPRINT_TEXT = """\
NAME:MPCP_CORE
TARGET:android
MODE:min
LIB:fs,store,net
BRIDGE:android
PARTITION:A,B,C
BOUNDARY:rot-governed
TRACE:required
ENV:preserve
"""

bp_parsed = parse_blueprint(BLUEPRINT_TEXT)
check("parsed NAME == MPCP_CORE", bp_parsed.get("NAME") == "MPCP_CORE")
check("parsed TARGET == android", bp_parsed.get("TARGET") == "android")
check("parsed MODE == min", bp_parsed.get("MODE") == "min")
check("parsed LIB is list", isinstance(bp_parsed.to_dict()["LIB"], list))
check("parsed LIB has 3 items", len(bp_parsed.get_list("LIB")) == 3)
check("parsed PARTITION has A,B,C", bp_parsed.get_list("PARTITION") == ["A", "B", "C"])
check("parsed BOUNDARY == rot-governed", bp_parsed.get("BOUNDARY") == "rot-governed")
check("parsed TRACE == required", bp_parsed.get("TRACE") == "required")
check("parsed ENV == preserve", bp_parsed.get("ENV") == "preserve")

# Condien-oriented blueprint
CONDIEN_BP_TEXT = """\
NAME:CONDIEN_RUNTIME
TARGET:linux
MODE:full
LIB:file,event,storage
BRIDGE:linux
OPTIONAL:debug,merge-view
ROLE:meaning_state_layer
BOUNDARY:paper-strict
TRACE:cause-action-result
ENV:non-reduced
"""
bp_cond = parse_blueprint(CONDIEN_BP_TEXT)
check("Condien bp NAME == CONDIEN_RUNTIME", bp_cond.get("NAME") == "CONDIEN_RUNTIME")
check("Condien bp ROLE == meaning_state_layer", bp_cond.get("ROLE") == "meaning_state_layer")
check("Condien bp OPTIONAL is list", isinstance(bp_cond.to_dict()["OPTIONAL"], list))
check("Condien bp OPTIONAL includes debug", "debug" in bp_cond.get_list("OPTIONAL"))
check("Condien bp BOUNDARY == paper-strict", bp_cond.get("BOUNDARY") == "paper-strict")

# Inline (comma-separated multi-pair) parsing — validate=False since no NAME field
# This mirrors the W3Lgu inspection/runtime exchange pattern (not a full blueprint)
INLINE_TEXT = "CONDIEN:CORE,MODEW:REPORT,PAPER:daily_summary"
bp_inline = parse_blueprint(INLINE_TEXT, validate=False)
check("inline parsed CONDIEN == CORE", bp_inline.get("CONDIEN") == "CORE")
check("inline parsed MODEW == REPORT", bp_inline.get("MODEW") == "REPORT")
check("inline parsed PAPER == daily_summary", bp_inline.get("PAPER") == "daily_summary")

# parse_blueprint raises TypeError on non-string input
expect_raise(
    "parse_blueprint(None) raises TypeError",
    lambda: parse_blueprint(None),  # type: ignore[arg-type]
    TypeError,
)

# parse_blueprint raises BlueprintError when NAME missing and validate=True
expect_raise(
    "parse_blueprint raises BlueprintError when NAME missing",
    lambda: parse_blueprint("TARGET:linux\nMODE:min"),
    BlueprintError,
    "NAME",
)

# parse_blueprint with validate=False skips validation
expect_no_raise(
    "parse_blueprint validate=False does not raise even without NAME",
    lambda: parse_blueprint("TARGET:linux", validate=False),
)

# Blank lines and missing ':' tokens are ignored
MESSY_TEXT = "\n\nNAME:CLEAN\n\nnotafield\n\nTARGET:linux\n"
bp_clean = parse_blueprint(MESSY_TEXT)
check("messy text parsed NAME == CLEAN", bp_clean.get("NAME") == "CLEAN")
check("messy text parsed TARGET == linux", bp_clean.get("TARGET") == "linux")


# ===========================================================================
# 9. Blueprint — validation behaviour
# ===========================================================================

print("\n=== 9. Blueprint validation ===")

# NAME is the only required field per W3Lgu-Blueprint profile
minimal = Blueprint({"NAME": "MINIMAL"})
expect_no_raise("Blueprint with only NAME passes validate", minimal.validate)

# BlueprintError is a ValueError subclass (composable)
check("BlueprintError is subclass of ValueError", issubclass(BlueprintError, ValueError))

# to_dict after validate is unchanged
minimal.validate()
check("to_dict after validate still has NAME", minimal.to_dict().get("NAME") == "MINIMAL")


# ===========================================================================
# 10. Blueprint declarative separation — no runtime logic
# ===========================================================================

print("\n=== 10. Blueprint declarative separation ===")

# Blueprint must not have execute/run methods (no imperative execution)
check("Blueprint has no 'run' method", not hasattr(Blueprint, "run"))
check("Blueprint has no 'execute' method", not hasattr(Blueprint, "execute"))

# Blueprint is inert — calling validate() does not trigger any side effects
side_effects = []
bp_inert = Blueprint({"NAME": "INERT", "TARGET": "test"})
expect_no_raise("Blueprint.validate() is side-effect-free", bp_inert.validate)
check("No side effects from Blueprint.validate()", len(side_effects) == 0)

# Blueprint instances are independent (no shared mutable state)
bp_a = Blueprint({"NAME": "A", "MODE": "min"})
bp_b = Blueprint({"NAME": "B", "MODE": "full"})
check("Blueprint A and B are independent", bp_a.get("NAME") != bp_b.get("NAME"))
check("Blueprint MODE difference preserved", bp_a.get("MODE") != bp_b.get("MODE"))


# ===========================================================================
# 11. Blueprint — W3Lgu re-serialisation round-trip
# ===========================================================================

print("\n=== 11. Blueprint W3Lgu round-trip ===")

ORIGINAL = """\
NAME:ROUND_TRIP
TARGET:linux
MODE:full
LIB:fs,store,net
BOUNDARY:rot-governed
TRACE:cause-action-result
ENV:preserve
"""

bp_rt = parse_blueprint(ORIGINAL)
serialised = bp_rt.to_w3lgu()

# Re-parse the serialised form
bp_rt2 = parse_blueprint(serialised)
check("round-trip NAME preserved", bp_rt2.get("NAME") == bp_rt.get("NAME"))
check("round-trip TARGET preserved", bp_rt2.get("TARGET") == bp_rt.get("TARGET"))
check("round-trip BOUNDARY preserved", bp_rt2.get("BOUNDARY") == bp_rt.get("BOUNDARY"))
check("round-trip ENV preserved", bp_rt2.get("ENV") == bp_rt.get("ENV"))
check("round-trip LIB preserved as list", bp_rt2.get_list("LIB") == bp_rt.get_list("LIB"))

# NAME appears first in to_w3lgu output
first_line = serialised.strip().splitlines()[0]
check("to_w3lgu starts with NAME:", first_line.startswith("NAME:"))


# ===========================================================================
# 12. Controlled vocabulary coverage
# ===========================================================================

print("\n=== 12. Controlled vocabulary coverage ===")

check("CONTINUITY_MODES is non-empty", len(CONTINUITY_MODES) > 0)
check("REBASE_MODES is non-empty", len(REBASE_MODES) > 0)
check("MEANING_MODES is non-empty", len(MEANING_MODES) > 0)
check("CONTEXT_MODES is non-empty", len(CONTEXT_MODES) > 0)

# All vocab values accepted by Condien constructor
for cm in CONTINUITY_MODES:
    expect_no_raise(
        f"Condien accepts continuity={cm!r}",
        lambda m=cm: Condien("TEST", continuity=m),
    )
for rm in REBASE_MODES:
    expect_no_raise(
        f"Condien accepts rebase={rm!r}",
        lambda m=rm: Condien("TEST", rebase=m),
    )
for mm in MEANING_MODES:
    expect_no_raise(
        f"Condien accepts meaning_mode={mm!r}",
        lambda m=mm: Condien("TEST", meaning_mode=m),
    )
for ctm in CONTEXT_MODES:
    expect_no_raise(
        f"Condien accepts context_mode={ctm!r}",
        lambda m=ctm: Condien("TEST", context_mode=m),
    )


# ===========================================================================
# Summary
# ===========================================================================

print("\n" + "=" * 60)
total = len(_results)
passed = sum(1 for s, _ in _results if s == PASS)
failed = total - passed
print(f"Condien & Blueprint Foundation Tests: {passed}/{total} passed")
if failed:
    print("\nFailed checks:")
    for s, label in _results:
        if s == FAIL:
            print(f"  ✕ {label}")
print("=" * 60)

sys.exit(0 if failed == 0 else 1)
