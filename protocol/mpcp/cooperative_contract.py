"""MPCP cooperative contract.

This module mirrors the W3 cooperative-module picture:
A = responsible module, B = assist modules, C = cross / assist field.

It does not execute work. It only shapes an event-level cooperation record so
MPCP can return trace after using Cross-X, Modew, Table-X, file.void, or other
assist fields when needed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4


EndEvent = Union[int, str]
TraceData = Union[Dict[str, Any], List[Dict[str, Any]]]
TriggerData = Union[str, List[str]]


@dataclass
class CooperativeContract:
    responsible_module: str
    assist_modules: List[str]
    cross_field: str
    reason: str
    return_to: str
    event_id: str
    end_event: EndEvent
    trigger: TriggerData
    expected_gain: List[str]
    papers: List[str] = field(default_factory=list)
    trace: TraceData = field(default_factory=dict)

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
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def validate(self) -> bool:
        """Validate the relation shape without executing anything."""
        if not self.responsible_module.strip():
            raise ValueError("COOP_FAIL: RESPONSIBLE_MODULE_REQUIRED")

        if not self.assist_modules:
            raise ValueError("COOP_FAIL: ASSIST_MODULES_REQUIRED")

        if self.responsible_module in self.assist_modules:
            raise ValueError("COOP_FAIL: RESPONSIBLE_MODULE_CANNOT_ASSIST_SELF")

        if self.return_to != self.responsible_module:
            raise ValueError("COOP_FAIL: RETURN_TO_MUST_MATCH_RESPONSIBLE_MODULE")

        if not self.cross_field.strip():
            raise ValueError("COOP_FAIL: CROSS_FIELD_REQUIRED")

        if not self.reason.strip():
            raise ValueError("COOP_FAIL: REASON_REQUIRED")

        if isinstance(self.trigger, str):
            if not self.trigger.strip():
                raise ValueError("COOP_FAIL: TRIGGER_REQUIRED")
        elif isinstance(self.trigger, list):
            if not self.trigger or not all(isinstance(item, str) and item.strip() for item in self.trigger):
                raise ValueError("COOP_FAIL: TRIGGER_LIST_INVALID")
        else:
            raise ValueError("COOP_FAIL: TRIGGER_MUST_BE_STRING_OR_LIST")

        if not self.expected_gain:
            raise ValueError("COOP_FAIL: EXPECTED_GAIN_REQUIRED")

        if self.max_assist_routes < len(self.assist_modules):
            raise ValueError("COOP_FAIL: MAX_ASSIST_ROUTES_TOO_LOW")

        return True

    def to_dict(self, *, omit_none: bool = True) -> Dict[str, Any]:
        data = {
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
        if omit_none:
            return {key: value for key, value in data.items() if value is not None}
        return data


def build_mpcp_lib_blueprint_contract() -> CooperativeContract:
    """Build the registered EVENT-A01 cooperative contract."""
    return CooperativeContract(
        responsible_module="MPCP",
        assist_modules=["Table-X", "file.void", "Modew-dynamic"],
        cross_field="Cross-X",
        reason=(
            "Large blueprint work may need visual relation, file boundary, "
            "and dynamic Modew assist before returning to MPCP."
        ),
        return_to="MPCP",
        event_id="EVENT-A01",
        end_event=1,
        trigger=["needs_more_variables", "risk_distribution_needed", "parallel_check_needed"],
        expected_gain=["primary_result", "comparison_result", "risk_signal", "trace_explanation"],
        rot_type="ROT:MPCP",
        paper_pack_id="Papers-Pack-A01",
        field_selected="Cross-X",
        can_change_direction=True,
        can_expand=True,
        distribution_mode="assist_when_needed",
        rejoin_strategy="merge",
        lrc_ref="LRC2",
        papers=[
            "Paper-A01.1: Table-X'PX ; _MPCP/ACE",
            "Paper-A01.2: file.void ; _MPCP/ACE",
            "Paper-A01.3: Modew-dynamic E-A01.3",
            "Paper-A01.4: Modew-dynamic E-A01.4",
        ],
        trace=[
            {"STEP": "EVENT", "VALUE": "EVENT-A01"},
            {"STEP": "REDR_ROT", "VALUE": "Papers-Pack / Cross-X"},
            {"STEP": "CROSS_X", "VALUE": "END"},
            {"STEP": "COMBINE", "VALUE": "MPCP/Lib'Blueprint"},
            {"STEP": "LOG", "VALUE": "LRC2"},
            {"STEP": "END_EVENT", "VALUE": 1},
        ],
    )
