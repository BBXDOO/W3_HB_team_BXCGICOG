from typing import Any, Dict

from .base import RuntimeAgent
from .cast_activity_log import log_assignment, log_subsystem_report, summarize_subsystem_health


class CastAgent(RuntimeAgent):
    module_name = "Cast"
    action_label = "completed structural adaptation / reasoning / interpretation output"
    # W3 ecosystem role: continuity + context bridge (W3LGU_MPCP_ROLE_MAPPING.md §9)
    mpcp_role = "continuity_context"
    mpcp_concepts = ["continuity", "context", "reasoning", "adaptation"]

    def execute(self, task: str, plan: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """บันทึกกิจกรรมระดับ MAIN ของ W3 — ไม่ลงลึกใน subsystem ใดๆ

        plan รองรับ 2 รูปแบบ:
          {"kind": "assignment", "module": "...", "task": "...", "assigned_by": "..."}
          {"kind": "subsystem_report", "subsystem": "...", "reported": bool, "channel": "..."}

        ถ้า plan ไม่ตรงรูปแบบใดเลย -> คืน UNAVAILABLE ตาม contract เดิม
        ของ RuntimeAgent (ไม่แกล้งทำเป็นเสร็จ)
        """
        kind = plan.get("kind")

        if kind == "assignment":
            record = log_assignment(
                module=plan.get("module", "unknown"),
                task=plan.get("task", task),
                assigned_by=plan.get("assigned_by", "unknown"),
                note=plan.get("note", ""),
            )
            return {
                "contract_version": "1.0",
                "status": "COMPLETED",
                "module": self.module_name,
                "task": task,
                "action": "log_assignment",
                "record": record,
                "artifacts": [{"type": "main_activity_record", "record": record}],
                "mutated": True,
                "traceable": True,
                "review": False,
            }

        if kind == "subsystem_report":
            record = log_subsystem_report(
                subsystem=plan.get("subsystem", "unknown"),
                reported=bool(plan.get("reported", False)),
                channel=plan.get("channel", ""),
                summary=plan.get("summary", ""),
            )
            return {
                "contract_version": "1.0",
                "status": "COMPLETED",
                "module": self.module_name,
                "task": task,
                "action": "log_subsystem_report",
                "record": record,
                "artifacts": [{"type": "main_activity_record", "record": record}],
                "mutated": True,
                "traceable": True,
                "review": False,
            }

        if kind == "health_summary":
            summary = summarize_subsystem_health()
            return {
                "contract_version": "1.0",
                "status": "COMPLETED",
                "module": self.module_name,
                "task": task,
                "action": "summarize_subsystem_health",
                "summary": summary,
                "mutated": False,
                "traceable": True,
                "review": False,
            }

        if kind in {"interpretation", "reasoning", "structural_review"}:
            request = context.get("request") if isinstance(context.get("request"), dict) else {}
            source = context.get("source") or request.get("source") or "unknown"
            observations = context.get("observations") or context.get("evidence") or []
            if not isinstance(observations, list):
                observations = [observations]
            observations = [item for item in observations if item not in (None, "")]
            assumptions = context.get("assumptions") or []
            if not isinstance(assumptions, list):
                assumptions = [assumptions]
            questions = context.get("questions") or []
            if not isinstance(questions, list):
                questions = [questions]

            return {
                "contract_version": "1.0",
                "status": "COMPLETED" if observations else "REVIEW_REQUIRED",
                "module": self.module_name,
                "task": task,
                "action": "structure_context",
                "summary": "Structured supplied observations without changing source truth.",
                "reason": (
                    "At least one supplied observation was structured for decision support."
                    if observations
                    else "Interpretation requires at least one explicit observation or evidence item."
                ),
                "details": {
                    "source": source,
                    "observations": observations,
                    "assumptions": assumptions,
                    "open_questions": questions,
                },
                "artifacts": [],
                "mutated": False,
                "traceable": True,
                "review": True,
                "authority": {"decision_allowed": False, "truth_mutation_allowed": False},
            }

        # ไม่ตรง plan ที่รู้จัก — คืน UNAVAILABLE ตาม contract เดิมของ base.py
        return super().execute(task, plan, context)
