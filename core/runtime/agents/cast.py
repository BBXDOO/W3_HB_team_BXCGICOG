from typing import Any, Dict

from .base import RuntimeAgent
from cast_activity_log import log_assignment, log_subsystem_report, summarize_subsystem_health


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
                "mutated": False,
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
                "mutated": False,
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
                "review": False,
            }

        # ไม่ตรง plan ที่รู้จัก — คืน UNAVAILABLE ตาม contract เดิมของ base.py
        return super().execute(task, plan, context)
