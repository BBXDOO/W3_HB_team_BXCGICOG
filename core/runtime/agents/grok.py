from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from .base import RuntimeAgent


class GrokAgent(RuntimeAgent):
    """
    Grok — Interpretation & Pattern Intelligence Module

    Role in W3 / WHUB foundation:
    - Pattern detection
    - Signal / insight extraction
    - Context synthesis
    - Observation-first interpretation
    - Narrative and knowledge framing

    Principles:
    - Observe before decide
    - Do not fabricate success
    - Produce real artifacts when insight is formed
    - Default: no system mutation
    """

    module_name = "Grok"
    action_label = "completed pattern scan"

    # ------------------------------------------------------------------
    # MPCP / W3Lgu Alignment
    # ------------------------------------------------------------------
    mpcp_role: str = "pattern_insight"
    mpcp_concepts: List[str] = [
        "pattern",
        "signal",
        "signals",
        "insight",
        "knowledge",
        "observation",
        "interpretation",
        "context",
        "narrative",
        "anomaly",
    ]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _now_iso(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _extract_target(self, context: Dict[str, Any]) -> str:
        return (
            context.get("target")
            or context.get("request", {}).get("target")
            or context.get("scope")
            or "W3"
        )

    def _extract_signals(self, context: Dict[str, Any]) -> List[Any]:
        signals = (
            context.get("signals")
            or context.get("records")
            or context.get("observations")
            or context.get("events")
            or []
        )
        return signals if isinstance(signals, list) else []

    def _build_observation(
        self,
        task: str,
        plan: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        responsibilities = self._responsibilities(plan)
        main_duty = (
            responsibilities[0]
            if responsibilities
            else "detect patterns and extract insight"
        )
        experience = self._experience_summary(task, context)
        signals = self._extract_signals(context)
        signal_count = len(signals)

        if signal_count >= 12:
            insight_level = "high"
        elif signal_count >= 5:
            insight_level = "medium"
        else:
            insight_level = "low"

        return {
            "main_duty": main_duty,
            "experience": experience,
            "signal_count": signal_count,
            "insight_level": insight_level,
            "target": self._extract_target(context),
            "role": plan.get("role", self.mpcp_role),
            "signals": signals,
        }

    def _build_artifacts(
        self,
        task: str,
        obs: Dict[str, Any],
        context: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Create real insight artifacts.
        These are observation/insight products, not system mutations.
        """
        artifacts: List[Dict[str, Any]] = []

        # 1) Core insight note
        insight_body = {
            "module": self.module_name,
            "task": task,
            "target": obs["target"],
            "role": obs["role"],
            "main_duty": obs["main_duty"],
            "experience": obs["experience"],
            "signal_count": obs["signal_count"],
            "insight_level": obs["insight_level"],
            "principle": "Observe → Understand → Do not rush to decide",
            "generated_at": self._now_iso(),
        }

        artifacts.append(
            {
                "type": "insight",
                "name": f"grok_insight_{task[:48].replace(' ', '_').lower()}",
                "format": "json",
                "content": insight_body,
                "mutable": False,
            }
        )

        # 2) Pattern summary (human-readable)
        pattern_summary = (
            f"[Grok Pattern Summary]\n"
            f"Task: {task}\n"
            f"Target: {obs['target']}\n"
            f"Role: {obs['role']}\n"
            f"Duty: {obs['main_duty']}\n"
            f"Signals: {obs['signal_count']}\n"
            f"Insight Level: {obs['insight_level']}\n"
            f"Experience: {obs['experience']}\n"
            f"Note: Observation completed. No system mutation performed.\n"
        )

        artifacts.append(
            {
                "type": "pattern_summary",
                "name": f"grok_pattern_{task[:48].replace(' ', '_').lower()}",
                "format": "text",
                "content": pattern_summary,
                "mutable": False,
            }
        )

        # 3) Optional narrative frame when insight is strong enough
        if obs["insight_level"] in ("medium", "high"):
            narrative = (
                f"Grok narrative frame for '{task}' on target '{obs['target']}'. "
                f"Observed {obs['signal_count']} signal(s) with insight level "
                f"'{obs['insight_level']}'. Primary interpretive duty: {obs['main_duty']}."
            )
            artifacts.append(
                {
                    "type": "narrative",
                    "name": f"grok_narrative_{task[:48].replace(' ', '_').lower()}",
                    "format": "text",
                    "content": narrative,
                    "mutable": False,
                }
            )

        return artifacts

    # ------------------------------------------------------------------
    # Legacy text interface
    # ------------------------------------------------------------------
    def run(self, task: str, plan: Dict[str, Any], context: Dict[str, Any]) -> str:
        obs = self._build_observation(task, plan, context)
        return (
            f"{self.module_name} ({obs['role']}) {self.action_label}: {task} | "
            f"target: {obs['target']} | "
            f"duty: {obs['main_duty']} | "
            f"experience: {obs['experience']} | "
            f"observation: {obs['signal_count']} signal(s), "
            f"insight_level={obs['insight_level']}"
        )

    # ------------------------------------------------------------------
    # Structured execution (with real artifacts)
    # ------------------------------------------------------------------
    def execute(
        self,
        task: str,
        plan: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Structured execution for Grok.

        Status policy:
        - OBSERVED      : observation + basic artifacts created
        - INSIGHT_READY : sufficient signals + stronger insight artifacts
        """
        obs = self._build_observation(task, plan, context)
        artifacts = self._build_artifacts(task, obs, context)

        status = "OBSERVED"
        if obs["insight_level"] in ("medium", "high"):
            status = "INSIGHT_READY"

        summary = (
            f"Grok observed task '{task}' under role '{obs['role']}'. "
            f"Primary duty: {obs['main_duty']}. "
            f"Experience: {obs['experience']}. "
            f"Signals: {obs['signal_count']}. "
            f"Insight level: {obs['insight_level']}. "
            f"Artifacts created: {len(artifacts)}."
        )

        return {
            "contract_version": "1.0",
            "status": status,
            "module": self.module_name,
            "task": task,
            "action": "pattern_insight_scan",
            "mpcp_role": self.mpcp_role,
            "mpcp_concepts": list(self.mpcp_concepts),
            "summary": summary,
            "reason": (
                "Grok completed observation and pattern framing. "
                "Insight artifacts were produced. No external system mutation was performed."
            ),
            "artifacts": artifacts,
            "mutated": False,
            "traceable": True,
            "review": True,
            "observation": {
                "target": obs["target"],
                "main_duty": obs["main_duty"],
                "experience": obs["experience"],
                "signal_count": obs["signal_count"],
                "insight_level": obs["insight_level"],
            },
            "meta": {
                "agent": self.module_name,
                "logic": "adaptive_0.5",
                "principle": "Observe → Understand → Do not rush to decide",
                "foundation": "WHUB-ready",
                "generated_at": self._now_iso(),
            },
        }

    # ------------------------------------------------------------------
    # Alignment helper
    # ------------------------------------------------------------------
    def inspect_alignment(self, doc_text: str) -> Dict[str, Any]:
        hits = self.inspect_mpcp(doc_text)
        coverage = (
            round(len(hits) / len(self.mpcp_concepts), 3)
            if self.mpcp_concepts
            else 0.0
        )
        return {
            "module": self.module_name,
            "mpcp_role": self.mpcp_role,
            "matched_concepts": hits,
            "coverage": coverage,
            "total_concepts": len(self.mpcp_concepts),
        }
