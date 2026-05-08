from typing import Dict, Any, List


class RuntimeAgent:
    module_name = "Fallback"
    action_label = "processed"

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
        role = plan.get("role", "—")
        responsibilities = self._responsibilities(plan)
        main_duty = responsibilities[0] if responsibilities else "execute assigned task"
        experience = self._experience_summary(task, context)

        return (
            f"{self.module_name} ({role}) {self.action_label}: {task} | "
            f"duty: {main_duty} | experience: {experience}"
        )


class FallbackAgent(RuntimeAgent):
    module_name = "Fallback"
    action_label = "handled fallback execution"
