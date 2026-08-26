from collections.abc import Mapping
from typing import Dict, Any

from .base import RuntimeAgent


class CopilotGmAgent(RuntimeAgent):
    module_name = "Copilot-Gm"
    action_label = "completed governance review"
    # W3 ecosystem role: governance / structural consistency (W3LGU_MPCP_ROLE_MAPPING.md §9)
    mpcp_role = "governance"
    mpcp_concepts = ["governance", "policy", "compliance", "structural consistency"]

    def _review_required(
        self,
        task: Any,
        reason: str,
        decision: str,
        *,
        preload: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        result = {
            "contract_version": "1.2",
            "status": "REVIEW_REQUIRED",
            "module": self.module_name,
            "task": str(task or ""),
            "role": self.mpcp_role,
            "action": "governance_concept_coverage_review",
            "decision": decision,
            "summary": "Copilot-Gm did not complete the governance coverage review.",
            "reason": reason,
            "preload": preload or {
                "context_valid": False,
                "notes_count": 0,
                "decisions_count": 0,
                "expectations_count": 0,
                "has_progress": False,
            },
            "result": {
                "required_terms": list(self.mpcp_concepts),
                "found_terms": [],
                "missing_terms": list(self.mpcp_concepts),
                "coverage_ratio": 0.0,
                "min_coverage": 0.5,
            },
            "details": {
                "governance_scope": "concept_coverage_only",
                "merge_performed": False,
                "authority_granted": False,
                "evidence_supplied": False,
                "evidence_type": "none",
            },
            "artifacts": [],
            "mutated": False,
            "traceable": True,
            "review": True,
            "authority": {
                "decision_allowed": False,
                "merge_allowed": False,
                "truth_mutation_allowed": False,
            },
        }
        result["evidence"] = self.collect_evidence({}, {}, {}, result)
        result["reflection"] = self.reflect(str(task or ""), {}, {}, result)
        result["continuity"] = self.persist_continuity(
            str(task or ""), {}, {}, result, result["reflection"]
        )
        return result

    def execute(self, task: str, plan: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Governance executor (MVP):
        - checks concept coverage in doc_text
        - returns traceable, non-fabricated status
        - includes reflection + continuity packet
        """
        if not isinstance(plan, Mapping) or not isinstance(context, Mapping):
            return self._review_required(
                task,
                "plan and context must be mappings",
                "invalid_review_input",
            )
        plan = dict(plan)
        context = dict(context)

        preload = self.preload_context(task, plan, context)
        raw_review_material = self.resolve_context_value(
            context, "doc_text", "text", "evidence", "artifacts"
        )
        doc_text = self.normalize_review_text(raw_review_material)
        target = self.resolve_context_value(context, "target") or "W3"
        responsibilities = self._responsibilities(plan)

        if not doc_text:
            return self._review_required(
                task,
                "Governance review requires explicit document text or supporting evidence.",
                "missing_governance_evidence",
                preload=preload,
            )

        required_terms = list(self.mpcp_concepts)
        found_terms = self.inspect_mpcp(doc_text)
        missing_terms = [t for t in required_terms if t not in found_terms]

        raw_min_coverage = plan.get("min_coverage", 0.5)
        try:
            min_coverage = float(raw_min_coverage)
        except (TypeError, ValueError):
            min_coverage = 0.5
        # Zero coverage must never be sufficient evidence of a completed review.
        min_coverage = max(0.25, min(1.0, min_coverage))

        coverage_ratio = (len(found_terms) / len(required_terms)) if required_terms else 1.0
        completed = coverage_ratio >= min_coverage
        status = "COMPLETED" if completed else "REVIEW_REQUIRED"

        summary = (
            f"{self.module_name} governance review on {target}: "
            f"{len(found_terms)}/{len(required_terms)} concept coverage "
            f"({coverage_ratio:.0%}, threshold={min_coverage:.0%})"
        )

        result = {
            "contract_version": "1.2",
            "status": status,
            "module": self.module_name,
            "task": task,
            "role": self.mpcp_role,
            "action": "governance_concept_coverage_review",
            "decision": "COVERAGE_ACCEPTED" if completed else "COVERAGE_INCOMPLETE",
            "summary": summary,
            "target": target,
            "responsibilities": responsibilities,
            "preload": preload,
            "result": {
                "required_terms": required_terms,
                "found_terms": found_terms,
                "missing_terms": missing_terms,
                "coverage_ratio": coverage_ratio,
                "min_coverage": min_coverage,
            },
            "details": {
                "governance_scope": "concept_coverage_only",
                "merge_performed": False,
                "authority_granted": False,
                "evidence_supplied": True,
                "evidence_type": type(raw_review_material).__name__,
            },
            "artifacts": [
                {
                    "type": "governance_review",
                    "label": f"{self.module_name} concept coverage",
                    "evidence": {
                        "terms_scanned": required_terms,
                        "terms_found": found_terms,
                        "terms_missing": missing_terms,
                    },
                }
            ],
            "mutated": False,
            "traceable": True,
            "review": not completed,
            "authority": {
                "decision_allowed": False,
                "merge_allowed": False,
                "truth_mutation_allowed": False,
            },
        }

        result["evidence"] = [
            {
                "type": "review_input",
                "evidence_class": "input_evidence",
                "label": "Normalized governance review material",
                "value_type": type(raw_review_material).__name__,
                "present": True,
            }
        ] + self.collect_evidence(task, plan, context, result)
        result["reflection"] = self.reflect(task, plan, context, result)
        result["continuity"] = self.persist_continuity(
            task, plan, context, result, result["reflection"]
        )
        return result
