from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from .base import RuntimeAgent


class ChatGPTAgent(RuntimeAgent):
    """Local, review-first flow-artifact executor for the ChatGPT role.

    This class does not claim to call an external model.  Its local capability
    is deliberately concrete: turn the routed task plus supplied request
    context into a traceable Markdown flow artifact inside the ChatGPT module
    workspace.
    """

    module_name = "ChatGPT"
    action_label = "completed architecture flow"
    # W3 ecosystem role: flow architect / executor (module.json role)
    mpcp_role = "flow_architecture"
    mpcp_concepts = ["flow", "architecture", "execution", "executor"]

    _REPO_ROOT = Path(__file__).resolve().parents[3]
    _DEFAULT_FLOW_DIR = _REPO_ROOT / "modules" / "ChatGPT" / "flows"
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

    def execute(self, task: str, plan: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Create a real local flow draft and return its verifiable artifact record."""
        normalized_task = str(task).strip()
        if not normalized_task:
            return {
                "contract_version": "1.0",
                "status": "REJECTED",
                "module": self.module_name,
                "task": task,
                "summary": "A non-empty task is required before a flow artifact can be created.",
                "artifacts": [],
                "mutated": False,
                "review": True,
            }

        request = context.get("request") if isinstance(context.get("request"), dict) else {}
        payload = context.get("payload") if isinstance(context.get("payload"), dict) else {}
        if not payload and isinstance(request.get("payload"), dict):
            payload = request["payload"]

        trace_id = str(context.get("trace_id") or uuid.uuid4().hex)
        flow_dir = self._flow_dir()
        flow_dir.mkdir(parents=True, exist_ok=True)

        artifact_path = flow_dir / self._artifact_name(normalized_task, trace_id)
        artifact_text = self._render_flow_artifact(
            task=normalized_task,
            plan=plan,
            context=context,
            request=request,
            payload=payload,
            trace_id=trace_id,
        )
        self._atomic_write(artifact_path, artifact_text)

        digest = hashlib.sha256(artifact_text.encode("utf-8")).hexdigest()
        artifact_ref = {
            "path": self._display_path(artifact_path),
            "sha256": digest,
            "bytes": len(artifact_text.encode("utf-8")),
            "kind": "w3.flow_artifact.markdown",
        }

        return {
            "contract_version": "1.0",
            "status": "COMPLETED",
            "module": self.module_name,
            "task": normalized_task,
            "capability": "local_flow_artifact",
            "trace_id": trace_id,
            "summary": (
                "Created a local flow artifact from the routed task and request context. "
                "No remote model, network call, or external executor was used."
            ),
            "artifacts": [artifact_ref],
            "mutated": True,
            "mutation_scope": [self._display_path(flow_dir)],
            "external_execution_allowed": False,
            "review": True,
            "limitations": [
                "This is a deterministic local planner, not an OpenAI API invocation.",
                "The generated flow remains a draft and requires human review before downstream execution.",
            ],
        }

    def _flow_dir(self) -> Path:
        override = os.environ.get("W3_CHATGPT_FLOW_DIR")
        if override:
            return Path(override).expanduser().resolve()
        return self._DEFAULT_FLOW_DIR

    def _artifact_name(self, task: str, trace_id: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", task.lower()).strip("-") or "task"
        safe_trace = re.sub(r"[^a-zA-Z0-9]", "", trace_id)[:12] or "trace"
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        return f"{stamp}_{slug[:48]}_{safe_trace}.md"

    def _render_flow_artifact(
        self,
        *,
        task: str,
        plan: Dict[str, Any],
        context: Dict[str, Any],
        request: Dict[str, Any],
        payload: Dict[str, Any],
        trace_id: str,
    ) -> str:
        target = context.get("target") or request.get("target") or "W3"
        source = context.get("source") or request.get("source") or "unspecified"
        intent = request.get("intent") or payload.get("intent") or task
        responsibilities = plan.get("responsibilities") or []
        if not isinstance(responsibilities, list):
            responsibilities = [str(responsibilities)]
        safe_payload = self._redact(payload)
        payload_json = json.dumps(safe_payload, indent=2, ensure_ascii=False, sort_keys=True)
        request_file = request.get("_request_file")
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

        responsibility_lines = "\n".join(
            f"- {item}" for item in responsibilities if str(item).strip()
        ) or "- No responsibility was supplied by the routed identity profile."

        request_file_line = f"- Request file: `{request_file}`\n" if request_file else ""

        return f"""# W3 Local Flow Artifact\n\n## Trace\n- Trace ID: `{trace_id}`\n- Created at: `{timestamp}`\n- Module: `{self.module_name}`\n- Capability: `local_flow_artifact`\n- Review required: `true`\n\n## Request\n- Task: `{task}`\n- Intent: {intent}\n- Source: `{source}`\n- Target: `{target}`\n{request_file_line}\n## Routed Plan\n- Role: `{plan.get('role', '—')}`\n- Assigned module: `{plan.get('run_with', self.module_name)}`\n- Plan status: `{plan.get('status', 'ACTIVE')}`\n\n### Responsibilities\n{responsibility_lines}\n\n## Local Flow\n1. Receive the routed task and request context.\n2. Preserve the supplied intent, target, and payload as a reviewable draft.\n3. Produce this flow artifact in the ChatGPT module workspace.\n4. Send the artifact to the required human and governance review path before any downstream execution.\n\n## Request Payload (redacted)\n```json\n{payload_json}\n```\n\n## Boundary\n- This artifact is a local deterministic draft; it is not evidence of an external model call.\n- No network request, API request, shell command, merge, or deployment was executed.\n- Secret-like values are redacted by key name before the payload is written here.\n- Do not place patient data, private keys, tokens, passwords, or credentials in the request payload.\n\n## Review Decision\n- [ ] Accept as a working flow\n- [ ] Revise request context or responsibilities\n- [ ] Route to validation/governance\n- [ ] Reject\n"""

    def _redact(self, value: Any) -> Any:
        if isinstance(value, dict):
            cleaned = {}
            for key, child in value.items():
                key_text = str(key)
                if any(keyword in key_text.lower() for keyword in self._SECRET_KEYWORDS):
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
