from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from uuid import uuid4
from datetime import datetime

@dataclass
class ECSCooperativeContract:
    event_id: str
    responsible_module: str
    assist_modules: List[str]
    cross_field: str
    reason: str
    expected_gain: List[str]
    return_to: str
    trigger: str
    trace: Dict[str, Any] = field(default_factory=dict)
    papers: List[str] = field(default_factory=list)
    risk_flags: List[str] = field(default_factory=list)
    distribution_mode: Optional[str] = "parallel"
    version: str = "ECS-Cooperative-v1"
    trace_id: str = field(default_factory=lambda: uuid4().hex)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "EVENT_ID": self.event_id,
            "RESPONSIBLE_MODULE": self.responsible_module,
            "ASSIST_MODULES": self.assist_modules,
            "CROSS_FIELD": self.cross_field,
            "REASON": self.reason,
            "EXPECTED_GAIN": self.expected_gain,
            "RETURN_TO": self.return_to,
            "TRIGGER": self.trigger,
            "TRACE": self.trace,
            "PAPERS": self.papers,
            "RISK_FLAGS": self.risk_flags,
            "DISTRIBUTION_MODE": self.distribution_mode,
            "VERSION": self.version,
            "TRACE_ID": self.trace_id,
            "TIMESTAMP": self.timestamp
        }
