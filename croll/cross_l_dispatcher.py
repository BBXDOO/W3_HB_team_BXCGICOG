"""
Cross-L Dispatch Planner.

Scope:
    Cross-L layer only.

Purpose:
    Convert a PX reference into a non-executing dispatch plan for Modew.

Important:
    This module plans work only.
    It never executes Modew, mutates truth, writes files, merges changes, or calls external systems.

Core law:
    Cross-L plans the work.
    Modew execution is not allowed yet.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

try:
    from .table_x import get_workset_from_px
except ImportError:  # Allows direct execution: python croll/cross_l_dispatcher.py
    from table_x import get_workset_from_px

DispatchPlan = Dict[str, Any]


def _unknown_workset(workset: Dict[str, Any]) -> bool:
    """Return True when Table-X returned fallback/unknown workset."""
    return workset.get("rytm") == "UNKNOWN" or workset.get("work_type") == "UNKNOWN"


def dispatch_workset(px: Any, paper_context: Optional[Dict[str, Any]] = None) -> DispatchPlan:
    """
    Build a safe dispatch plan from a PX reference.

    Args:
        px: PX reference, e.g. "1,1", "PX:[1,1]", [1, 1], or (1, 1).
        paper_context: Optional Cross-L paper context. This function only passes the
            context into Table-X lookup for trace markers. It does not execute anything.

    Returns:
        A dispatch plan with execution_allowed=False and mutated=False always.
    """
    workset = get_workset_from_px(px, paper_context=paper_context)

    plan: DispatchPlan = {
        "state": "planned",
        "reason": "dispatch_plan_created",
        "scope": "CROSS_L_ONLY",
        "px": workset.get("px"),
        "modew": workset.get("modew_style", "UNKNOWN"),
        "modew_style": workset.get("modew_style", "UNKNOWN"),
        "action": "call_modew_stub_only",
        "execution_allowed": False,
        "mutated": False,
        "review": True,
        "workset": workset,
        "safety": {
            "planner_only": True,
            "modew_execution_allowed": False,
            "truth_mutation_allowed": False,
            "repo_write_allowed": False,
            "direct_merge_allowed": False,
        },
    }

    if _unknown_workset(workset):
        plan.update(
            {
                "state": "review",
                "reason": workset.get("reason", "unknown_px_requires_review"),
                "modew": "UNKNOWN",
                "modew_style": "UNKNOWN",
                "action": "review_before_dispatch",
            }
        )
        return plan

    return plan


if __name__ == "__main__":
    for sample_px in ("1,1", "PX:[2,1]", "99,1", "invalid"):
        print(f"{sample_px} -> {dispatch_workset(sample_px)}")
