import json
from collections.abc import Mapping
from typing import Dict, Any, List

from .mpcp_reader import scan_terms


class RuntimeAgent:
    module_name = "Fallback"
    action_label = "processed"

    # MPCP / W3Lgu concept alignment (W3LGU_MPCP_ROLE_MAPPING.md §4 / §9)
    # Subclasses override these to declare their position in the W3 ecosystem.
    # mpcp_role  — short label matching the role mapping document
    # mpcp_concepts — key concept words the agent is responsible for;
    #                 used by inspect_mpcp() to verify concept-document coverage
    mpcp_role: str = "operational"
    mpcp_concepts: List[str] = []

    @staticmethod
    def _mapping(value: Any) -> Dict[str, Any]:
        """Return a shallow mapping copy or an empty fail-safe container."""
        return dict(value) if isinstance(value, Mapping) else {}

    @classmethod
    def resolve_context_value(cls, context: Any, *names: str) -> Any:
        """Resolve a field without forcing every ENV to use one nesting shape.

        Direct context has precedence, followed by payload, request, and a
        payload nested under request.  This resolves transport shape only; it
        does not grant authority or reinterpret the field's meaning.
        """
        direct = cls._mapping(context)
        request = cls._mapping(direct.get("request"))
        payload = cls._mapping(direct.get("payload"))
        request_payload = cls._mapping(request.get("payload"))
        for container in (direct, payload, request, request_payload):
            for name in names:
                if name in container:
                    return container[name]
        return None

    @staticmethod
    def normalize_review_text(value: Any) -> str:
        """Create deterministic review text from scalar or structured input."""
        if value is None:
            return ""
        if isinstance(value, str):
            return value.strip()
        if isinstance(value, bytes):
            return value.decode("utf-8", errors="replace").strip()
        if isinstance(value, (Mapping, list, tuple, set)):
            serializable = sorted(value, key=str) if isinstance(value, set) else value
            try:
                return json.dumps(serializable, ensure_ascii=False, sort_keys=True, default=str)
            except (TypeError, ValueError):
                return str(value).strip()
        return str(value).strip()

    def inspect_mpcp(self, doc_text: str) -> List[str]:
        """
        Return the subset of this agent's *mpcp_concepts* that appear in
        *doc_text* (case-insensitive substring match).

        Agents call this against MPCP concept documents to verify that the
        documents mention their responsibilities — a lightweight alignment
        check without heavy schema machinery.
        """
        if not self.mpcp_concepts:
            return []
        terms_set = frozenset(self.mpcp_concepts)
        return scan_terms(doc_text, terms_set)

    def _responsibilities(self, plan: Dict[str, Any]) -> List[str]:
        duties = plan.get("responsibilities") or []
        return [str(x) for x in duties if x]

    def _experience_summary(self, task: str, context: Dict[str, Any]) -> str:
        records = context.get("records") or []
        if not records:
            return "0 prior matches"

        same_module = [r for r in records if r.get("source") == self.module_name]
        same_task = [r for r in records if r.get("topic") == task]
        learned_topics = sorted({str(r.get("topic")) for r in records if r.get("topic")})

        if learned_topics:
            hint = ", ".join(learned_topics[:2])
        else:
            hint = "historical traces"

        return (
            f"{len(records)} prior matches, "
            f"{len(same_module)} from {self.module_name}, "
            f"{len(same_task)} similar task(s), reuse: {hint}"
        )

    def run(self, task: str, plan: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Legacy text summary retained for compatibility with existing callers."""
        role = plan.get("role", "—")
        responsibilities = self._responsibilities(plan)
        main_duty = responsibilities[0] if responsibilities else "execute assigned task"
        experience = self._experience_summary(task, context)

        target = context.get("target") or context.get("request", {}).get("target") or "W3"

        return (
            f"{self.module_name} ({role}) {self.action_label}: {task} | "
            f"target: {target} | duty: {main_duty} | experience: {experience}"
        )

    def execute(self, task: str, plan: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Return an explicit non-success result until a real executor exists.

        A module may be registered and routable without having an executable
        local capability. Returning this contract prevents the runtime from
        reporting a fabricated successful completion.
        """
        return {
            "contract_version": "1.0",
            "status": "UNAVAILABLE",
            "module": self.module_name,
            "task": task,
            "action": "no_local_executor",
            "summary": (
                f"{self.module_name} has no local executor registered for '{task}'. "
                "No task was completed and no artifact was created."
            ),
            "reason": "Implement a module-specific execute() method before this task can report COMPLETED.",
            "artifacts": [],
            "mutated": False,
            "traceable": True,
            "review": True,
        }

    # -----------------------------
    # Continuity hooks (MVP)
    # -----------------------------
    def preload_context(self, task: str, plan: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Read-before-guess hook:
        Pull lightweight memory from context if available.
        Runtime/dispatcher can inject these fields from notes/progress later.
        """
        valid_context = isinstance(context, Mapping)
        notes = self.resolve_context_value(context, "notes") or []
        decisions = self.resolve_context_value(context, "decisions") or []
        expectations = self.resolve_context_value(context, "expectations") or []
        progress = self.resolve_context_value(context, "progress") or {}

        if not isinstance(notes, list):
            notes = [notes]
        if not isinstance(decisions, list):
            decisions = [decisions]
        if not isinstance(expectations, list):
            expectations = [expectations]
        if not isinstance(progress, dict):
            progress = {"raw": progress}

        return {
            "context_valid": valid_context,
            "notes_count": len(notes),
            "decisions_count": len(decisions),
            "expectations_count": len(expectations),
            "has_progress": bool(progress),
        }

    def collect_evidence(
        self,
        task: str,
        plan: Dict[str, Any],
        context: Dict[str, Any],
        result: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Evidence-first hook:
        Gather execution trace. Input evidence must remain separately labeled
        by the module so a self-generated status is never treated as proof.
        """
        evidence: List[Dict[str, Any]] = []
        if result.get("summary"):
            evidence.append(
                {
                    "type": "summary",
                    "evidence_class": "execution_trace",
                    "label": f"{self.module_name} summary",
                    "value": result["summary"],
                }
            )
        if result.get("status"):
            evidence.append(
                {
                    "type": "status",
                    "evidence_class": "execution_trace",
                    "label": f"{self.module_name} status",
                    "value": result["status"],
                }
            )
        return evidence

    def reflect(
        self,
        task: str,
        plan: Dict[str, Any],
        context: Dict[str, Any],
        result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Learn hook:
        Produce compact reflection payload for notes/reflections.
        """
        return {
            "module": self.module_name,
            "task": task,
            "status": result.get("status"),
            "insight": result.get("summary", "no summary"),
            "next_attention": "verify missing evidence and continue iteration",
        }

    def persist_continuity(
        self,
        task: str,
        plan: Dict[str, Any],
        context: Dict[str, Any],
        result: Dict[str, Any],
        reflection: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Continue hook:
        Build a normalized continuity packet for a storage layer to persist.
        This method does not claim that persistence already occurred.
        """
        return {
            "persisted": False,
            "persistence_owner": "dispatcher_or_storage_layer",
            "progress_entry": {
                "module": self.module_name,
                "task": task,
                "status": result.get("status"),
                "mutated": result.get("mutated", False),
            },
            "reflection_entry": reflection,
            "next_step": (
                result.get("next_step")
                or result.get("recommendation")
                or result.get("reason")
                or "continue with next controlled iteration"
            ),
        }


class FallbackAgent(RuntimeAgent):
    module_name = "Fallback"
    action_label = "handled fallback execution"
