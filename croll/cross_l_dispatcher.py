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

from collections.abc import Mapping
from typing import Any, Dict, Optional

try:
    from .table_x import get_workset_from_px
except ImportError:  # Allows direct execution: python croll/cross_l_dispatcher.py
    from table_x import get_workset_from_px

DispatchPlan = Dict[str, Any]
CrossCodeEnvelope = Dict[str, Any]


def _unknown_workset(workset: Dict[str, Any]) -> bool:
    """Return True when Table-X returned fallback/unknown workset."""
    return workset.get("rytm") == "UNKNOWN" or workset.get("work_type") == "UNKNOWN"


def dispatch_workset(
    px: Any,
    paper_context: Optional[Mapping[str, Any]] = None,
    *,
    enable_box_suggestion: bool = False,
) -> DispatchPlan:
    """
    Build a safe dispatch plan from a PX reference.

    Args:
        px: PX reference, e.g. "1,1", "PX:[1,1]", [1, 1], or (1, 1).
        paper_context: Optional Cross-L paper context. This function only passes the
            context into Table-X lookup for trace markers. It does not execute anything.
        enable_box_suggestion: When true, add one read-only BOX registry suggestion.
            The lookup does not copy, write, execute, or grant new authority.

    Returns:
        A dispatch plan with execution_allowed=False and mutated=False always.
    """
    workset = get_workset_from_px(px, paper_context=paper_context)

    plan: DispatchPlan = {
        "contract_version": "1.0",
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

    if enable_box_suggestion:
        # Lazy import keeps CROLL usable as a standalone planner when BOX is absent.
        from wx.engine_index import search_by_px

        template = search_by_px(workset.get("px"))
        plan["suggested_template"] = (
            {
                "template_id": template["template_id"],
                "name": template["name"],
                "path": template["path"],
                "version": template["version"],
                "boundary": template["boundary"],
                "deny": list(template["deny"]),
                "reference_only": True,
            }
            if template
            else None
        )

    return plan


def dispatch_cross_code(
    px: Any,
    *,
    chain_id: str,
    event_id: str,
    paper_context: Optional[Mapping[str, Any]] = None,
    enable_box_suggestion: bool = False,
    active: bool = True,
) -> CrossCodeEnvelope:
    """Bind a Cross-L plan to one E-CS event without executing CrossCode.

    The envelope is the Cross-Series handoff contract: E-CS supplies trace
    identity, Cross-L supplies bounded work logic, and Modew remains a stub
    target until human review and governance approve a separate execution step.
    """

    if not chain_id.strip() or not event_id.strip():
        raise ValueError("CrossCode dispatch requires non-empty chain_id and event_id")
    if not active:
        return {
            "contract_version": "1.0",
            "kind": "cross-code-dispatch",
            "chain_id": chain_id,
            "event_id": event_id,
            "state": "inactive",
            "reason": "cross_code_not_in_use",
            "cross_l_plan": None,
            "handoff": None,
            "return_value": {
                "state": "inactive",
                "handled": True,
                "execution_allowed": False,
                "mutated": False,
            },
            "execution_allowed": False,
            "mutated": False,
            "review": False,
        }
    plan = dispatch_workset(
        px,
        paper_context=paper_context,
        enable_box_suggestion=enable_box_suggestion,
    )
    return {
        "contract_version": "1.0",
        "kind": "cross-code-dispatch",
        "chain_id": chain_id,
        "event_id": event_id,
        "state": plan["state"],
        "cross_l_plan": plan,
        "handoff": {
            "from": "Cross-L",
            "to": "Modew",
            "action": plan["action"],
            "boundary": plan["workset"]["boundary"],
            "return_contract": list(plan["workset"].get("return_contract", [])),
        },
        "execution_allowed": False,
        "mutated": False,
        "review": True,
    }


if __name__ == "__main__":
    for sample_px in ("1,1", "PX:[2,1]", "99,1", "invalid"):
        print(f"{sample_px} -> {dispatch_workset(sample_px)}")
