from dataclasses import dataclass, field
from typing import Dict, Any, List
from uuid import uuid4
from datetime import datetime

@dataclass
class ECSEventTemplate:
    template_id: str
    event_type: str
    scope: str
    required_fields: List[str]
    allowed_assist: List[str]
    paper_pack_hint: str
    cross_field_hint: str
    return_to: str
    trace_id: str = field(default_factory=lambda: uuid4().hex)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def validate_payload(self, payload: Dict[str, Any]) -> bool:
        missing = [f for f in self.required_fields if f not in payload]
        if missing:
            raise ValueError(f"EVENT_TEMPLATE_FAIL: PAYLOAD_MISSING_REQUIRED:{','.join(missing)}")
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "TEMPLATE_ID": self.template_id,
            "EVENT_TYPE": self.event_type,
            "SCOPE": self.scope,
            "REQUIRED_FIELDS": self.required_fields,
            "ALLOWED_ASSIST": self.allowed_assist,
            "PAPER_PACK_HINT": self.paper_pack_hint,
            "CROSS_FIELD_HINT": self.cross_field_hint,
            "RETURN_TO": self.return_to,
            "TRACE_ID": self.trace_id,
            "TIMESTAMP": self.timestamp
        }
