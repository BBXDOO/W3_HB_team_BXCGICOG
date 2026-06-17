# mpcp/kernel/module_bridge.py

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import uuid4

from protocol.mpcp.kernel.module_validator import ModuleValidator


@dataclass(frozen=True)
class ModuleBridgeTrace:
    """Trace packet for cooperative module return.

    This is not an executor and does not send over network.
    It only builds a return/assist trace packet for later routing.
    """

    source_module: str
    target_module: str
    event_id: str
    cross_field: str
    payload: Dict[str, Any]
    bridge_state: str = "TRACE_BUILT"
    trace_id: str = field(default_factory=lambda: uuid4().hex)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "BRIDGE_STATE": self.bridge_state,
            "SOURCE_MODULE": self.source_module,
            "TARGET_MODULE": self.target_module,
            "EVENT_ID": self.event_id,
            "CROSS_FIELD": self.cross_field,
            "PAYLOAD": self.payload,
            "TRACE_ID": self.trace_id,
            "TIMESTAMP": self.timestamp,
            "SOURCE_TRUTH_MUTATED": False,
            "ENV_MUTATED": False,
        }


class ModuleBridge:
    """Build cooperative bridge traces.

    Bridge means: prepare a traceable return packet.
    It must not execute work or mutate source truth.
    """

    @staticmethod
    def _get(contract: Any, upper_key: str, lower_key: str, default: Any = None) -> Any:
        if isinstance(contract, dict):
            if upper_key in contract:
                return contract[upper_key]
            return contract.get(lower_key, default)
        return getattr(contract, lower_key, default)

    @staticmethod
    def build_return_trace(contract: Any, payload: Dict[str, Any], *, target_module: Optional[str] = None) -> ModuleBridgeTrace:
        data = contract.to_dict() if hasattr(contract, "to_dict") else contract
        ModuleValidator.validate_contract(data)

        if not isinstance(payload, dict):
            raise ValueError("MODULE_BRIDGE_FAIL: PAYLOAD_MUST_BE_DICT")

        source = ModuleBridge._get(data, "RESPONSIBLE_MODULE", "responsible_module")
        target = target_module or ModuleBridge._get(data, "RETURN_TO", "return_to")
        event_id = ModuleBridge._get(data, "EVENT_ID", "event_id")
        cross_field = ModuleBridge._get(data, "CROSS_FIELD", "cross_field")

        return ModuleBridgeTrace(
            source_module=source,
            target_module=target,
            event_id=event_id,
            cross_field=cross_field,
            payload=payload,
        )

    @staticmethod
    def build_assist_trace(contract: Any, assist_module: str, payload: Dict[str, Any]) -> ModuleBridgeTrace:
        data = contract.to_dict() if hasattr(contract, "to_dict") else contract
        ModuleValidator.validate_contract(data)

        assists = ModuleBridge._get(data, "ASSIST_MODULES", "assist_modules", [])
        if assist_module not in assists:
            raise ValueError("MODULE_BRIDGE_FAIL: ASSIST_MODULE_NOT_IN_CONTRACT")

        if not isinstance(payload, dict):
            raise ValueError("MODULE_BRIDGE_FAIL: PAYLOAD_MUST_BE_DICT")

        source = ModuleBridge._get(data, "RESPONSIBLE_MODULE", "responsible_module")
        event_id = ModuleBridge._get(data, "EVENT_ID", "event_id")
        cross_field = ModuleBridge._get(data, "CROSS_FIELD", "cross_field")

        return ModuleBridgeTrace(
            source_module=source,
            target_module=assist_module,
            event_id=event_id,
            cross_field=cross_field,
            payload=payload,
            bridge_state="ASSIST_TRACE_BUILT",
        )
