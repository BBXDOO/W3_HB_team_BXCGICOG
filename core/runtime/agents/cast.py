from collections.abc import Mapping
from typing import Any, Dict

from .base import RuntimeAgent
from .cast_activity_log import log_assignment, log_subsystem_report, summarize_subsystem_health


class CastAgent(RuntimeAgent):
    module_name = "Cast"
    action_label = "completed structural adaptation / reasoning / interpretation output"
    # W3 ecosystem role: continuity + context bridge (W3LGU_MPCP_ROLE_MAPPING.md §9)
    mpcp_role = "continuity_context"
    mpcp_concepts = ["continuity", "context", "reasoning", "adaptation"]

    @staticmethod
    def _reported_value(value: Any) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"true", "1", "yes", "reported"}:
                return True
            if normalized in {"false", "0", "no", "silent", "missing", ""}:
                return False
        if value in {0, 1}:
            return bool(value)
        raise ValueError("reported must be a boolean or an explicit boolean string")

    def _review_required(self, task: Any, reason: str, action: str) -> Dict[str, Any]:
        return {
            "contract_version": "1.1",
            "status": "REVIEW_REQUIRED",
            "module": self.module_name,
            "task": str(task or ""),
            "role": self.mpcp_role,
            "action": action,
            "decision": "input_or_runtime_review_required",
            "reason": reason,
            "summary": "Cast did not record or complete the requested activity.",
            "artifacts": [],
            "mutated": False,
            "traceable": True,
            "review": True,
            "authority": {"decision_allowed": False, "truth_mutation_allowed": False},
        }

    def execute(self, task: str, plan: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """บันทึกกิจกรรมระดับ MAIN ของ W3 — ไม่ลงลึกใน subsystem ใดๆ

        plan รองรับ 2 รูปแบบ:
          {"kind": "assignment", "module": "...", "task": "...", "assigned_by": "..."}
          {"kind": "subsystem_report", "subsystem": "...", "reported": bool, "channel": "..."}

        ถ้า plan ไม่ตรงรูปแบบใดเลย -> คืน UNAVAILABLE ตาม contract เดิม
        ของ RuntimeAgent (ไม่แกล้งทำเป็นเสร็จ)
        """
        if not isinstance(plan, Mapping):
            return self._review_required(task, "plan must be a mapping", "validate_plan")
        if not isinstance(context, Mapping):
            return self._review_required(task, "context must be a mapping", "validate_context")

        task_name = str(task or "").strip().lower()
        inferred_kind = (
            "reasoning"
            if task_name in {"reason", "reasoning", "interpret", "interpretation"}
            else ""
        )
        kind = str(plan.get("kind") or inferred_kind).strip()
        log_path = context.get("cast_log_path")

        if kind == "assignment":
            module = str(plan.get("module") or "").strip()
            assigned_task = str(plan.get("task") or task or "").strip()
            if not module or not assigned_task:
                return self._review_required(
                    task, "assignment requires explicit module and task", "log_assignment"
                )
            try:
                record = log_assignment(
                    module=module,
                    task=assigned_task,
                    assigned_by=str(plan.get("assigned_by") or "unknown"),
                    note=str(plan.get("note") or ""),
                    path=log_path,
                )
            except (OSError, TypeError, ValueError) as exc:
                return self._review_required(task, f"Cast log write failed: {exc}", "log_assignment")
            return {
                "contract_version": "1.1",
                "status": "COMPLETED",
                "module": self.module_name,
                "task": task,
                "action": "log_assignment",
                "record": record,
                "artifacts": [{"type": "main_activity_record", "path": record["log_path"], "record": record}],
                "mutated": True,
                "traceable": True,
                "review": False,
            }

        if kind == "subsystem_report":
            subsystem = str(plan.get("subsystem") or "").strip()
            if not subsystem or "reported" not in plan:
                return self._review_required(
                    task,
                    "subsystem_report requires explicit subsystem and reported fields",
                    "log_subsystem_report",
                )
            try:
                reported = self._reported_value(plan.get("reported"))
                record = log_subsystem_report(
                    subsystem=subsystem,
                    reported=reported,
                    channel=str(plan.get("channel") or ""),
                    summary=str(plan.get("summary") or ""),
                    path=log_path,
                )
            except (OSError, TypeError, ValueError) as exc:
                return self._review_required(task, f"Cast report write failed: {exc}", "log_subsystem_report")
            return {
                "contract_version": "1.1",
                "status": "COMPLETED",
                "module": self.module_name,
                "task": task,
                "action": "log_subsystem_report",
                "record": record,
                "artifacts": [{"type": "main_activity_record", "path": record["log_path"], "record": record}],
                "mutated": True,
                "traceable": True,
                "review": False,
            }

        if kind == "health_summary":
            try:
                summary = summarize_subsystem_health(path=log_path)
            except (OSError, TypeError, ValueError) as exc:
                return self._review_required(task, f"Cast log read failed: {exc}", "summarize_subsystem_health")
            return {
                "contract_version": "1.1",
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
            request = context.get("request") if isinstance(context.get("request"), Mapping) else {}
            payload = context.get("payload") if isinstance(context.get("payload"), Mapping) else {}
            if not payload and isinstance(request.get("payload"), Mapping):
                payload = request["payload"]
            source = context.get("source") or request.get("source") or "unknown"
            observations = (
                context.get("observations")
                or context.get("evidence")
                or payload.get("observations")
                or payload.get("evidence")
                or context.get("records")
                or []
            )
            if not isinstance(observations, list):
                observations = [observations]
            observations = [item for item in observations if item not in (None, "")]
            assumptions = context.get("assumptions") or payload.get("assumptions") or []
            if not isinstance(assumptions, list):
                assumptions = [assumptions]
            questions = context.get("questions") or payload.get("questions") or []
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
