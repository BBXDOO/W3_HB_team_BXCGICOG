"""Value objects crossing the Cross-L / ENV / MPCP boundary."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping


def _frozen_mapping(value: Mapping[str, Any]) -> Mapping[str, Any]:
    return MappingProxyType(dict(value))


@dataclass(frozen=True)
class EnvironmentSnapshot:
    """Inspectible ENV facts with secret values excluded by construction."""

    platform: str
    platform_release: str
    architecture: str
    python: str
    mobile: bool
    termux: bool
    container: bool
    commands: Mapping[str, str] = field(default_factory=dict)
    variable_names: tuple[str, ...] = ()
    hints: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "commands", _frozen_mapping(self.commands))
        object.__setattr__(self, "hints", _frozen_mapping(self.hints))

    def to_dict(self) -> dict:
        return {
            "platform": self.platform,
            "platform_release": self.platform_release,
            "architecture": self.architecture,
            "python": self.python,
            "mobile": self.mobile,
            "termux": self.termux,
            "container": self.container,
            "commands": dict(self.commands),
            "variable_names": list(self.variable_names),
            "hints": dict(self.hints),
            "secret_values_included": False,
        }


@dataclass(frozen=True)
class MPCPWorkUnit:
    """Normalized work accepted at the MPCP side of the Cross-L boundary."""

    chain_id: str
    event_id: str
    task: str
    intent: str
    scope: str
    boundary: str
    modew: str
    language_tag: str
    language: str
    payload: Mapping[str, Any]
    paper: Mapping[str, Any]
    condien_read: tuple[str, ...]
    condien_deny: tuple[str, ...]
    deny: tuple[str, ...]
    return_contract: tuple[str, ...]
    env: EnvironmentSnapshot
    review: bool

    def __post_init__(self) -> None:
        for name in (
            "chain_id", "event_id", "task", "intent", "scope", "boundary",
            "modew", "language_tag", "language",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"MPCP_ENV:WORK_UNIT_{name.upper()}_REQUIRED")
        object.__setattr__(self, "payload", _frozen_mapping(self.payload))
        object.__setattr__(self, "paper", _frozen_mapping(self.paper))

    def to_mpcp_packet(self) -> dict:
        """Convert only after Cross-L and ENV validation has completed."""

        return {
            "SYSTEM": "mpcp",
            "W3LGU_PROFILE": "W3Lgu-MPCP-Runtime",
            "TASK": self.task,
            "INTENT": self.intent,
            "SCOPE": self.scope,
            "BOUNDARY": self.boundary,
            "MODEW": self.modew,
            "LANGUAGE_TAG": self.language_tag,
            "LANGUAGE": self.language,
            "CHAIN_ID": self.chain_id,
            "EVENT_ID": self.event_id,
            "CONDIEN_READ": list(self.condien_read),
            "CONDIEN_DENY": list(self.condien_deny),
            "DENY": list(self.deny),
            "RETURN_CONTRACT": list(self.return_contract),
            "PAYLOAD": dict(self.payload),
            "PAPER": dict(self.paper),
            "ENV": self.env.to_dict(),
            "REVIEW": self.review,
        }


@dataclass(frozen=True)
class ExecutionAgreement:
    """Temporary authority granted outside Cross-L for one bounded work unit."""

    agreement_id: str
    lender: str
    borrower: str
    capability: str
    chain_id: str
    event_id: str
    boundary: str
    approved_by: str
    active: bool = True

    def __post_init__(self) -> None:
        for name in (
            "agreement_id", "lender", "borrower", "capability", "chain_id",
            "event_id", "boundary", "approved_by",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"MPCP_ENV:AGREEMENT_{name.upper()}_REQUIRED")

    def permits(self, work: MPCPWorkUnit) -> bool:
        return bool(
            self.active
            and self.borrower == "MPCP"
            and self.chain_id == work.chain_id
            and self.event_id == work.event_id
            and self.boundary == work.boundary
            and self.capability in {work.modew, work.language, work.language_tag}
        )

    def to_dict(self) -> dict:
        return {
            "agreement_id": self.agreement_id,
            "lender": self.lender,
            "borrower": self.borrower,
            "capability": self.capability,
            "chain_id": self.chain_id,
            "event_id": self.event_id,
            "boundary": self.boundary,
            "approved_by": self.approved_by,
            "active": self.active,
        }
