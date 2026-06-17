# mpcp/kernel/event_template.py

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4


EndEvent = Union[int, str]


@dataclass(frozen=True)
class EventTemplate:
    """MPCP-side event template.

    Template shapes incoming event data so Condien can pull libs and prepare
    field without guessing. It does not execute work.
    """

    template_id: str
    event_type: str
    scope: str
    context_fields: List[str]
    required_payload: List[str]

    optional_payload: List[str] = field(default_factory=list)
    condien_libs: List[str] = field(default_factory=list)
    allowed_assist: List[str] = field(default_factory=list)
    paper_pack_hint: Optional[str] = None
    cross_field_hint: Optional[str] = None
    return_to: str = "MPCP"
    end_event: EndEvent = 1
    rot_type: str = "ROT:MPCP"

    def validate(self) -> bool:
        for attr in ("template_id", "event_type", "scope", "return_to", "rot_type"):
            value = getattr(self, attr)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"EVENT_TEMPLATE_FAIL: {attr.upper()}_REQUIRED")

        for attr in ("context_fields", "required_payload"):
            values = getattr(self, attr)
            if not isinstance(values, list) or not values:
                raise ValueError(f"EVENT_TEMPLATE_FAIL: {attr.upper()}_MUST_BE_NON_EMPTY_LIST")
            for idx, value in enumerate(values):
                if not isinstance(value, str) or not value.strip():
                    raise ValueError(f"EVENT_TEMPLATE_FAIL: {attr.upper()}[{idx}]_INVALID")

        for attr in ("optional_payload", "condien_libs", "allowed_assist"):
            values = getattr(self, attr)
            if not isinstance(values, list):
                raise ValueError(f"EVENT_TEMPLATE_FAIL: {attr.upper()}_MUST_BE_LIST")
            for idx, value in enumerate(values):
                if not isinstance(value, str) or not value.strip():
                    raise ValueError(f"EVENT_TEMPLATE_FAIL: {attr.upper()}[{idx}]_INVALID")

        return True

    def to_dict(self, *, omit_empty: bool = True) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "TEMPLATE_ID": self.template_id,
            "EVENT_TYPE": self.event_type,
            "SCOPE": self.scope,
            "CONTEXT_FIELDS": self.context_fields,
            "REQUIRED_PAYLOAD": self.required_payload,
            "OPTIONAL_PAYLOAD": self.optional_payload,
            "CONDIEN_LIBS": self.condien_libs,
            "ALLOWED_ASSIST": self.allowed_assist,
            "PAPER_PACK_HINT": self.paper_pack_hint,
            "CROSS_FIELD_HINT": self.cross_field_hint,
            "RETURN_TO": self.return_to,
            "END_EVENT": self.end_event,
            "ROT_TYPE": self.rot_type,
        }
        if omit_empty:
            return {key: value for key, value in data.items() if value not in (None, [], {})}
        return data


@dataclass(frozen=True)
class CondienLibRequest:
    """Request produced from EventTemplate for Condien."""

    event_id: str
    template_id: str
    event_type: str
    scope: str
    condien_libs: List[str]
    allowed_assist: List[str]
    return_to: str
    cross_field_hint: Optional[str] = None
    paper_pack_hint: Optional[str] = None
    env_ref: Optional[str] = None
    trace_id: str = field(default_factory=lambda: uuid4().hex)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self, *, omit_none: bool = True) -> Dict[str, Any]:
        data = {
            "EVENT_ID": self.event_id,
            "TEMPLATE_ID": self.template_id,
            "EVENT_TYPE": self.event_type,
            "SCOPE": self.scope,
            "CONDIEN_LIBS": self.condien_libs,
            "ALLOWED_ASSIST": self.allowed_assist,
            "RETURN_TO": self.return_to,
            "CROSS_FIELD_HINT": self.cross_field_hint,
            "PAPER_PACK_HINT": self.paper_pack_hint,
            "ENV_REF": self.env_ref,
            "TRACE_ID": self.trace_id,
            "TIMESTAMP": self.timestamp,
        }
        if omit_none:
            return {key: value for key, value in data.items() if value is not None}
        return data


class EventTemplateBridge:
    """Convert a shaped event template into a Condien lib request."""

    @staticmethod
    def validate_payload(template: EventTemplate, payload: Dict[str, Any]) -> bool:
        template.validate()
        if not isinstance(payload, dict):
            raise ValueError("EVENT_TEMPLATE_FAIL: PAYLOAD_MUST_BE_DICT")

        missing = [key for key in template.required_payload if key not in payload]
        if missing:
            raise ValueError(f"EVENT_TEMPLATE_FAIL: PAYLOAD_MISSING_REQUIRED:{','.join(missing)}")

        return True

    @staticmethod
    def build_condien_request(
        *,
        event_id: str,
        template: EventTemplate,
        payload: Dict[str, Any],
        env_ref: Optional[str] = None,
    ) -> CondienLibRequest:
        EventTemplateBridge.validate_payload(template, payload)
        if not isinstance(event_id, str) or not event_id.strip():
            raise ValueError("EVENT_TEMPLATE_FAIL: EVENT_ID_REQUIRED")

        return CondienLibRequest(
            event_id=event_id,
            template_id=template.template_id,
            event_type=template.event_type,
            scope=template.scope,
            condien_libs=template.condien_libs,
            allowed_assist=template.allowed_assist,
            return_to=template.return_to,
            cross_field_hint=template.cross_field_hint,
            paper_pack_hint=template.paper_pack_hint,
            env_ref=env_ref,
        )


def build_mpcp_lib_blueprint_template() -> EventTemplate:
    """Template matching the EVENT-A01 blueprint sketch."""
    return EventTemplate(
        template_id="EVT:MPCP/LIB.BLUEPRINT",
        event_type="MPCP_LIB_BLUEPRINT",
        scope="MPCP_LIB_BLUEPRINT_BUILD",
        context_fields=["MPCP", "LIB", "BLUEPRINT"],
        required_payload=["code_set", "intent", "scope"],
        optional_payload=["risk", "context", "expected_gain"],
        condien_libs=["lib_blueprint", "file_boundary", "table_relation", "modew_dynamic"],
        allowed_assist=["Table-X", "file.void", "Modew-dynamic"],
        paper_pack_hint="Papers-Pack-A01",
        cross_field_hint="Cross-X",
        return_to="MPCP",
        end_event=1,
        rot_type="ROT:MPCP",
    )
