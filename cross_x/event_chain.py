"""Immutable Event-Chain System (E-CS) contracts for Cross-Series.

E-CS makes the configured Cross-X chain observable as ordered handoffs.  It
does not run subsystems: every event is a plan record carrying the subsystem
contract, predecessor, and governance boundary.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Any, Mapping, Sequence

ECS_CONTRACT_VERSION = "1.0"
_ECS_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_TERMINAL_EVENT_STATES = frozenset({"completed", "stopped", "inactive"})


def freeze_ecs_mapping(value: Mapping[str, Any]) -> Mapping[str, Any]:
    """Return a recursively immutable copy suitable for E-CS history."""

    if not isinstance(value, Mapping):
        raise TypeError("E-CS value must be a mapping")
    return MappingProxyType(
        {str(key): _freeze_ecs_value(item) for key, item in value.items()}
    )


def thaw_ecs_mapping(value: Mapping[str, Any]) -> dict[str, Any]:
    """Return a JSON-friendly copy of an immutable E-CS mapping."""

    return {str(key): _thaw_ecs_value(item) for key, item in value.items()}


def _freeze_ecs_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return freeze_ecs_mapping(value)
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_ecs_value(item) for item in value)
    if isinstance(value, set):
        return tuple(sorted((_freeze_ecs_value(item) for item in value), key=repr))
    return value


def _thaw_ecs_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return thaw_ecs_mapping(value)
    if isinstance(value, tuple):
        return [_thaw_ecs_value(item) for item in value]
    return value


def normalize_ecs_identifier(value: object, *, field: str) -> str:
    """Return a delimiter-safe E-CS identifier or reject it.

    E-CS identifiers are embedded in W3Lgu values, so commas, colons, line
    breaks, and other packet delimiters are intentionally forbidden.
    """

    if not isinstance(value, str):
        raise ValueError(f"E-CS {field} must be a string")
    normalized = value.strip()
    if not _ECS_IDENTIFIER.fullmatch(normalized):
        raise ValueError(
            f"E-CS {field} must use 1-128 letters, digits, '.', '_' or '-'"
        )
    return normalized


def _stable_event_id(chain_id: str, sequence: int, system: str) -> str:
    body = json.dumps(
        {"chain_id": chain_id, "sequence": sequence, "system": system},
        sort_keys=True,
        separators=(",", ":"),
    )
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest().upper()[:12]
    return f"ECS-{sequence:02d}-{digest}"


@dataclass(frozen=True)
class EventChainRecord:
    """One ordered, non-executing handoff in an E-CS chain."""

    event_id: str
    chain_id: str
    sequence: int
    system: str
    contract: str
    predecessor: str | None
    successor: str | None
    status: str = "planned"
    return_value: Mapping[str, Any] | None = None
    return_history: tuple[Mapping[str, Any], ...] = ()
    mutated: bool = False
    execute_allowed: bool = False

    def __post_init__(self) -> None:
        if self.return_value is not None:
            object.__setattr__(
                self,
                "return_value",
                freeze_ecs_mapping(self.return_value),
            )
        object.__setattr__(
            self,
            "return_history",
            tuple(freeze_ecs_mapping(item) for item in self.return_history),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "chain_id": self.chain_id,
            "sequence": self.sequence,
            "system": self.system,
            "contract": self.contract,
            "predecessor": self.predecessor,
            "successor": self.successor,
            "status": self.status,
            "return_value": thaw_ecs_mapping(self.return_value)
            if self.return_value is not None
            else None,
            "return_history": [
                thaw_ecs_mapping(item) for item in self.return_history
            ],
            "mutated": self.mutated,
            "execute_allowed": self.execute_allowed,
        }


@dataclass(frozen=True)
class EventChain:
    """Complete E-CS plan for a Cross-X coordination request."""

    chain_id: str
    events: tuple[EventChainRecord, ...]
    contract_version: str = ECS_CONTRACT_VERSION
    state: str = "planned"
    supervisor: str = "AI_SUPERVISOR"
    mutated: bool = False
    human_review_required: bool = True
    governance_gate_required: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract_version": self.contract_version,
            "chain_id": self.chain_id,
            "state": self.state,
            "supervisor": self.supervisor,
            "mutated": self.mutated,
            "human_review_required": self.human_review_required,
            "governance_gate_required": self.governance_gate_required,
            "events": [event.to_dict() for event in self.events],
        }


def build_event_chain(
    *,
    chain_id: str,
    systems: Sequence[str],
    contracts: Mapping[str, Any],
    system_states: Mapping[str, str] | None = None,
    supervisor: str = "AI_SUPERVISOR",
) -> EventChain:
    """Build a deterministic E-CS handoff plan from configured systems."""

    chain_id = normalize_ecs_identifier(chain_id, field="chain_id")
    supervisor = normalize_ecs_identifier(supervisor, field="supervisor")
    if not systems:
        raise ValueError("E-CS requires at least one system")
    if isinstance(systems, (str, bytes)) or not isinstance(systems, Sequence):
        raise ValueError("E-CS systems must be a sequence of strings")
    if not isinstance(contracts, Mapping):
        raise ValueError("E-CS contracts must be a mapping")
    if system_states is not None and not isinstance(system_states, Mapping):
        raise ValueError("E-CS system_states must be a mapping")
    normalized = []
    for index, system in enumerate(systems):
        if not isinstance(system, str) or not system.strip():
            raise ValueError(f"E-CS systems[{index}] must be a non-empty string")
        normalized.append(system.strip())
    normalized = tuple(normalized)
    if len(set(normalized)) != len(normalized):
        raise ValueError("E-CS system names must be unique within a chain")

    states = system_states or {}
    events = []
    for index, system in enumerate(normalized, start=1):
        configured_state = str(states.get(system, "active")).strip().lower()
        active = configured_state in {"active", "ready", "enabled"}
        events.append(
            EventChainRecord(
                event_id=_stable_event_id(chain_id, index, system),
                chain_id=chain_id,
                sequence=index,
                system=system,
                contract=str(contracts.get(system, "observe_handoff_only")),
                predecessor=normalized[index - 2] if index > 1 else None,
                successor=normalized[index] if index < len(normalized) else None,
                status="planned" if active else "inactive",
                return_value=None
                if active
                else {
                    "state": "inactive",
                    "reason": "system_not_in_use",
                    "configured_state": configured_state or "inactive",
                    "handled": True,
                },
            )
        )
    chain_state = "planned" if all(event.status == "planned" for event in events) else "partial"
    return EventChain(
        chain_id=chain_id,
        events=tuple(events),
        state=chain_state,
        supervisor=supervisor,
    )


def bind_event_return(
    chain: EventChain,
    *,
    event_id: str,
    return_value: Mapping[str, Any],
    status: str,
    execute_allowed: bool,
    mutated: bool = False,
) -> EventChain:
    """Return a new E-CS chain with one event result bound exactly once.

    The original chain and record remain unchanged.  This is the canonical
    return path for adapters that execute or observe work outside Cross-X.
    """

    if not isinstance(chain, EventChain):
        raise TypeError("chain must be an EventChain")
    event_id = normalize_ecs_identifier(event_id, field="event_id")
    if not isinstance(return_value, Mapping):
        raise ValueError("E-CS return_value must be a mapping")
    normalized_status = str(status).strip().lower()
    if normalized_status not in {"completed", "waiting", "stopped", "inactive"}:
        raise ValueError(
            "E-CS return status must be completed, waiting, stopped, or inactive"
        )

    matches = [index for index, event in enumerate(chain.events) if event.event_id == event_id]
    if not matches:
        raise ValueError(f"E-CS event_id not found in chain: {event_id}")
    index = matches[0]
    current = chain.events[index]
    if current.return_value is not None and current.status != "waiting":
        raise ValueError(f"E-CS event already has a return value: {event_id}")
    if current.status not in {"planned", "waiting"}:
        raise ValueError(
            f"E-CS event status {current.status!r} cannot accept a return value"
        )

    return_history = current.return_history
    if current.status == "waiting" and current.return_value is not None:
        return_history = return_history + (current.return_value,)
    updated_record = replace(
        current,
        status=normalized_status,
        return_value=dict(return_value),
        return_history=return_history,
        execute_allowed=bool(execute_allowed),
        mutated=bool(mutated),
    )
    events = chain.events[:index] + (updated_record,) + chain.events[index + 1 :]
    statuses = {event.status for event in events}
    if "stopped" in statuses:
        chain_state = "stopped"
    elif all(event.status in _TERMINAL_EVENT_STATES for event in events):
        chain_state = "partial" if "inactive" in statuses else "completed"
    else:
        chain_state = "in_progress"
    return replace(
        chain,
        events=events,
        state=chain_state,
        mutated=chain.mutated or bool(mutated),
    )
