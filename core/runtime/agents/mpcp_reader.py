"""
mpcp_reader — MPCP Document Inspection Helpers
------------------------------------------------
Lightweight utilities that allow runtime agents to read and inspect
MPCP concept documents and module registry files.

Design principles (aligned with MPCP / W3Lgu):
- No heavy schema system — plain text and JSON reading only
- Composable: agents call individual helpers, not a monolithic reader
- Readable: functions return plain dicts / strings / lists
- Traceable: every function accepts explicit paths (no global state)

Concept alignment (W3LGU_MPCP_ROLE_MAPPING.md §6):
  MPCP     — operational structure / orchestration
  W3Lgu    — language / expression / readable representation
  Condien  — meaning / state / context layer
  Paper    — task intent declaration
  ROT      — law / boundary / truth protection
  Result   — what happened record
  PRX      — perception / signal layer
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, FrozenSet, List, Optional


# ---------------------------------------------------------------------------
# Repo root resolution
# ---------------------------------------------------------------------------

# This file lives at core/runtime/agents/mpcp_reader.py
# → repo root is four levels up
_HERE = Path(__file__).resolve().parent
REPO_ROOT: Path = _HERE.parent.parent.parent


# ---------------------------------------------------------------------------
# Core MPCP concept terms (aligned with ROT_PAPER.md / MODEW_PAPER.md)
# ---------------------------------------------------------------------------

MPCP_CORE_TERMS: FrozenSet[str] = frozenset({
    "ROT", "Paper", "Modew", "Condien", "Result",
    "PRX", "Blueprint", "W3Lgu",
})

# Minimum required fields in every module.json (aligned with validate_modules.py)
MODULE_JSON_REQUIRED: FrozenSet[str] = frozenset({
    "name", "role", "scope", "status", "authority",
})


# ---------------------------------------------------------------------------
# Document reading
# ---------------------------------------------------------------------------

def read_doc(rel_path: str) -> str:
    """
    Read a text file relative to the repo root.

    Returns the file contents as a string, or an empty string when the file
    does not exist (callers may check the returned string to handle missing
    docs gracefully without raising).
    """
    full = REPO_ROOT / rel_path
    try:
        return full.read_text(encoding="utf-8")
    except OSError:
        return ""


def doc_exists(rel_path: str) -> bool:
    """Return True when *rel_path* (relative to repo root) resolves to a file."""
    return (REPO_ROOT / rel_path).is_file()


# ---------------------------------------------------------------------------
# Term scanning
# ---------------------------------------------------------------------------

def scan_terms(text: str, terms: FrozenSet[str]) -> List[str]:
    """
    Return the subset of *terms* that appear (case-insensitive) in *text*.

    Checks for the term as a substring so that both plain text and Markdown
    headings / code blocks are covered.
    """
    lower = text.lower()
    return sorted(t for t in terms if t.lower() in lower)


def missing_terms(text: str, terms: FrozenSet[str]) -> List[str]:
    """Return terms from *terms* that do NOT appear in *text*."""
    found = set(scan_terms(text, terms))
    return sorted(t for t in terms if t not in found)


# ---------------------------------------------------------------------------
# Module JSON inspection
# ---------------------------------------------------------------------------

def read_module_json(module_name: str) -> Optional[Dict]:
    """
    Read and parse modules/<module_name>/module.json.

    Returns the parsed dict on success, or None when the file is absent or
    cannot be parsed (e.g., invalid JSON).
    """
    rel = f"modules/{module_name}/module.json"
    text = read_doc(rel)
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def validate_module_json(module_name: str) -> Dict:
    """
    Validate the module.json for *module_name*.

    Returns a result dict:
      {
        "ok":      bool,           # True when all required fields present
        "found":   list[str],      # required fields present
        "missing": list[str],      # required fields absent
        "data":    dict | None,    # parsed module.json, or None on error
      }
    """
    data = read_module_json(module_name)
    if data is None:
        return {"ok": False, "found": [], "missing": list(MODULE_JSON_REQUIRED), "data": None}

    found = sorted(f for f in MODULE_JSON_REQUIRED if f in data)
    missing = sorted(f for f in MODULE_JSON_REQUIRED if f not in data)
    return {"ok": len(missing) == 0, "found": found, "missing": missing, "data": data}
