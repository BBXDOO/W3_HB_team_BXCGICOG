from __future__ import annotations

import json
from typing import Any, Dict, Mapping

from .base import RuntimeAgent
from ..w3lgu_mfc_logic.redr_mfc_logic import classify_event


class REDRAgent(RuntimeAgent):
    module_name = "REDR"
    action_label = "read, tagged, and packaged event"
    mpcp_role = "reader_package_builder"
    mpcp_concepts = [
        "read",
        "reader",
        "tag",
        "package",
        "payload",
        "structure",
        "signal",
        "route",
        "memory",
        "trace",
        "non_mutation",
        "review",
    ]

    def _safe_mapping(self, value: Any) -> Dict[str, Any]:
        if isinstance(value, Mapping):
            return dict(value)
        return {}

    def _text_part(self, value: Any) -> str:
        if value is None:
            return ""

        if isinstance(value, str):
            return value.strip()

        try:
            return json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                default=str,
            )
        except TypeError:
            return str(value)

    def build_event(
        self,
        task: str,
        plan: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        request = self._safe_mapping(context.get("request"))

        if "payload" in request:
            payload = request.get("payload")
        else:
            payload = context.get("payload", plan.get("payload"))

        text_parts = [
            self._text_part(task),
            self._text_part(request.get("intent")),
            self._text_part(payload),
        ]

        text = " ".join(part for part in text_parts if part).strip()

        event = {
            "text": text or task,
            "task": task,
            "source": request.get("source")
            or context.get("source")
            or "runtime_agent",
            "target": request.get("target")
            or context.get("target")
            or plan.get("target")
            or "W3",
            "role": plan.get("role", "reader"),
            "agent": self.module_name,
        }

        if payload is not None:
            event["payload"] = payload

        responsibilities = self._responsibilities(plan)
        if responsibilities:
            event["responsibilities"] = responsibilities

        return event

    def inspect_event(
        self,
        task: str,
        plan: Dict[str, Any] | None = None,
        context: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        plan = plan or {}
        context = context or {}

        event = self.build_event(task, plan, context)
        result = classify_event(event)

        return result.as_dict()

    def run(
        self,
        task: str,
        plan: Dict[str, Any],
        context: Dict[str, Any],
    ) -> str:
        result = self.inspect_event(task, plan, context)

        details = result.get("details", {})
        package = details.get("package", {})

        package_id = package.get("package_id", "REDR-PKG-UNKNOWN")
        tags = package.get("tag_summary", [])
        next_modules = result.get("next", [])
        input_type = result.get("input_type", "package:unknown")
        status = result.get("status", "UNKNOWN")

        return (
            f"{self.module_name} ({plan.get('role', 'reader')}) "
            f"{self.action_label}: {task} | "
            f"status: {status} | "
            f"type: {input_type} | "
            f"package: {package_id} | "
            f"tags: {tags} | "
            f"next: {next_modules} | "
            f"mutated: False"
        )


__all__ = ["REDRAgent"]
