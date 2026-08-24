"""BBEX-Core: the perceptive intent layer paired with BBX19 action.

BBEX does not execute an operational task or decide whether an intent is
"right". It makes the intent explicit, preserves uncertainty, and returns a
traceable record that BBX19 or another authorized runtime can act on later.

BBEX may observe alignment signals and communicate them, but it does not turn
those observations into operational authority.  BBX19 receives consultation;
other modules receive reflective feedback rather than direct answers.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

from .base import RuntimeAgent


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _as_text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _as_list(value: Any) -> List[str]:
    if value is None:
        return []
    values = value if isinstance(value, (list, tuple, set)) else [value]
    return [text for item in values if (text := _as_text(item))]


class BBEXCore:
    """Build and optionally persist a non-executing W3 perception record."""

    contract_version = "1.1"
    module_name = "BBEX-Core"
    role = "perceptive_intent_anchor"

    def __init__(self, repo_path: Path | str, clock=_utc_now):
        self.repo_path = Path(repo_path).expanduser().resolve()
        self.clock = clock

    def capture(
        self,
        task: str,
        *,
        source: str = "BBX19",
        target: str = "W3",
        intent: Optional[str] = None,
        desired_outcome: Optional[str] = None,
        constraints: Any = None,
        non_goals: Any = None,
        evidence: Any = None,
        observations: Any = None,
        support_signals: Any = None,
        drift_signals: Any = None,
        structural_options: Any = None,
    ) -> Dict[str, Any]:
        task_text = _as_text(task)
        intent_text = _as_text(intent) or task_text
        outcome_text = _as_text(desired_outcome)
        missing = []
        if not intent_text:
            missing.append("intent")
        if not outcome_text:
            missing.append("desired_outcome")

        support = _as_list(support_signals)
        drift = _as_list(drift_signals)
        if drift:
            alignment_state = "DRIFT_REVIEW"
        elif support:
            alignment_state = "SUPPORT"
        else:
            alignment_state = "OBSERVE"

        source_text = _as_text(source) or "BBX19"
        communication_mode = "CONSULTATION" if source_text.upper() == "BBX19" else "FEEDBACK"
        state = "READY_FOR_ACTION" if not missing and not drift else "REFLECTION_REQUIRED"
        created_at = self.clock()
        identity_seed = json.dumps(
            {
                "source": source_text,
                "target": _as_text(target) or "W3",
                "intent": intent_text,
                "desired_outcome": outcome_text,
                "constraints": _as_list(constraints),
                "non_goals": _as_list(non_goals),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
        intent_id = "BBEX-" + hashlib.sha256(identity_seed.encode("utf-8")).hexdigest()[:12]

        question = (
            "What outcome would show that this intent was preserved?"
            if outcome_text
            else "What observable outcome should this intent produce?"
        )
        return {
            "contract_version": self.contract_version,
            "record_type": "w3.intent_record",
            "record_profile": "perception_memory_alignment",
            "intent_id": intent_id,
            "module": self.module_name,
            "role": self.role,
            "state": state,
            "source": source_text,
            "target": _as_text(target) or "W3",
            "task": task_text,
            "intent": intent_text,
            "desired_outcome": outcome_text,
            "constraints": _as_list(constraints),
            "non_goals": _as_list(non_goals),
            "evidence": _as_list(evidence),
            "memory": {
                "observations": _as_list(observations),
                "support_signals": support,
                "drift_signals": drift,
                "append_only_intent": True,
            },
            "alignment": {
                "state": alignment_state,
                "basis": "declared_signals_only",
                "decision": False,
            },
            "communication": {
                "mode": communication_mode,
                "counterpart": source_text,
                "structural_options": _as_list(structural_options) if communication_mode == "CONSULTATION" else [],
                "direct_operational_answer": False,
                "feedback_question": question,
            },
            "missing": missing,
            "reflection_question": question,
            "created_at": created_at,
            "execution": {
                "allowed": False,
                "performed": False,
                "reason": "BBEX perceives and preserves intent; BBX19 owns contextual decision and action.",
            },
        }

    def render_markdown(self, record: Mapping[str, Any]) -> str:
        def bullets(values: Any) -> str:
            items = _as_list(values)
            return "\n".join(f"- {item}" for item in items) if items else "- None declared"

        memory = record.get("memory", {})
        alignment = record.get("alignment", {})
        communication = record.get("communication", {})

        return f"""# BBEX Perception Record

- Intent ID: `{record['intent_id']}`
- State: `{record['state']}`
- Source: `{record['source']}`
- Target: `{record['target']}`
- Created: `{record['created_at']}`
- Alignment: `{alignment.get('state', 'OBSERVE')}`
- Communication: `{communication.get('mode', 'FEEDBACK')}`

## Intent

{record['intent'] or 'Not yet declared.'}

## Desired Outcome

{record['desired_outcome'] or 'Not yet declared.'}

## Constraints

{bullets(record.get('constraints'))}

## Non-goals

{bullets(record.get('non_goals'))}

## Evidence

{bullets(record.get('evidence'))}

## Observations

{bullets(memory.get('observations'))}

## Signals Supporting the Root Intent

{bullets(memory.get('support_signals'))}

## Possible Drift Signals

{bullets(memory.get('drift_signals'))}

## Structural Options

{bullets(communication.get('structural_options'))}

## Reflection

> {record['reflection_question']}

## Boundary

BBEX perceives, remembers, and reflects intent. With BBX19 it may provide
consultation and structural options. With other modules it provides feedback
and questions, not direct operational answers. It never executes the action,
grants approval, or replaces BBX19's contextual decision.
"""

    def save(self, record: Mapping[str, Any], output_path: Path | str) -> Path:
        target = Path(output_path).expanduser()
        if not target.is_absolute():
            target = self.repo_path / target
        target = target.resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        text = self.render_markdown(record)

        descriptor, temporary_name = tempfile.mkstemp(
            dir=str(target.parent), prefix=f".{target.name}.", suffix=".tmp"
        )
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                handle.write(text)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary_name, target)
        except BaseException:
            try:
                os.unlink(temporary_name)
            except FileNotFoundError:
                pass
            raise
        return target


class BBEXCoreAgent(RuntimeAgent):
    module_name = "BBEX-Core"
    action_label = "recorded intent perception"
    mpcp_role = "perceptive_intent_anchor"
    mpcp_concepts = ["intent", "meaning", "identity", "purpose", "context", "memory", "drift"]

    def execute(self, task: str, plan: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        request = context.get("request") if isinstance(context.get("request"), dict) else {}
        payload = context.get("payload") if isinstance(context.get("payload"), dict) else {}
        if not payload and isinstance(request.get("payload"), dict):
            payload = request["payload"]

        repo_path = Path(__file__).resolve().parents[3]
        core = BBEXCore(repo_path)
        record = core.capture(
            task,
            source=context.get("source") or request.get("source") or "BBX19",
            target=context.get("target") or request.get("target") or "W3",
            intent=payload.get("intent") or request.get("intent") or task,
            desired_outcome=payload.get("desired_outcome") or request.get("desired_outcome"),
            constraints=payload.get("constraints") or request.get("constraints"),
            non_goals=payload.get("non_goals") or request.get("non_goals"),
            evidence=payload.get("evidence") or request.get("evidence"),
            observations=payload.get("observations") or request.get("observations"),
            support_signals=payload.get("support_signals") or request.get("support_signals"),
            drift_signals=payload.get("drift_signals") or request.get("drift_signals"),
            structural_options=payload.get("structural_options") or request.get("structural_options"),
        )

        artifacts: List[Dict[str, Any]] = []
        mutated = False
        if context.get("persist_intent") is True:
            relative = Path("modules/BBEX-Core/reflections") / f"{record['intent_id']}.md"
            saved = core.save(record, relative)
            artifacts.append({"kind": "w3.intent_record.markdown", "path": str(saved.relative_to(repo_path))})
            mutated = True

        return {
            "contract_version": "1.1",
            "status": "COMPLETED" if record["state"] == "READY_FOR_ACTION" else "REVIEW_REQUIRED",
            "module": self.module_name,
            "task": task,
            "action": "intent_perception_recorded",
            "summary": "BBEX recorded intent, memory, and alignment signals without deciding or executing.",
            "intent_record": record,
            "artifacts": artifacts,
            "mutated": mutated,
            "traceable": True,
            "review": True,
        }
