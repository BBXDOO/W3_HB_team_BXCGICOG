"""W3Lgu 6ROOM runtime selector.

Reads an event shape, selects a Logic27 slot, opens only the required 6ROOM
fields, and returns a contract for MPCP / Cross-X / E-CS / Modew.

Scope:
- 6ROOM selects rooms and support needs.
- 6ROOM does not own MPCP ENV control.
- 6ROOM does not own E-CS return binding.
- 6ROOM does not own Cross-X cooperation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Mapping

SYS_STANDBY = 0x00
SYS_ACTIVE = 0x01
SYS_REVIEW = 0x02

STATE_MAP = {
    SYS_STANDBY: "STANDBY",
    SYS_ACTIVE: "ACTIVE",
    SYS_REVIEW: "REVIEW",
}

CONFIDENCE_LOW = 0.0
CONFIDENCE_MID = 0.5
CONFIDENCE_HIGH = 1.0

ROOMS = ("Ev", "Si", "Ap", "Ca", "Cu", "Re")


LogicLens = Callable[["EventForm"], None]


def ordered_unique(values: Iterable[str]) -> list[str]:
    out: list[str] = []
    for value in values:
        if value not in out:
            out.append(value)
    return out


@dataclass(frozen=True)
class LogicSlot:
    """Logic27 slot mapped into 6ROOM allocation."""

    slot_id: str
    purpose: str
    active_rooms: tuple[str, ...]
    support_required: tuple[str, ...] = ()
    next_handler: str = "none"
    next_event: str = "STOP"
    result_state: str = "READY"
    cross_request: str = "STANDBY"
    active_system_hints: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "slot_id": self.slot_id,
            "purpose": self.purpose,
            "active_rooms": list(self.active_rooms),
            "support_required": list(self.support_required),
            "next_handler": self.next_handler,
            "next_event": self.next_event,
            "result_state": self.result_state,
            "cross_request": self.cross_request,
            "active_system_hints": list(self.active_system_hints),
        }


DEFAULT_LOGIC27_SLOTS: dict[str, LogicSlot] = {
    "L1-C1": LogicSlot(
        slot_id="L1-C1",
        purpose="local_simple_observation",
        active_rooms=("Ev", "Si", "Re"),
        support_required=("CONFIG",),
        next_handler="local_handler",
        next_event="Event-2_local_result",
    ),
    "L1-C2": LogicSlot(
        slot_id="L1-C2",
        purpose="local_document_check",
        active_rooms=("Ev", "Si", "Re"),
        support_required=("TEMPLATE", "DOCUMENT_CHECKER"),
        next_handler="document_checker",
        next_event="Event-2_document_report",
    ),
    "L2-C1": LogicSlot(
        slot_id="L2-C1",
        purpose="normal_route_handoff",
        active_rooms=("Ev", "Si", "Cu", "Re"),
        support_required=("MPCP_ENV", "CONFIG"),
        next_handler="mpcp",
        next_event="Event-2_health_review",
        result_state="SUCCESS",
        cross_request="ACTIVE",
        active_system_hints=("Git",),
    ),
    "L2-C3": LogicSlot(
        slot_id="L2-C3",
        purpose="risk_and_ambiguity_review",
        active_rooms=("Ev", "Si", "Ap", "Ca", "Cu", "Re"),
        support_required=("DTML", "ROT", "Cross-X", "LRC2"),
        next_handler="review",
        next_event="Event-2_recovery_trace",
        result_state="REVIEW",
        cross_request="REVIEW",
        active_system_hints=("DTML", "Hospitication"),
    ),
    "L3-C1": LogicSlot(
        slot_id="L3-C1",
        purpose="external_language_normalization",
        active_rooms=("Ev", "Si", "Ap", "Cu", "Re"),
        support_required=("Cross-L", "REDR"),
        next_handler="cross_l",
        next_event="Event-2_cross_l_normalize",
    ),
    "L5-C1": LogicSlot(
        slot_id="L5-C1",
        purpose="template_ready_render",
        active_rooms=("Ev", "Si", "Re"),
        support_required=("TEMPLATE", "CONFIG"),
        next_handler="template_renderer",
        next_event="Event-2_render_output",
    ),
    "L6-C1": LogicSlot(
        slot_id="L6-C1",
        purpose="repo_sync_check",
        active_rooms=("Ev", "Si", "Cu", "Re"),
        support_required=("GIT", "MPCP_ENV"),
        next_handler="git",
        next_event="Event-2_repo_health",
        result_state="SUCCESS",
        cross_request="ACTIVE",
        active_system_hints=("Git",),
    ),
    "L6-C3": LogicSlot(
        slot_id="L6-C3",
        purpose="repo_conflict_recovery",
        active_rooms=("Ev", "Si", "Ap", "Ca", "Cu", "Re"),
        support_required=("GIT", "DTML", "ROT", "Cross-X"),
        next_handler="recovery_review",
        next_event="Event-2_repo_conflict_recovery",
        result_state="REVIEW",
        cross_request="REVIEW",
        active_system_hints=("Git", "DTML", "Hospitication"),
    ),
    "L7-C1": LogicSlot(
        slot_id="L7-C1",
        purpose="env_support_prepare",
        active_rooms=("Ev", "Si", "Cu", "Re"),
        support_required=("MPCP_ENV", "CONFIG"),
        next_handler="mpcp",
        next_event="Event-2_env_support",
    ),
    "L9-C3": LogicSlot(
        slot_id="L9-C3",
        purpose="unknown_safe_fallback",
        active_rooms=("Ev", "Si", "Ap"),
        support_required=("REDR", "LRC2"),
        next_handler="observe",
        next_event="STOP",
        result_state="STOP",
    ),
}


class EventForm:
    """Fixed-slot 6ROOM event form."""

    __slots__ = [
        "event_id", "source", "type_data", "intent",
        "logic_chain", "logic_slot", "logic_purpose",
        "ev", "si", "ap", "ca", "cu", "re",
        "active_systems", "standby_systems",
        "cross_state", "cross_request",
        "confidence", "confidence_level",
        "result", "result_state", "next_event", "next_handler",
        "support_required",
        "event_container_mutated", "source_truth_mutated", "env_mutated",
        "rooms_registry",
    ]

    def __init__(
        self,
        event_id: str,
        source: str,
        type_data: str,
        intent: str,
        environment_si: Mapping[str, Any] | None = None,
    ) -> None:
        self.event_id = str(event_id).strip()
        if not self.event_id:
            raise ValueError("event_id must be non-empty")
        self.source = str(source)
        self.type_data = str(type_data)
        self.intent = str(intent)
        self.logic_chain = "UNDEFINED"
        self.logic_slot = None
        self.logic_purpose = None

        self.ev = None
        self.si = dict(environment_si or {})
        self.ap = None
        self.ca = None
        self.cu = None
        self.re = "STANDBY"

        self.active_systems = []
        self.standby_systems = []
        self.cross_state = SYS_STANDBY
        self.cross_request = "STANDBY"
        self.confidence = CONFIDENCE_LOW
        self.confidence_level = "LOW"
        self.result = "INITIAL"
        self.result_state = "STOP"
        self.next_event = "STOP"
        self.next_handler = "none"
        self.support_required = []

        self.event_container_mutated = False
        self.source_truth_mutated = False
        self.env_mutated = False

        self.rooms_registry = {
            "Ev": SYS_ACTIVE,
            "Si": SYS_ACTIVE,
            "Ap": SYS_STANDBY,
            "Ca": SYS_STANDBY,
            "Cu": SYS_STANDBY,
            "Re": SYS_STANDBY,
        }

    def sync_room_gates(self, active_rooms: Iterable[str]) -> None:
        active = set(active_rooms)
        for room in ROOMS:
            self.rooms_registry[room] = SYS_ACTIVE if room in active else SYS_STANDBY
        self.event_container_mutated = True

    def matrix_snapshot(self) -> dict[str, Any]:
        return {
            "EV": self.ev,
            "SI": dict(self.si),
            "AP": self.ap,
            "CA": self.ca,
            "CU": self.cu,
            "RE": self.re,
        }

    def rooms_allocation(self) -> dict[str, str]:
        return {room: STATE_MAP[state] for room, state in self.rooms_registry.items()}

    def export_return_contract(self) -> dict[str, Any]:
        return {
            "RETURN": {
                "schema": "w3lgu.6room.return.v1",
                "event_id": self.event_id,
                "source": self.source,
                "type_data": self.type_data,
                "intent": self.intent,
                "logic_chain": self.logic_chain,
                "logic_slot": self.logic_slot,
                "logic_purpose": self.logic_purpose,
                "result_state": self.result_state,
                "cross_state": STATE_MAP[self.cross_state],
                "cross_request": self.cross_request,
                "confidence": {
                    "level": self.confidence_level,
                    "score": self.confidence,
                },
                "result": self.result,
                "next": {
                    "event": self.next_event,
                    "handler": self.next_handler,
                },
                "routing": {
                    "active_systems": list(self.active_systems),
                    "standby_systems": list(self.standby_systems),
                },
                "support_required": list(self.support_required),
                "mutation": {
                    "event_container": self.event_container_mutated,
                    "source_truth": self.source_truth_mutated,
                    "env": self.env_mutated,
                },
                "matrix_snapshot": self.matrix_snapshot(),
                "rooms_allocation": self.rooms_allocation(),
            }
        }


class SixRoomRuntime:
    """6ROOM runtime selector and room allocation engine."""

    def __init__(self, *, logic_slots: Mapping[str, LogicSlot] | None = None) -> None:
        self._logic_pool: dict[str, LogicLens] = {}
        self._logic_slots = dict(logic_slots or DEFAULT_LOGIC27_SLOTS)
        self.runtime_systems = [
            "W3Lgu", "REDR", "PSP2", "DTML", "PX", "LRC2",
            "Cross-L", "File.void", "Git", "Hospitication", "IGET",
        ]

    def deploy_logic_lens(self, chain_name: str, lens: LogicLens) -> None:
        if not callable(lens):
            raise TypeError("logic lens must be callable")
        self._logic_pool[str(chain_name)] = lens

    def register_logic_slot(self, slot: LogicSlot) -> None:
        self._logic_slots[slot.slot_id] = slot

    def execute_chain(self, event: EventForm, raw_input_signal: Any) -> dict[str, Any]:
        event.ev = raw_input_signal
        event.event_container_mutated = True
        self._evaluate_confidence(event)
        slot = self._select_logic_slot(event)
        self._apply_slot(event, slot)
        self._allocate_systems(event, slot)

        lens = self._logic_pool.get(event.logic_chain)
        if lens and event.confidence_level == "HIGH":
            lens(event)
            event.event_container_mutated = True
        elif event.confidence_level in {"LOW", "MID"}:
            self._ambiguity_fallback(event)

        return event.export_return_contract()

    def _evaluate_confidence(self, event: EventForm) -> None:
        raw = str(event.ev or "").upper()
        if not raw:
            event.confidence = CONFIDENCE_LOW
            event.confidence_level = "LOW"
        elif "CONFLICT" in raw or "UNCLEAR" in raw or "AMBIGUOUS" in raw:
            event.confidence = CONFIDENCE_MID
            event.confidence_level = "MID"
        else:
            event.confidence = CONFIDENCE_HIGH
            event.confidence_level = "HIGH"

    def _select_logic_slot(self, event: EventForm) -> LogicSlot:
        raw = str(event.ev or "").upper()
        type_data = event.type_data.upper()
        intent = event.intent.upper()
        operation_type = str(event.si.get("operation_type", "")).lower()

        if event.confidence_level == "LOW":
            return self._logic_slots["L9-C3"]
        if event.confidence_level == "MID":
            if operation_type == "source_control" or "GIT" in raw:
                return self._logic_slots["L6-C3"]
            return self._logic_slots["L2-C3"]
        if operation_type == "source_control" or "GIT" in raw or "SYNC" in intent:
            return self._logic_slots["L6-C1"]
        if "DOC" in type_data or "DOCUMENT" in intent:
            if event.si.get("template_available") or event.si.get("config_ok"):
                return self._logic_slots["L5-C1"]
            return self._logic_slots["L1-C2"]
        if "EXTERNAL" in type_data or "CROSS_LANGUAGE" in type_data:
            return self._logic_slots["L3-C1"]
        if event.si.get("env_required") or event.si.get("mpcp_required"):
            return self._logic_slots["L7-C1"]
        return self._logic_slots["L1-C1"]

    def _apply_slot(self, event: EventForm, slot: LogicSlot) -> None:
        event.logic_slot = slot.slot_id
        event.logic_purpose = slot.purpose
        event.logic_chain = slot.purpose
        event.cross_request = slot.cross_request
        event.result_state = slot.result_state
        event.next_event = slot.next_event
        event.next_handler = slot.next_handler
        event.support_required = list(slot.support_required)
        event.result = slot.result_state
        event.re = slot.result_state
        event.cu = f"LOGIC27:{slot.slot_id}:{slot.purpose}"
        event.sync_room_gates(slot.active_rooms)

    def _allocate_systems(self, event: EventForm, slot: LogicSlot) -> None:
        active = ordered_unique(("W3Lgu",) + slot.active_system_hints)
        support_map = {
            "REDR": "REDR",
            "DTML": "DTML",
            "Cross-L": "Cross-L",
            "PX": "PX",
            "LRC2": "LRC2",
            "GIT": "Git",
            "Hospitication": "Hospitication",
            "IGET": "IGET",
        }
        for support, node in support_map.items():
            if support in slot.support_required:
                active.append(node)
        event.active_systems = ordered_unique(active)
        event.standby_systems = [node for node in self.runtime_systems if node not in event.active_systems]
        if slot.cross_request == "REVIEW":
            event.cross_state = SYS_REVIEW
        elif slot.cross_request == "ACTIVE":
            event.cross_state = SYS_ACTIVE
        else:
            event.cross_state = SYS_STANDBY

    def _ambiguity_fallback(self, event: EventForm) -> None:
        event.sync_room_gates(("Ev", "Si", "Ap", "Ca", "Cu", "Re"))
        event.ap = "AMBIGUOUS_SIGNAL_ALERT"
        event.ca = "INPUT_METADATA_OBSCURED"
        event.cu = "DEFERRED_TO_LRC2_LEARNING_LAB"
        event.re = "WAIT" if event.confidence_level == "MID" else "STOP"
        event.result = "UNCLEAR_RECOVERY_TRIGGERED"
        event.result_state = event.re
        event.next_event = "WAIT_OR_REVIEW" if event.confidence_level == "MID" else "STOP"
        event.next_handler = "review" if event.confidence_level == "MID" else "none"
        event.cross_state = SYS_REVIEW if event.confidence_level == "MID" else SYS_STANDBY
        event.cross_request = STATE_MAP[event.cross_state]


def logic27_to_6room_bridge_lens(event: EventForm) -> None:
    """Simple Logic27 bridge lens for direct attachment to SixRoomRuntime."""

    raw = str(event.ev or "").upper()
    slot = DEFAULT_LOGIC27_SLOTS["L2-C3"] if "CONFLICT" in raw or "AMBIGUOUS" in raw else DEFAULT_LOGIC27_SLOTS["L2-C1"]
    event.logic_slot = slot.slot_id
    event.logic_purpose = slot.purpose
    event.logic_chain = slot.purpose
    event.support_required = list(slot.support_required)
    event.next_handler = slot.next_handler
    event.next_event = slot.next_event
    event.result_state = slot.result_state
    event.result = slot.result_state
    event.re = slot.result_state
    event.ap = f"LOGIC27_SLOT_{slot.slot_id}_ENGAGED"
    event.ca = f"INTENT_IDENTIFIED_AS_{event.intent.upper()}"
    event.cu = f"PROCESSED_VIA_PURPOSE_{slot.purpose.upper()}"
    event.cross_request = slot.cross_request
    event.cross_state = SYS_REVIEW if slot.cross_request == "REVIEW" else SYS_ACTIVE if slot.cross_request == "ACTIVE" else SYS_STANDBY
    event.sync_room_gates(slot.active_rooms)


__all__ = [
    "SYS_STANDBY", "SYS_ACTIVE", "SYS_REVIEW",
    "CONFIDENCE_LOW", "CONFIDENCE_MID", "CONFIDENCE_HIGH",
    "LogicSlot", "DEFAULT_LOGIC27_SLOTS", "EventForm", "SixRoomRuntime",
    "logic27_to_6room_bridge_lens",
]
