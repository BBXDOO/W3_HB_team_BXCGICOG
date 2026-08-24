from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any, Dict

from .base import RuntimeAgent


class CopilotGmAgent(RuntimeAgent):
    """Deterministic governance reviewer; never merges or grants authority."""

    module_name = "Copilot-Gm"
    action_label = "completed governance review"
    mpcp_role = "governance"
    mpcp_concepts = [
        "governance",
        "policy",
        "compliance",
        "structural consistency",
    ]

    def execute(
        self,
        task: str,
        plan: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        if not isinstance(plan, Mapping) or not isinstance(context, Mapping):
            return {
                "contract_version": "1.1",
                "status": "REVIEW_REQUIRED",
                "module": self.module_name,
                "task": str(task or ""),
                "role": self.mpcp_role,
                "action": "validate_governance_review_input",
                "decision": "invalid_review_input",
                "reason": "plan and context must be mappings",
                "summary": "Governance review did not run because its input contract was invalid.",
                "details": {"merge_performed": False, "authority_granted": False},
                "artifacts": [],
                "mutated": False,
                "traceable": True,
                "review": True,
            }
        request = (
            context.get("request")
            if isinstance(context.get("request"), Mapping)
            else {}
        )
        payload = context.get("payload") if isinstance(context.get("payload"), Mapping) else {}
        if not payload and isinstance(request.get("payload"), Mapping):
            payload = request["payload"]
        evidence = (
            context.get("doc_text")
            or request.get("doc_text")
            or context.get("text")
            or request.get("text")
            or context.get("evidence")
            or request.get("evidence")
            or payload.get("doc_text")
            or payload.get("text")
            or payload.get("evidence")
            or ""
        )
        target = context.get("target") or request.get("target") or "W3"
        required = list(self.mpcp_concepts)
        if isinstance(evidence, str):
            evidence_text = evidence
        elif evidence:
            try:
                evidence_text = json.dumps(evidence, ensure_ascii=False, sort_keys=True)
            except (TypeError, ValueError):
                evidence_text = str(evidence)
        else:
            evidence_text = ""
        found = self.inspect_mpcp(evidence_text) if evidence_text else []
        missing = [term for term in required if term not in found]
        coverage = len(found) / len(required) if required else 1.0

        if not evidence_text.strip():
            status = "REVIEW_REQUIRED"
            decision = "wait_for_governance_evidence"
            reason = (
                "No document or repository evidence was supplied "
                "for inspection."
            )
        elif coverage >= 0.5:
            status = "COMPLETED"
            decision = "governance_evidence_reviewed"
            reason = (
                "Minimum declared governance concept coverage was found."
            )
        else:
            status = "REVIEW_REQUIRED"
            decision = "governance_revision_required"
            reason = (
                "Evidence does not cover the minimum declared "
                "governance concepts."
            )

        return {
            "contract_version": "1.1",
            "status": status,
            "module": self.module_name,
            "task": task,
            "role": self.mpcp_role,
            "action": "governance_review",
            "decision": decision,
            "reason": reason,
            "summary": (
                f"Governance review for {target}: "
                f"{len(found)}/{len(required)} declared concepts found."
            ),
            "target": target,
            "details": {
                "required_terms": required,
                "found_terms": found,
                "missing_terms": missing,
                "coverage_ratio": coverage,
                "merge_performed": False,
                "authority_granted": False,
                "evidence_supplied": bool(evidence_text.strip()),
                "evidence_type": type(evidence).__name__,
            },
            "artifacts": [],
            "mutated": False,
            "traceable": True,
            "review": status != "COMPLETED",
        }


__all__ = ["CopilotGmAgent"]
