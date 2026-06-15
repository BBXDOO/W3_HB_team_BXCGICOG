"""W3Lgu core contracts.

This module captures the smallest faithful runtime contract from the W3Lgu
papers: one readable language, explicit KEY:VALUE packets, and the five-line
operational shape that preserves memory, patch, law, event, and signal as
separate layers.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal, Mapping

W3LguLineRole = Literal["MEM", "PATCH", "LAW", "EVENT", "SIGNAL"]

FIVE_LINE_ROLES: tuple[W3LguLineRole, ...] = ("MEM", "PATCH", "LAW", "EVENT", "SIGNAL")
COMMAND_KEYS = frozenset({"EVENT", "TASK", "MODE", "MODEW", "CONDIEN", "STATE", "ENV", "LAW", "PATCH"})


class W3LguError(ValueError):
    """Raised when a W3Lgu packet cannot preserve the language contract."""


@dataclass(frozen=True, order=True)
class W3LguPair:
    """One explicit KEY:VALUE pair."""

    key: str
    value: str

    def __post_init__(self) -> None:
        key = self.key.strip().upper()
        value = self.value.strip()
        if not key:
            raise W3LguError("W3Lgu key must be non-empty")
        if not key.replace("_", "").isalnum() or not key[0].isalpha():
            raise W3LguError(f"Invalid W3Lgu key: {self.key!r}")
        object.__setattr__(self, "key", key)
        object.__setattr__(self, "value", value)

    def to_text(self) -> str:
        return f"{self.key}:{self.value}"


@dataclass(frozen=True)
class W3LguPacket:
    """Normalized W3Lgu packet: explicit, ordered, compact, replayable."""

    pairs: tuple[W3LguPair, ...]
    source: str = ""
    warnings: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.pairs:
            raise W3LguError("W3LguPacket requires at least one pair")

    def get(self, key: str, default: str | None = None) -> str | None:
        wanted = key.upper()
        for pair in self.pairs:
            if pair.key == wanted:
                return pair.value
        return default

    def with_pair(self, key: str, value: str) -> "W3LguPacket":
        filtered = tuple(pair for pair in self.pairs if pair.key != key.upper())
        return W3LguPacket(filtered + (W3LguPair(key, value),), self.source, self.warnings)

    def to_dict(self) -> dict[str, str]:
        return {pair.key: pair.value for pair in self.pairs}

    def to_text(self) -> str:
        return ",".join(pair.to_text() for pair in self.pairs)


@dataclass(frozen=True)
class W3LguLine:
    """One line inside the five-line operating shape."""

    role: W3LguLineRole
    packet: W3LguPacket

    def __post_init__(self) -> None:
        if self.role not in FIVE_LINE_ROLES:
            raise W3LguError(f"Unknown W3Lgu line role: {self.role!r}")

    def to_text(self) -> str:
        return f"{self.role}:{self.packet.to_text()}"


@dataclass(frozen=True)
class W3LguFiveLineProgram:
    """Canonical five-line W3Lgu operating unit.

    Line 1: MEM    — system reserve / compact continuity memory
    Line 2: PATCH  — training patch / protective example
    Line 3: LAW    — strict law zone, never runtime log decoration
    Line 4: EVENT  — the actionable event packet
    Line 5: SIGNAL — visible state/perception output
    """

    lines: tuple[W3LguLine, ...]
    references: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        roles = tuple(line.role for line in self.lines)
        if roles != FIVE_LINE_ROLES:
            raise W3LguError(
                "W3Lgu five-line program must use roles "
                f"{FIVE_LINE_ROLES}, got {roles}"
            )

    @property
    def memory(self) -> W3LguPacket:
        return self.lines[0].packet

    @property
    def patch(self) -> W3LguPacket:
        return self.lines[1].packet

    @property
    def law(self) -> W3LguPacket:
        return self.lines[2].packet

    @property
    def event(self) -> W3LguPacket:
        return self.lines[3].packet

    @property
    def signal(self) -> W3LguPacket:
        return self.lines[4].packet

    def to_text(self) -> str:
        return "\n".join(line.to_text() for line in self.lines)

    def to_dict(self) -> dict[str, object]:
        return {
            "lines": {line.role: line.packet.to_dict() for line in self.lines},
            "references": list(self.references),
        }


def packet_from_mapping(values: Mapping[str, object], *, source: str = "") -> W3LguPacket:
    """Create a packet from a mapping while preserving sorted deterministic order."""

    pairs = tuple(W3LguPair(key, str(values[key])) for key in sorted(values))
    return W3LguPacket(pairs, source=source)


def ensure_packet(value: W3LguPacket | Mapping[str, object] | Iterable[W3LguPair]) -> W3LguPacket:
    if isinstance(value, W3LguPacket):
        return value
    if isinstance(value, Mapping):
        return packet_from_mapping(value)
    return W3LguPacket(tuple(value))
