"""Immutable Event-Chain System (E-CS) contracts for Cross-Series.

E-CS makes the configured Cross-X chain observable as ordered handoffs.  It
does not run subsystems: every event is a plan record carrying the subsystem
contract, predecessor, and governance boundary.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

ECS_CONTRACT_VERSION = "1.0"


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
    mutated: bool = False
    execute_allowed: bool = False

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
            "return_value": dict(self.return_value) if self.return_value is not None else None,
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

    if not chain_id.strip():
        raise ValueError("E-CS chain_id must be non-empty")
    if not systems:
        raise ValueError("E-CS requires at least one system")
    normalized = tuple(str(system).strip() for system in systems)
    if any(not system for system in normalized):
        raise ValueError("E-CS system names must be non-empty")
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
