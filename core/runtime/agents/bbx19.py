"""BBX19 runtime adapter for explicit human action decisions.

BBEX preserves intent; this module records what BBX19 explicitly decided. It
never invents approval and never performs the approved operation itself.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping

from .base import RuntimeAgent


DECISION_ALIASES = {
    "APPROVE": "APPROVE", "APPROVED": "APPROVE", "SIGN_OFF": "APPROVE",
    "REJECT": "REJECT", "REJECTED": "REJECT", "DENY": "REJECT",
    "HOLD": "HOLD", "WAIT": "HOLD",
    "REVIEW": "REVIEW", "REVIEW_REQUIRED": "REVIEW",
    "CANCEL": "CANCEL", "CANCELLED": "CANCEL",
}


def _text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _items(value: Any) -> List[str]:
    if value is None:
        return []
    values = value if isinstance(value, (list, tuple, set)) else [value]
    return [text for item in values if (text := _text(item))]


def _first(*values: Any) -> Any:
    return next((value for value in values if value not in (None, "")), None)


class BBX19Agent(RuntimeAgent):
    """Record a BBX19 decision without executing its downstream action."""

    module_name = "BBX19"
    action_label = "recorded final human direction"
    mpcp_role = "final_human_decision"
    mpcp_concepts = ["action", "decision", "direction", "approval", "sign-off"]

    def execute(self, task: str, plan: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        request = context.get("request") if isinstance(context.get("request"), Mapping) else {}
        payload = context.get("payload") if isinstance(context.get("payload"), Mapping) else {}
        if not payload and isinstance(request.get("payload"), Mapping):
            payload = request["payload"]

        raw_decision = _first(payload.get("decision"), payload.get("action"), request.get("decision"), request.get("action"))
        decision = DECISION_ALIASES.get(_text(raw_decision).upper(), "")
        reason = _text(_first(payload.get("reason"), request.get("reason")))
        evidence = _items(_first(payload.get("evidence"), request.get("evidence")))
        annotations = _items(_first(payload.get("annotations"), payload.get("annotation"), request.get("annotations"), request.get("annotation")))
        intent_record = _first(
            payload.get("intent_record"), request.get("intent_record"), context.get("intent_record")
        )
        intent_record = intent_record if isinstance(intent_record, Mapping) else None
        override_intent_review = (
            payload.get("override_intent_review") is True
            or request.get("override_intent_review") is True
        )
        source = _text(_first(context.get("source"), request.get("source")))
        decided_by = _text(_first(payload.get("decided_by"), payload.get("approved_by"), request.get("decided_by"), request.get("approved_by")))
        confirmed = payload.get("confirmed") is True or request.get("confirmed") is True
        authenticated = decided_by.upper() == "BBX19" or (source.upper() == "BBX19" and confirmed)

        missing: List[str] = []
        if not decision:
            missing.append("decision")
        if not reason:
            missing.append("reason")
        if not evidence:
            missing.append("evidence")
        if not annotations:
            missing.append("annotation")
        if not authenticated:
            missing.append("explicit_bbx19_confirmation")

        intent_link: Dict[str, Any] | None = None
        intent_blockers: List[str] = []
        non_overridable_intent_blockers: List[str] = []
        review_intent_blockers: List[str] = []
        if intent_record is not None:
            record_type = _text(intent_record.get("record_type"))
            intent_id = _text(intent_record.get("intent_id"))
            intent_state = _text(intent_record.get("state"))
            alignment = intent_record.get("alignment")
            alignment = alignment if isinstance(alignment, Mapping) else {}
            alignment_state = _text(alignment.get("state")) or "OBSERVE"

            if record_type != "w3.intent_record":
                non_overridable_intent_blockers.append("invalid_intent_record_type")
            if not intent_id:
                non_overridable_intent_blockers.append("missing_intent_id")
            if _text(intent_record.get("module")) != "BBEX-Core":
                non_overridable_intent_blockers.append("invalid_intent_source_module")
            if decision == "APPROVE" and intent_state != "READY_FOR_ACTION":
                review_intent_blockers.append("intent_not_ready_for_action")
            if decision == "APPROVE" and alignment_state == "DRIFT_REVIEW":
                review_intent_blockers.append("declared_intent_drift")

            intent_blockers = non_overridable_intent_blockers + review_intent_blockers

            intent_link = {
                "intent_id": intent_id,
                "record_type": record_type,
                "state": intent_state,
                "alignment_state": alignment_state,
                "source_module": _text(intent_record.get("module")),
                "override_applied": bool(review_intent_blockers and override_intent_review),
            }

        unresolved_intent_blockers = non_overridable_intent_blockers + (
            [] if override_intent_review else review_intent_blockers
        )
        missing.extend(unresolved_intent_blockers)

        if missing:
            return {
                "contract_version": "1.0", "status": "REVIEW_REQUIRED",
                "module": self.module_name, "task": task,
                "action": "await_bbx19_decision",
                "decision_state": "AWAITING_BBX19_DECISION",
                "summary": "No final action was authorized; an explicit, evidenced BBX19 decision is required.",
                "reason": "Missing: " + ", ".join(missing), "missing": missing,
                "intent_link": intent_link,
                "intent_blockers": intent_blockers,
                "artifacts": [], "mutated": False, "traceable": True, "review": True,
                "execution": {"allowed": False, "performed": False},
            }

        target = _text(_first(context.get("target"), request.get("target"), "W3")) or "W3"
        seed = json.dumps({
            "task": _text(task), "target": target, "decision": decision,
            "reason": reason, "evidence": evidence, "annotations": annotations,
            "decided_by": "BBX19",
            "intent_id": intent_link["intent_id"] if intent_link else "",
        }, ensure_ascii=False, sort_keys=True)
        decision_id = "BBX19-" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:12]
        record = {
            "record_type": "w3.human_decision", "decision_id": decision_id,
            "decision": decision, "decided_by": "BBX19", "task": _text(task),
            "target": target, "reason": reason, "evidence": evidence,
            "annotations": annotations, "trace_id": _text(context.get("trace_id")),
            "intent_link": intent_link,
            "recorded_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }
        allows_execution = decision == "APPROVE"
        return {
            "contract_version": "1.0", "status": "COMPLETED",
            "module": self.module_name, "task": task,
            "action": "human_decision_recorded", "decision": decision,
            "decision_state": "FINAL_DECISION_RECORDED",
            "summary": f"BBX19 recorded {decision} for '{task}'. No downstream action was executed.",
            "reason": reason, "decision_record": record,
            "intent_link": intent_link,
            "artifacts": [{"kind": "w3.human_decision.inline", "id": decision_id}],
            "mutated": False, "traceable": True, "review": False,
            "execution": {
                "allowed": allows_execution, "performed": False,
                "reason": "This adapter records authority; the authorized runtime performs the action.",
            },
        }
