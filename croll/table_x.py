"""
Table-X Matrix Lookup for Cross-L.

Reference:
    croll/CROSS_L_TABLE_X_MATRIX.md v0.1

Scope:
    Cross-L layer only.

Purpose:
    Convert a PX reference such as "1,1" or "PX:[1,1]" into a
    bounded workset dictionary for Modew.

Important:
    This module is a pure lookup helper.
    It does not execute code, mutate truth, write files, or merge changes.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, Iterable, Optional, Tuple, Union

PXInput = Union[str, Iterable[int], Tuple[int, int]]
Workset = Dict[str, Any]


TABLE_X: Dict[Tuple[int, int], Workset] = {
    (1, 1): {
        "rytm": "ROCK",
        "work_type": "FAST_PATCH",
        "color": "RED",
        "symbol": "▲",
        "tag_group": ["FAST", "LOW", "SCRIPT", "CONFIG"],
        "lang_candidate": ["C++", "Rust", "C", "Assembly", "WASM", "Bash", "JSON"],
        "modew_style": "Fixer",
        "boundary": "temp_patch",
        "default_review": "on_complete",
        "deny": ["truth_mutation", "direct_merge", "repo_write_without_review"],
        "return_contract": ["state", "reason", "trace", "mutated", "review", "patch_candidate"],
    },
    (2, 1): {
        "rytm": "JAZZ",
        "work_type": "ADAPTIVE_RULE",
        "color": "YELLOW",
        "symbol": "◆",
        "tag_group": ["SCRIPT", "GEN", "CONFIG", "DOC"],
        "lang_candidate": ["Lua", "Python", "JSON", "YAML", "Markdown"],
        "modew_style": "Adapter",
        "boundary": "observe",
        "default_review": "on_uncertain",
        "deny": ["truth_mutation", "file_write", "network", "merge"],
        "return_contract": ["state", "reason", "trace", "mutated", "review"],
    },
    (3, 1): {
        "rytm": "EDM",
        "work_type": "PULSE_LOOP",
        "color": "BLUE",
        "symbol": "●",
        "tag_group": ["SCRIPT", "WEB", "ENV", "CONFIG", "QUERY"],
        "lang_candidate": ["Python", "Bash", "JavaScript", "TypeScript", "JSON", "YAML", "Go"],
        "modew_style": "Runner",
        "boundary": "observe_loop",
        "default_review": "on_error",
        "deny": ["truth_mutation", "direct_merge", "unlimited_loop", "log_flood"],
        "return_contract": [
            "state",
            "reason",
            "trace",
            "mutated",
            "review",
            "pulse_count",
            "limit",
            "stop_condition",
        ],
    },
    (4, 1): {
        "rytm": "BALLAD",
        "work_type": "MEMORY_NOTE",
        "color": "GREEN",
        "symbol": "■",
        "tag_group": ["DOC", "CONFIG", "QUERY", "GEN"],
        "lang_candidate": ["Markdown", "TXT", "JSON", "YAML", "SQL", "Python"],
        "modew_style": "Keeper",
        "boundary": "record_only",
        "default_review": "on_missing_context",
        "deny": ["truth_mutation", "direct_merge", "delete_docs"],
        "return_contract": ["state", "reason", "trace", "mutated", "review", "stored_path"],
    },
    (5, 1): {
        "rytm": "R&B",
        "work_type": "HUMAN_REPORT",
        "color": "BLUE",
        "symbol": "●",
        "tag_group": ["DOC", "WEB", "GEN", "CONFIG"],
        "lang_candidate": ["Markdown", "TXT", "HTML", "CSS", "JavaScript", "Python", "JSON"],
        "modew_style": "Translator",
        "boundary": "readable_output",
        "default_review": "on_risk",
        "deny": ["truth_mutation", "repo_write", "risk_hiding"],
        "return_contract": ["state", "reason", "summary", "risk", "next_step", "mutated", "review"],
    },
    (6, 1): {
        "rytm": "STRING",
        "work_type": "KNOWLEDGE_CHAIN",
        "color": "PURPLE",
        "symbol": "◆",
        "tag_group": ["DOC", "QUERY", "FORMAL", "CONFIG", "GEN"],
        "lang_candidate": ["Markdown", "YAML", "JSON", "SQL", "SPARQL", "Datalog", "Lean", "Python"],
        "modew_style": "Binder",
        "boundary": "knowledge_index",
        "default_review": "on_conflict",
        "deny": ["truth_mutation", "delete_docs", "direct_merge"],
        "return_contract": ["state", "reason", "trace", "mutated", "review", "relation_map"],
    },
}


FALLBACK_WORKSET: Workset = {
    "rytm": "UNKNOWN",
    "work_type": "UNKNOWN",
    "modew_style": "UNKNOWN",
    "boundary": "unknown",
    "mutated": False,
    "review": True,
    "reason": "PX not found in Table-X",
}


def parse_px(px: PXInput) -> Tuple[int, int]:
    """
    Convert a PX input into a tuple: (row, col).

    Supported:
        - "1,1"
        - "PX:[1,1]"
        - "[1,1]"
        - [1, 1]
        - (1, 1)
    """
    if isinstance(px, (tuple, list)) and len(px) == 2:
        return int(px[0]), int(px[1])

    if isinstance(px, str):
        raw = px.strip()
        if raw.startswith("PX:"):
            raw = raw[3:].strip()
        raw = raw.strip("[]")
        parts = raw.split(",")
        if len(parts) == 2:
            return int(parts[0].strip()), int(parts[1].strip())

    raise ValueError(f"Invalid PX format: {px}")


def _review_required(default_review: Optional[str]) -> bool:
    """Return whether the default review condition requires review by default."""
    return default_review not in (None, "never", "false", "none")


def get_workset_from_px(px: PXInput, paper_context: Optional[Dict[str, Any]] = None) -> Workset:
    """
    Look up a bounded workset from Table-X by PX.

    Args:
        px: PX reference, e.g. "1,1", "PX:[1,1]", [1, 1], or (1, 1).
        paper_context: Optional Paper/Cross-L context. This function only records
            that context was provided; it does not execute or mutate anything.

    Returns:
        A workset dict containing at least:
            rytm, work_type, modew_style, boundary, mutated, review.
    """
    try:
        row, col = parse_px(px)
    except (TypeError, ValueError) as exc:
        return {**deepcopy(FALLBACK_WORKSET), "reason": str(exc)}

    workset = TABLE_X.get((row, col))
    if workset is None:
        return {**deepcopy(FALLBACK_WORKSET), "reason": f"PX ({row},{col}) not found in Table-X"}

    result: Workset = {
        "px": [row, col],
        "rytm": workset["rytm"],
        "work_type": workset["work_type"],
        "modew_style": workset["modew_style"],
        "boundary": workset["boundary"],
        "mutated": False,
        "review": _review_required(workset.get("default_review")),
        "color": workset.get("color"),
        "symbol": workset.get("symbol"),
        "tag_group": list(workset.get("tag_group", [])),
        "lang_candidate": list(workset.get("lang_candidate", [])),
        "deny": list(workset.get("deny", [])),
        "return_contract": list(workset.get("return_contract", [])),
        "default_review_condition": workset.get("default_review"),
    }

    if paper_context is not None:
        result["paper_context_received"] = True
        result["paper_context_keys"] = sorted(str(key) for key in paper_context.keys())

    return result


if __name__ == "__main__":
    for sample_px in ("1,1", "PX:[2,1]", "99,1"):
        print(f"{sample_px} -> {get_workset_from_px(sample_px)}")
