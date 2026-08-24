from __future__ import annotations

from typing import Any, Dict

from codex.agent import build_execution_packet

from .base import RuntimeAgent


class CodexAgent(RuntimeAgent):
    """Runtime bridge for approved implementation intake, never final authority."""

    module_name = "Codex"
    action_label = "prepared implementation packet"
    mpcp_role = "implementation_executor"
    mpcp_concepts = ["implementation", "adapter", "test", "review", "governance"]

    def execute(self, task: str, plan: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        request = context.get("request") if isinstance(context.get("request"), dict) else {}
        source = str(context.get("source") or request.get("source") or "BBX19")
        target = str(context.get("target") or request.get("target") or "repository")
        mode = str(context.get("mode") or request.get("mode") or "implementation")
        intent = str(request.get("intent") or task).strip()

        if not intent:
            return {
                "contract_version": "1.0", "status": "REVIEW_REQUIRED",
                "module": self.module_name, "task": task, "action": "reject_empty_intent",
                "reason": "Codex requires an explicit implementation intent.", "artifacts": [],
                "mutated": False, "traceable": True, "review": True,
            }

        packet = build_execution_packet(intent, source=source, target=target, mode=mode)
        return {
            "contract_version": "1.0",
            "status": "REVIEW_REQUIRED",
            "module": self.module_name,
            "task": task,
            "action": "prepare_implementation_packet",
            "summary": "Prepared a traceable implementation packet for human and governance review.",
            "reason": "Preparation is not execution approval, truth mutation, or merge authority.",
            "artifacts": [{"type": "codex_execution_packet", "packet": packet.as_dict()}],
            "mutated": False,
            "traceable": True,
            "review": True,
            "authority": {
                "truth_mutation_allowed": False,
                "self_merge_allowed": False,
                "final_decision_holder": "BBX19",
            },
        }
