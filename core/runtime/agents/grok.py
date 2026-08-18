from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from .base import RuntimeAgent


class GrokAgent(RuntimeAgent):
    """Local, review-first insight/pattern artifact executor for the Grok role.

    This class does not claim to call an external model. Its local capability
    is deliberately concrete: turn the routed task plus supplied context into
    a traceable Markdown insight/pattern artifact inside the Grok module
    workspace.
    """

    module_name = "Grok"
    action_label = "completed pattern scan"

    # W3 ecosystem role: pattern / signals / insight
    mpcp_role = "pattern_insight"
    mpcp_concepts = [
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

    _REPO_ROOT = Path(__file__).resolve().parents[3]
    _DEFAULT_INSIGHT_DIR = _REPO_ROOT / "modules" / "Grok" / "insights"
    _SECRET_KEYWORDS = (
        "token",
        "secret",
        "password",
        "api_key",
        "apikey",
        "authorization",
        "cookie",
        "private_key",
        "credential",
    )

    def execute(
        self,
        task: str,
        plan: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Create a real local insight/pattern artifact and return its record."""
        normalized_task = str(task).strip()
        if not normalized_task:
            return {
                "contract_version": "1.0",
                "status": "REJECTED",
                "module": self.module_name,
                "task": task,
                "summary": (
                    "A non-empty task is required before an insight artifact "
                    "can be created."
                ),
                "artifacts": [],
                "mutated": False,
                "review": True,
            }

        request = (
            context.get("request")
            if isinstance(context.get("request"), dict)
            else {}
        )
        payload = (
            context.get("payload")
            if isinstance(context.get("payload"), dict)
            else {}
        )
        if not payload and isinstance(request.get("payload"), dict):
            payload = request["payload"]

        signals = self._extract_signals(context)
        experience = self._experience_summary(normalized_task, context)
        responsibilities = self._responsibilities(plan)
        main_duty = (
            responsibilities[0]
            if responsibilities
            else "detect patterns and extract insight"
        )

        insight_level = self._insight_level(len(signals))
        trace_id = str(context.get("trace_id") or uuid.uuid4().hex)

        insight_dir = self._insight_dir()
        insight_dir.mkdir(parents=True, exist_ok=True)

        artifact_path = insight_dir / self._artifact_name(
            normalized_task,
            trace_id,
        )
        artifact_text = self._render_insight_artifact(
            task=normalized_task,
            plan=plan,
            context=context,
            request=request,
            payload=payload,
            signals=signals,
            experience=experience,
            main_duty=main_duty,
            insight_level=insight_level,
            trace_id=trace_id,
        )
        self._atomic_write(artifact_path, artifact_text)

        digest = hashlib.sha256(
            artifact_text.encode("utf-8")
        ).hexdigest()
        artifact_ref = {
            "path": self._display_path(artifact_path),
            "sha256": digest,
            "bytes": len(artifact_text.encode("utf-8")),
            "kind": "w3.insight_artifact.markdown",
        }

        return {
            "contract_version": "1.0",
            "status": "COMPLETED",
            "module": self.module_name,
            "task": normalized_task,
            "capability": "local_insight_artifact",
            "trace_id": trace_id,
            "mpcp_role": self.mpcp_role,
            "summary": (
                "Created a local insight/pattern artifact from the routed "
                "task and context. No remote model, network call, or external "
                "executor was used."
            ),
            "artifacts": [artifact_ref],
            "mutated": True,
            "mutation_scope": [self._display_path(insight_dir)],
            "external_execution_allowed": False,
            "review": True,
            "observation": {
                "signal_count": len(signals),
                "insight_level": insight_level,
                "experience": experience,
                "main_duty": main_duty,
            },
            "limitations": [
                (
                    "This is a deterministic local interpreter, not an "
                    "external model invocation."
                ),
                (
                    "The generated insight remains a draft and requires "
                    "human review before downstream use."
                ),
            ],
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _extract_signals(
        self,
        context: Dict[str, Any],
    ) -> List[Any]:
        signals = (
            context.get("signals")
            or context.get("records")
            or context.get("observations")
            or context.get("events")
            or []
        )
        return signals if isinstance(signals, list) else []

    def _insight_level(self, signal_count: int) -> str:
        if signal_count >= 12:
            return "high"
        if signal_count >= 5:
            return "medium"
        return "low"

    def _insight_dir(self) -> Path:
        override = os.environ.get("W3_GROK_INSIGHT_DIR")
        if override:
            return Path(override).expanduser().resolve()
        return self._DEFAULT_INSIGHT_DIR

    def _artifact_name(self, task: str, trace_id: str) -> str:
        slug = (
            re.sub(r"[^a-z0-9]+", "-", task.lower()).strip("-")
            or "task"
        )
        safe_trace = (
            re.sub(r"[^a-zA-Z0-9]", "", trace_id)[:12]
            or "trace"
        )
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        return f"{stamp}_{slug[:48]}_{safe_trace}.md"

    def _render_insight_artifact(
        self,
        *,
        task: str,
        plan: Dict[str, Any],
        context: Dict[str, Any],
        request: Dict[str, Any],
        payload: Dict[str, Any],
        signals: List[Any],
        experience: str,
        main_duty: str,
        insight_level: str,
        trace_id: str,
    ) -> str:
        target = (
            context.get("target")
            or request.get("target")
            or "W3"
        )
        source = (
            context.get("source")
            or request.get("source")
            or "unspecified"
        )
        intent = request.get("intent") or payload.get("intent") or task
        role = plan.get("role", self.mpcp_role)

        responsibilities = plan.get("responsibilities") or []
        if not isinstance(responsibilities, list):
            responsibilities = [str(responsibilities)]

        safe_payload = self._redact(payload)
        payload_json = json.dumps(
            safe_payload,
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )

        request_file = request.get("_request_file")
        timestamp = (
            datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        )

        responsibility_lines = "\n".join(
            f"- {item}"
            for item in responsibilities
            if str(item).strip()
        ) or "- No responsibility was supplied by the routed identity profile."

        request_file_line = (
            f"- Request file: `{request_file}`\n"
            if request_file
            else ""
        )

        signal_preview = json.dumps(
            self._redact(signals[:8]),
            indent=2,
            ensure_ascii=False,
        )

        return f"""# W3 Local Insight Artifact

## Trace
- Trace ID: `{trace_id}`
- Created at: `{timestamp}`
- Module: `{self.module_name}`
- Capability: `local_insight_artifact`
- Review required: `true`

## Request
- Task: `{task}`
- Intent: {intent}
- Source: `{source}`
- Target: `{target}`
{request_file_line}
## Routed Plan
- Role: `{role}`
- Assigned module: `{plan.get('run_with', self.module_name)}`
- Plan status: `{plan.get('status', 'ACTIVE')}`
- Main duty: `{main_duty}`

### Responsibilities
{responsibility_lines}

## Observation
- Experience context: {experience}
- Signal count: `{len(signals)}`
- Insight level: `{insight_level}`
- Principle: Observe → Understand → Do not rush to decide

## Local Interpretation Flow
1. Receive the routed task and request context.
2. Observe available signals/records without forcing a decision.
3. Frame patterns and insight candidates.
4. Produce this reviewable insight artifact in the Grok module workspace.
5. Route to human/governance review before downstream action.

## Signal Preview (redacted, capped)
```json
{signal_preview}
```

## Request Payload (redacted)
```json
{payload_json}
```

## Boundary
- Observation does not become final truth.
- No external model, network call, merge, or deployment was executed.
- Human/governance review remains required.
"""

    def _redact(self, value: Any) -> Any:
        if isinstance(value, dict):
            cleaned = {}
            for key, child in value.items():
                key_text = str(key)
                if any(
                    keyword in key_text.lower()
                    for keyword in self._SECRET_KEYWORDS
                ):
                    cleaned[key_text] = "[REDACTED]"
                else:
                    cleaned[key_text] = self._redact(child)
            return cleaned

        if isinstance(value, list):
            return [self._redact(item) for item in value]

        return value

    @staticmethod
    def _atomic_write(path: Path, content: str) -> None:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            delete=False,
            dir=path.parent,
        ) as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
            temporary_path = Path(handle.name)

        temporary_path.replace(path)

    def _display_path(self, path: Path) -> str:
        try:
            return str(path.relative_to(self._REPO_ROOT))
        except ValueError:
            return str(path)


__all__ = ["GrokAgent"]
