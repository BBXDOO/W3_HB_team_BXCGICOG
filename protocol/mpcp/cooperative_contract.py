from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from uuid import uuid4
from datetime import datetime

@dataclass
class CooperativeContract:
    responsible_module: str
    assist_modules: List[str]
    cross_field: str
    reason: str
    return_to: str
    event_id: str
    end_event: str
    trigger: str
    expected_gain: List[str]
    papers: List[str] = field(default_factory=list)
    trace: Dict[str, Any] = field(default_factory=dict)

    # optional markers
    rot_type: Optional[str] = None
    paper_pack_id: Optional[str] = None
    field_selected: Optional[str] = None
    temp_agreement: bool = False
    can_change_direction: bool = True
    can_expand: bool = True
    risk_flags: List[str] = field(default_factory=list)
    distribution_mode: Optional[str] = None
    max_assist_routes: int = 3
    rejoin_strategy: Optional[str] = "merge"
    quality_check: bool = True
    env_ref: Optional[str] = None
    stack_ref: Optional[str] = None
    lrc_ref: Optional[str] = None

    trace_id: str = field(default_factory=lambda: uuid4().hex)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "RESPONSIBLE_MODULE": self.responsible_module,
            "ASSIST_MODULES": self.assist_modules,
            "CROSS_FIELD": self.cross_field,
            "REASON": self.reason,
            "RETURN_TO": self.return_to,
            "EVENT_ID": self.event_id,
            "END_EVENT": self.end_event,
            "TRIGGER": self.trigger,
            "EXPECTED_GAIN": self.expected_gain,
            "PAPERS": self.papers,
            "TRACE": self.trace,
            "ROT_TYPE": self.rot_type,
            "PAPER_PACK_ID": self.paper_pack_id,
            "FIELD_SELECTED": self.field_selected,
            "TEMP_AGREEMENT": self.temp_agreement,
            "CAN_CHANGE_DIRECTION": self.can_change_direction,
            "CAN_EXPAND": self.can_expand,
            "RISK_FLAGS": self.risk_flags,
            "DISTRIBUTION_MODE": self.distribution_mode,
            "MAX_ASSIST_ROUTES": self.max_assist_routes,
            "REJOIN_STRATEGY": self.rejoin_strategy,
            "QUALITY_CHECK": self.quality_check,
            "ENV_REF": self.env_ref,
            "STACK_REF": self.stack_ref,
            "LRC_REF": self.lrc_ref,
            "TRACE_ID": self.trace_id,
            "TIMESTAMP": self.timestamp,
        }
