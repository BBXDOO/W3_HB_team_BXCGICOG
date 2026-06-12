from typing import Any, Dict, List
from pathlib import Path
import json

from .base import RuntimeAgent
from core.memory.stats import memory_stats


ROOT = Path(__file__).resolve().parents[3]
IDENTITY_DIR = ROOT / "core" / "module-loader" / "identity"


class LRC2Agent(RuntimeAgent):
    module_name = "LRC2"
    action_label = "completed lifecycle review checkpoint"
    mpcp_role = "lifecycle_review"
    mpcp_concepts = ["lifecycle", "checkpoint", "review", "compliance", "memory", "system"]

    def _load_target_identity(self, target: str) -> Dict[str, Any]:
        path = IDENTITY_DIR / f"{target}.idp.json"

        if not path.exists():
            return {"found": False, "path": str(path), "note": "target identity file not found"}

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return {"found": True, "path": str(path), "data": data}
        except Exception as exc:
            return {"found": False, "path": str(path), "note": str(exc)}

    def _identity_text(self, target: str) -> str:
        identity = self._load_target_identity(target)

        if not identity["found"]:
            return f"identity=missing note={identity['note']}"

        idp = identity["data"]
        inner = idp.get("identity", {})
        designation = inner.get("designation") or idp.get("designation") or "unknown"
        status = inner.get("status") or idp.get("status") or "unknown"

        return f"identity=found designation={designation} status={status}"

    def _module_line(self, target: str) -> str:
        mem = memory_stats(target)
        ident = self._identity_text(target)

        return (
            f"{target}: "
            f"{ident} "
            f"memory_total={mem['total']} "
            f"success={mem['success']} "
            f"failed={mem['failed']} "
            f"health={mem['health']} "
            f"confidence={mem['confidence']} "
            f"trend={mem['trend']} "
            f"top_patterns={mem['top_patterns']}"
        )

    def _system_review(self, focus: str) -> str:
        modules: List[str] = ["REDR", "DTML", "LRC2", "PSP2"]
        lines = []
        healthy = 0
        warning = 0
        critical = 0
        unknown = 0
        total_memory = 0
        total_failed = 0

        for name in modules:
            mem = memory_stats(name)
            total_memory += mem["total"]
            total_failed += mem["failed"]

            if mem["health"] == "HEALTHY":
                healthy += 1
            elif mem["health"] == "WARNING":
                warning += 1
            elif mem["health"] == "CRITICAL":
                critical += 1
            else:
                unknown += 1

            lines.append(self._module_line(name))

        if critical > 0:
            system_status = "CRITICAL"
        elif warning > 0:
            system_status = "WATCH"
        elif healthy >= 3 and total_memory > 0:
            system_status = "STABLE"
        elif total_memory > 0:
            system_status = "FORMING"
        else:
            system_status = "NO_MEMORY"

        return (
            f"W3_SYSTEM_REVIEW focus={focus} "
            f"modules={len(modules)} "
            f"healthy={healthy} warning={warning} critical={critical} unknown={unknown} "
            f"total_memory={total_memory} total_failed={total_failed} "
            f"system_status={system_status} | "
            + " | ".join(lines)
        )

    def _single_review(self, task: str, plan: Dict[str, Any], context: Dict[str, Any]) -> str:
        role = plan.get("role", "—")

        request = context.get("request", {})
        target = context.get("target") or request.get("target") or "W3"
        payload = context.get("payload") or request.get("payload", {})
        focus = request.get("focus") or payload.get("focus") or "general"

        target_upper = str(target).upper()
        focus_lower = str(focus).lower()

        experience = self._experience_summary(task, context)
        memory = memory_stats(target_upper)

        target_duties = {
            "REDR": "review risk routing, escalation path, intake decision, and cross signal safety",
            "DTML": "review decision trace, law trigger, verification chain, and boundary judgment",
            "LRC2": "review memory integrity, checkpoint history, lifecycle trace, and reuse pattern",
            "PSP2": "review package handoff, routing compression, dispatch accuracy, and transfer state",
            "W3": "review whole W3 lifecycle, cross boundary, runtime health, and memory continuity",
        }

        focus_notes = {
            "risk": "focus on risk chain and failure boundary",
            "signal": "focus on cross signal, traceability, and mutation status",
            "memory": "focus on memory reuse, record integrity, and lifecycle recall",
            "law": "focus on law trigger, decision rule, and verification boundary",
            "route": "focus on routing path, handoff, and module assignment",
            "system": "focus on cross-system health, module continuity, and city-level review",
            "general": "focus on overall lifecycle review",
        }

        duty = target_duties.get(target_upper, f"review target-specific lifecycle behavior for {target}")
        focus_note = focus_notes.get(focus_lower, f"focus on {focus}")
        identity_text = self._identity_text(target_upper)

        memory_text = (
            f"memory: "
            f"total={memory['total']} "
            f"success={memory['success']} "
            f"failed={memory['failed']} "
            f"runtime={memory['runtime']} "
            f"top_sources={memory['top_sources']} "
            f"top_patterns={memory['top_patterns']} "
            f"top_tags={memory['top_tags']} "
            f"confidence={memory['confidence']} "
            f"health={memory['health']} "
            f"trend={memory['trend']} "
            f"first_seen={memory['first_seen']} "
            f"last_seen={memory['last_seen']} "
            f"age_seconds={memory['age_seconds']}"
        )

        report = (
            f"historical_review: "
            f"target={target_upper} "
            f"focus={focus_lower} "
            f"evidence={memory['total']} "
            f"confidence={memory['confidence']} "
            f"health={memory['health']} "
            f"trend={memory['trend']}"
        )

        return (
            f"{self.module_name} ({role}) {self.action_label}: {task} | "
            f"target: {target} | "
            f"focus: {focus} | "
            f"duty: {duty} | "
            f"{focus_note} | "
            f"{identity_text} | "
            f"{memory_text} | "
            f"{report} | "
            f"experience: {experience}"
        )

    def run(self, task: str, plan: Dict[str, Any], context: Dict[str, Any]) -> str:
        request = context.get("request", {})
        target = context.get("target") or request.get("target") or "W3"
        payload = context.get("payload") or request.get("payload", {})
        focus = request.get("focus") or payload.get("focus") or "general"

        if str(target).upper() == "W3" and str(focus).lower() == "system":
            return self._system_review(str(focus).lower())

        return self._single_review(task, plan, context)
