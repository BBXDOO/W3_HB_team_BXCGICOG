from typing import Dict, Any, List

from .mpcp_reader import scan_terms, MPCP_CORE_TERMS


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
        local capability.  Returning this contract prevents the runtime from
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


class FallbackAgent(RuntimeAgent):
    module_name = "Fallback"
    action_label = "handled fallback execution"
