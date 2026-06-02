#!/usr/bin/env python3
"""
Agent MPCP Alignment Tests
===========================
MODE  : concept_alignment_check
TARGET: refactor/v0.2

Verifies that each named module agent (Gemini, DeepSeek, Grok, Cast,
ChatGPT, Copilot-Gm) is:

  1. Registered in the agent registry (AGENT_TABLE)
  2. Equipped with MPCP-aligned metadata (mpcp_role, mpcp_concepts)
  3. Able to read and validate its own module.json (required fields present)
  4. Able to read core MPCP concept documents
  5. Able to detect its concept terms within those documents (inspect_mpcp)
  6. Producing output whose label is consistent with its module role
  7. Correctly positioned relative to the W3Lgu role mapping document

Concept alignment expectations (W3LGU_MPCP_ROLE_MAPPING.md):
  - ROT      = law / boundary / truth protection
  - Paper    = task intent declaration
  - Modew    = execution unit
  - Condien  = meaning / state / context layer
  - Blueprint = declarative setup/plan model
  - Result   = what happened record
  - PRX      = perception / signal layer
  - W3Lgu   = language / expression / intent representation
  - Gemini   = validation
  - DeepSeek = scale / long-term planning
  - Grok     = pattern / signals / insight
  - Cast     = continuity + context bridge
  - ChatGPT  = flow architecture / execution
  - Copilot-Gm = governance / structural consistency

Runs standalone (no pytest required) — mirrors existing repo test style.
Assumptions:
  - Repo root is four levels above this file:
      protocol/mpcp/test_agent_mpcp_alignment.py
  - MPCP concept documents are present under protocol/mpcp/
  - module.json files are present under modules/<name>/module.json
"""

import sys
import os

# ---------------------------------------------------------------------------
# Path setup — resolve repo root so both `core.*` and `src.*` imports work
# ---------------------------------------------------------------------------

_HERE = os.path.dirname(os.path.abspath(__file__))           # .../protocol/mpcp
_SYSTEM_TESTS = os.path.dirname(_HERE)                       # .../SYSTEM/TESTS
_REPO_ROOT = os.path.dirname(os.path.dirname(_SYSTEM_TESTS)) # repo root

for _p in (_REPO_ROOT,):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from core.runtime.agents.registry import get_agent, AGENT_TABLE
from core.runtime.agents.mpcp_reader import (
    read_doc,
    doc_exists,
    scan_terms,
    missing_terms,
    validate_module_json,
    MPCP_CORE_TERMS,
    MODULE_JSON_REQUIRED,
)


# ---------------------------------------------------------------------------
# Test harness (same style as runtime_sanity_sweep.py / test_condien_blueprint.py)
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


# ---------------------------------------------------------------------------
# Constants — modules under test and MPCP concept document paths
# ---------------------------------------------------------------------------

MODULES_UNDER_TEST = [
    "Gemini",
    "DeepSeek",
    "Grok",
    "Cast",
    "ChatGPT",
    "Copilot-Gm",
]

# Core MPCP concept documents (paths relative to repo root)
CONCEPT_DOCS = {
    "ROT_PAPER":    "protocol/mpcp/mpcp_concept_paper/ROT_PAPER.md",
    "MODEW_PAPER":  "protocol/mpcp/MODEW_PAPER.md",
    "MPCP_CONCEPT": "protocol/mpcp/mpcp_concept_paper/mpcp_concept_paper.md",
    "ROLE_MAPPING": "protocol/mpcp/w3lgu_integration_paper/W3LGU_MPCP_ROLE_MAPPING.md",
}

# Role mapping document — used for ecosystem positioning checks
ROLE_MAPPING_PATH = CONCEPT_DOCS["ROLE_MAPPING"]

# Combined text of all concept documents (read once, reused across checks)
_combined_concept_text: str = ""


def _get_combined_text() -> str:
    global _combined_concept_text
    if not _combined_concept_text:
        _combined_concept_text = "\n".join(read_doc(p) for p in CONCEPT_DOCS.values())
    return _combined_concept_text


# ===========================================================================
# 1. Agent registry — all 6 modules must be registered
# ===========================================================================

print("\n=== 1. Agent registry ===")

for name in MODULES_UNDER_TEST:
    check(
        f"'{name}' is registered in AGENT_TABLE",
        name in AGENT_TABLE,
    )

check(
    "get_agent('Gemini') returns GeminiAgent instance",
    type(get_agent("Gemini")).__name__ == "GeminiAgent",
)
check(
    "get_agent('unknown') returns FallbackAgent",
    type(get_agent("__not_a_module__")).__name__ == "FallbackAgent",
)


# ===========================================================================
# 2. Agent MPCP metadata — mpcp_role and mpcp_concepts must be declared
# ===========================================================================

print("\n=== 2. Agent MPCP metadata ===")

EXPECTED_ROLES = {
    "Gemini":     "validation",
    "DeepSeek":   "planning",
    "Grok":       "pattern_insight",
    "Cast":       "continuity_context",
    "ChatGPT":    "flow_architecture",
    "Copilot-Gm": "governance",
}

for name in MODULES_UNDER_TEST:
    agent = get_agent(name)
    check(
        f"{name}: mpcp_role is non-empty string",
        isinstance(agent.mpcp_role, str) and agent.mpcp_role,
    )
    check(
        f"{name}: mpcp_role == '{EXPECTED_ROLES[name]}'",
        agent.mpcp_role == EXPECTED_ROLES[name],
    )
    check(
        f"{name}: mpcp_concepts is a non-empty list",
        isinstance(agent.mpcp_concepts, list) and len(agent.mpcp_concepts) > 0,
    )


# ===========================================================================
# 3. MPCP concept documents — existence and core term coverage
# ===========================================================================

print("\n=== 3. MPCP concept document existence ===")

for doc_label, doc_path in CONCEPT_DOCS.items():
    check(f"concept doc '{doc_label}' exists", doc_exists(doc_path))

print("\n=== 3b. Core MPCP terms in concept documents ===")

# Each core MPCP term should appear in at least one concept document
combined = _get_combined_text()
for term in sorted(MPCP_CORE_TERMS):
    check(
        f"core term '{term}' appears in at least one concept document",
        term.lower() in combined.lower(),
    )


# ===========================================================================
# 4. module.json validation — required fields present for each module
# ===========================================================================

print("\n=== 4. module.json required fields ===")

for name in MODULES_UNDER_TEST:
    result = validate_module_json(name)
    check(
        f"{name}: module.json exists and is valid JSON",
        result["data"] is not None,
    )
    check(
        f"{name}: module.json has all required fields {sorted(MODULE_JSON_REQUIRED)}",
        result["ok"],
    )
    if not result["ok"] and result["missing"]:
        # Surface missing fields for diagnostics (does not count as a new check)
        print(f"         missing: {result['missing']}")

    # Name consistency: module.json 'name' should match the module key
    if result["data"]:
        check(
            f"{name}: module.json 'name' field matches module key",
            result["data"].get("name") == name,
        )


# ===========================================================================
# 5. Concept alignment — each agent finds its concepts in MPCP docs
# ===========================================================================

print("\n=== 5. Agent concept alignment in MPCP documents ===")

combined = _get_combined_text()
for name in MODULES_UNDER_TEST:
    agent = get_agent(name)
    hits = agent.inspect_mpcp(combined)
    check(
        f"{name}: at least one mpcp_concept found in concept documents",
        len(hits) > 0,
    )


# ===========================================================================
# 6. Role mapping — ecosystem positioning document mentions key modules
# ===========================================================================

print("\n=== 6. Ecosystem positioning in role mapping document ===")

# These modules are explicitly named in W3LGU_MPCP_ROLE_MAPPING.md §4 / §9
ROLE_MAPPING_MENTIONS = {"Gemini", "Cast", "Copilot-Gm"}

role_doc = read_doc(ROLE_MAPPING_PATH)
check("Role mapping document is non-empty", len(role_doc) > 0)

for name in ROLE_MAPPING_MENTIONS:
    check(
        f"Role mapping doc mentions '{name}'",
        name in role_doc,
    )

# W3Lgu, MPCP, Condien, ROT must all appear in the role mapping doc
for term in ["W3Lgu", "MPCP", "Condien", "ROT"]:
    check(
        f"Role mapping doc contains MPCP concept '{term}'",
        term in role_doc,
    )

# The doc should explicitly state the separation principle
check(
    "Role mapping doc states MPCP controls operational structure",
    "operational structure" in role_doc,
)
check(
    "Role mapping doc states W3Lgu controls expression/transmission",
    "expression" in role_doc or "transmission" in role_doc,
)


# ===========================================================================
# 7. Agent run() output consistency — label and module name alignment
# ===========================================================================

print("\n=== 7. Agent run() output consistency ===")

_dummy_plan = {
    "role": "test-role",
    "responsibilities": ["test duty"],
}
_dummy_context: dict = {}

for name in MODULES_UNDER_TEST:
    agent = get_agent(name)
    output = agent.run("test_task", _dummy_plan, _dummy_context)
    check(
        f"{name}: run() returns a non-empty string",
        isinstance(output, str) and len(output) > 0,
    )
    check(
        f"{name}: run() output contains module name",
        name in output,
    )
    check(
        f"{name}: run() output contains task name",
        "test_task" in output,
    )
    check(
        f"{name}: run() output contains action_label",
        agent.action_label in output,
    )


# ===========================================================================
# 8. Concept separation — W3Lgu is NOT treated as the execution system
# ===========================================================================

print("\n=== 8. Concept separation (W3Lgu ≠ execution) ===")

role_doc = read_doc(ROLE_MAPPING_PATH)

# The role mapping must state the separation principle (§5.1)
check(
    "Role mapping doc declares 'Execution is not language' principle",
    "execution" in role_doc.lower() and "language" in role_doc.lower(),
)

# Condien must not be reduced to syntax/text-only — the doc should preserve its role
check(
    "Role mapping doc preserves Condien as meaning/state/context layer",
    "meaning" in role_doc.lower() and "context" in role_doc.lower(),
)

# ROT must remain as law/boundary, not collapsed into execution
check(
    "Role mapping doc preserves ROT as law/boundary authority",
    "boundary" in role_doc.lower() and "law" in role_doc.lower(),
)


# ===========================================================================
# Summary
# ===========================================================================

total = len(_results)
passed = sum(1 for status, _ in _results if status == PASS)
failed = total - passed

print("\n" + "=" * 60)
print(f"Agent MPCP Alignment Tests: {passed}/{total} passed")
print("=" * 60)

if failed:
    print("\nFailed checks:")
    for status, label in _results:
        if status == FAIL:
            print(f"  [FAIL] {label}")
    sys.exit(1)
