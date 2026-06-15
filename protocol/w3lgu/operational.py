"""Production operational contract for W3Lgu.

The original W3Lgu modules provide the compact packet grammar.  This module
adds the minimum operational semantics shared by W3 systems:

* six event rooms;
* PX positions and a Cross-X point of convergence (POC);
* the REDR -> PSP2 -> DTML -> LRC2 event chain;
* an append-only, hash-linked LRC2 ledger; and
* 27 explicit minimum laws that other systems can adopt as a template.

The runtime performs real classification, routing, governance, and recording.
It deliberately does not perform the external action described by a packet;
that authority belongs to an explicitly approved adapter after DTML review.
"""

from __future__ import annotations

import hashlib
import json
import re
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from protocol.w3lgu.core import W3LguError, W3LguPacket
from protocol.w3lgu.parser import parse_line

ROOM_CODES = ("CA", "CU", "RE", "SI", "AP", "EV")
STAGES = ("REDR", "PSP2", "DTML", "LRC2")
GENESIS_HASH = "0" * 64

_PX_RE = re.compile(
    r"^(?:PX\s*:\s*)?LN(?P<room>CA|CU|RE|SI|AP|EV)'(?P<position>[0-9]{4})$",
    re.IGNORECASE,
)
_OPERATIONAL_IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _stable_id(prefix: str, value: object, *, length: int = 20) -> str:
    digest = hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest().upper()
    return f"{prefix}-{digest[:length]}"


def _immutable_mapping(value: Mapping[str, Any]) -> Mapping[str, Any]:
    return MappingProxyType(dict(value))


def _normalize_operational_identifier(value: object, *, field: str) -> str:
    """Return a delimiter-safe identifier for emitted operational text."""

    if not isinstance(value, str):
        raise W3LguError(f"{field} must be a string")
    normalized = value.strip()
    if not _OPERATIONAL_IDENTIFIER_RE.fullmatch(normalized):
        raise W3LguError(
            f"{field} must use 1-128 letters, digits, '.', '_' or '-'"
        )
    return normalized


def _require_unique_packet_keys(packet: W3LguPacket) -> None:
    """Reject ambiguous packets before governance or durable recording."""

    seen: set[str] = set()
    duplicates: set[str] = set()
    for pair in packet.pairs:
        if pair.key in seen:
            duplicates.add(pair.key)
        seen.add(pair.key)
    if duplicates:
        joined = ",".join(sorted(duplicates))
        raise W3LguError(f"Operational packet keys must be unique: {joined}")


@dataclass(frozen=True)
class RoomSpec:
    """One of the six non-sequential W3Lgu event rooms."""

    number: int
    code: str
    name: str
    meaning: str

    def to_dict(self) -> dict[str, object]:
        return {
            "number": self.number,
            "code": self.code,
            "name": self.name,
            "meaning": self.meaning,
        }


ROOMS: tuple[RoomSpec, ...] = (
    RoomSpec(1, "CA", "CAUSE", "cause"),
    RoomSpec(2, "CU", "CAUSE_RESULT", "cause and result"),
    RoomSpec(3, "RE", "RESULT", "result"),
    RoomSpec(4, "SI", "SITUATION", "situation"),
    RoomSpec(5, "AP", "APPEARANCE", "appearance or observed phenomenon"),
    RoomSpec(6, "EV", "EVENT", "event"),
)
ROOM_BY_CODE = MappingProxyType({room.code: room for room in ROOMS})


@dataclass(frozen=True)
class MinimumLaw:
    """A machine-readable minimum law for W3Lgu implementations."""

    number: int
    code: str
    statement: str


MINIMUM_LAWS: tuple[MinimumLaw, ...] = (
    MinimumLaw(1, "READ_LR", "Read left to right."),
    MinimumLaw(2, "READ_UD", "Read top to bottom."),
    MinimumLaw(3, "UPPER_DECL", "Commands, variables, and functions declare uppercase keys."),
    MinimumLaw(4, "COLON_CONTEXT", "Colon binds one key to its context."),
    MinimumLaw(5, "SEMICOLON_EVENT", "Semicolon separates events."),
    MinimumLaw(6, "DOT_END", "Dot closes an event or command."),
    MinimumLaw(7, "APOSTROPHE_SPACE", "Apostrophe separates values sharing one space."),
    MinimumLaw(8, "COMMA_DATA", "Comma separates independent raw data in one space."),
    MinimumLaw(9, "SLASH_RELATION", "Slash relates an activity to its context or result."),
    MinimumLaw(10, "UNDERSCORE_INTENT", "Underscore marks requested or expected input."),
    MinimumLaw(11, "BANG_INCOMPLETE", "Exclamation marks incomplete, harmful, or unresolved data."),
    MinimumLaw(12, "HASH_BOUNDARY", "Hash establishes an explicit governed boundary."),
    MinimumLaw(13, "QUOTE_HISTORY", "Quote marks a previously observed repeatable pattern."),
    MinimumLaw(14, "TILDE_CONCURRENT", "Tilde relates concurrent activities."),
    MinimumLaw(15, "BRACKET_AUTHORITY", "Brackets contain the authority of a local work zone."),
    MinimumLaw(16, "PX_POSITION", "Every operational event has an explicit or derived PX position."),
    MinimumLaw(17, "POC_CROSS_X", "POC identifies the Cross-X convergence point."),
    MinimumLaw(18, "ROOM_NONLINEAR", "The six rooms classify context; they do not force flow order."),
    MinimumLaw(19, "REDR_PACKAGE", "REDR classifies, tags, packages, and duplicates without rewriting truth."),
    MinimumLaw(20, "PSP2_ROUTE", "PSP2 stamps and routes without inspecting or modifying payload truth."),
    MinimumLaw(21, "DTML_DECIDE", "DTML reviews destination, signal, intent, and risk before authority."),
    MinimumLaw(22, "DTML_STOP", "DTML immediately stops unresolved harmful or invalid activity."),
    MinimumLaw(23, "LRC2_APPEND", "LRC2 appends every outcome, including failure and stop."),
    MinimumLaw(24, "LRC2_IMMUTABLE", "LRC2 history is hash-linked and cannot be edited in place."),
    MinimumLaw(25, "HALF_OBSERVE", "Confidence 0.5 is observable uncertainty, never final truth."),
    MinimumLaw(26, "NO_IMPLICIT_MAGIC", "Derived meaning must be exposed in tags, room, signal, or trace."),
    MinimumLaw(27, "EXPLICIT_AUTHORITY", "External execution requires a separate approved adapter."),
)


@dataclass(frozen=True)
class PXPosition:
    """A position in the six-room W3Lgu plane.

    ``LNCU'0001`` means horizontal position 1 in room CU.  The room number is
    the vertical coordinate, so this notation remains compact while preserving
    an unambiguous X/Y intersection.
    """

    room: str
    position: int

    def __post_init__(self) -> None:
        room = str(self.room).strip().upper()
        if room not in ROOM_BY_CODE:
            raise W3LguError(f"Unknown W3Lgu room: {self.room!r}")
        if isinstance(self.position, bool) or not isinstance(self.position, int):
            raise W3LguError("PX position must be an integer")
        if not 1 <= self.position <= 9999:
            raise W3LguError("PX position must be between 0001 and 9999")
        object.__setattr__(self, "room", room)

    @property
    def x(self) -> int:
        return self.position

    @property
    def y(self) -> int:
        return ROOM_BY_CODE[self.room].number

    @property
    def relative_point(self) -> tuple[int, int]:
        return (self.x, self.y)

    def to_text(self) -> str:
        return f"LN{self.room}'{self.position:04d}"

    def to_dict(self) -> dict[str, object]:
        return {
            "px": self.to_text(),
            "room": self.room,
            "x": self.x,
            "y": self.y,
            "relative_point": [self.x, self.y],
        }

    @classmethod
    def parse(cls, value: str) -> "PXPosition":
        if not isinstance(value, str):
            raise W3LguError("PX notation must be a string")
        match = _PX_RE.fullmatch(value.strip())
        if not match:
            raise W3LguError("PX notation must use LN<ROOM>'<0001-9999>, for example LNCU'0001")
        return cls(match.group("room"), int(match.group("position")))


@dataclass(frozen=True)
class PointOfConvergence:
    """Cross-X convergence point shared by related W3Lgu events."""

    cross_id: str
    x: int
    y: int

    def __post_init__(self) -> None:
        cross_id = _normalize_operational_identifier(self.cross_id, field="POC cross_id")
        if self.x < 1 or self.y < 1:
            raise W3LguError("POC coordinates must be positive")
        object.__setattr__(self, "cross_id", cross_id)

    def to_text(self) -> str:
        return f"POC'{self.cross_id}'X{self.x:04d}'Y{self.y:04d}"


@dataclass(frozen=True)
class OperationalPackage:
    """Immutable REDR package passed by reference through the event chain."""

    package_id: str
    packet: W3LguPacket
    room: RoomSpec
    px: PXPosition
    poc: PointOfConvergence
    tags: tuple[str, ...]
    duplicate_to: tuple[str, ...] = ("PSP2", "LRC2")

    def to_dict(self) -> dict[str, object]:
        return {
            "package_id": self.package_id,
            "packet": self.packet.to_dict(),
            "room": self.room.to_dict(),
            "px": self.px.to_dict(),
            "poc": self.poc.to_text(),
            "tags": list(self.tags),
            "duplicate_to": list(self.duplicate_to),
        }


@dataclass(frozen=True)
class OperationalStage:
    """One auditable stage transition."""

    stage: str
    status: str
    action: str
    data: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        stage = str(self.stage).strip().upper()
        if stage not in STAGES:
            raise W3LguError(f"Unknown operational stage: {self.stage!r}")
        object.__setattr__(self, "stage", stage)
        object.__setattr__(self, "data", _immutable_mapping(self.data))

    def to_dict(self) -> dict[str, object]:
        return {
            "stage": self.stage,
            "status": self.status,
            "action": self.action,
            "data": dict(self.data),
        }


@dataclass(frozen=True)
class LRC2Record:
    """One append-only, hash-linked history record."""

    sequence: int
    record_id: str
    timestamp: str
    event_id: str
    package_id: str
    stage: str
    status: str
    payload: Mapping[str, Any]
    previous_hash: str
    record_hash: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "payload", _immutable_mapping(self.payload))

    def to_dict(self) -> dict[str, object]:
        return {
            "sequence": self.sequence,
            "record_id": self.record_id,
            "timestamp": self.timestamp,
            "event_id": self.event_id,
            "package_id": self.package_id,
            "stage": self.stage,
            "status": self.status,
            "payload": dict(self.payload),
            "previous_hash": self.previous_hash,
            "record_hash": self.record_hash,
        }


class LRC2Ledger:
    """Thread-safe append-only ledger with idempotent event recording."""

    def __init__(self) -> None:
        self._records: list[LRC2Record] = []
        self._event_index: dict[str, LRC2Record] = {}
        self._lock = threading.RLock()

    def __len__(self) -> int:
        with self._lock:
            return len(self._records)

    def records(self) -> tuple[LRC2Record, ...]:
        with self._lock:
            return tuple(self._records)

    def append(
        self,
        *,
        event_id: str,
        package_id: str,
        stage: str,
        status: str,
        payload: Mapping[str, Any],
        timestamp: str | None = None,
    ) -> LRC2Record:
        event_id = str(event_id).strip()
        if not event_id:
            raise W3LguError("LRC2 event_id must be non-empty")
        with self._lock:
            existing = self._event_index.get(event_id)
            if existing is not None:
                return existing
            sequence = len(self._records) + 1
            previous_hash = self._records[-1].record_hash if self._records else GENESIS_HASH
            body = {
                "sequence": sequence,
                "event_id": event_id,
                "package_id": package_id,
                "stage": stage,
                "status": status,
                "payload": dict(payload),
                "previous_hash": previous_hash,
            }
            record_hash = hashlib.sha256(_canonical(body).encode("utf-8")).hexdigest()
            record = LRC2Record(
                sequence=sequence,
                record_id=f"LRC2-{record_hash[:20].upper()}",
                timestamp=timestamp or _now_iso(),
                event_id=event_id,
                package_id=package_id,
                stage=stage,
                status=status,
                payload=payload,
                previous_hash=previous_hash,
                record_hash=record_hash,
            )
            self._records.append(record)
            self._event_index[event_id] = record
            return record

    def verify(self) -> bool:
        with self._lock:
            previous_hash = GENESIS_HASH
            seen: set[str] = set()
            for expected_sequence, record in enumerate(self._records, start=1):
                if record.sequence != expected_sequence or record.event_id in seen:
                    return False
                body = {
                    "sequence": record.sequence,
                    "event_id": record.event_id,
                    "package_id": record.package_id,
                    "stage": record.stage,
                    "status": record.status,
                    "payload": dict(record.payload),
                    "previous_hash": previous_hash,
                }
                expected_hash = hashlib.sha256(_canonical(body).encode("utf-8")).hexdigest()
                if record.previous_hash != previous_hash or record.record_hash != expected_hash:
                    return False
                seen.add(record.event_id)
                previous_hash = record.record_hash
            return True


@dataclass(frozen=True)
class OperationalResult:
    """Complete result of one W3Lgu operational event."""

    event_id: str
    package: OperationalPackage
    stages: tuple[OperationalStage, ...]
    decision: str
    signal: str
    execute_allowed: bool
    lrc2_records: tuple[LRC2Record, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "event_id": self.event_id,
            "package": self.package.to_dict(),
            "stages": [stage.to_dict() for stage in self.stages],
            "decision": self.decision,
            "signal": self.signal,
            "execute_allowed": self.execute_allowed,
            "lrc2_records": [record.to_dict() for record in self.lrc2_records],
        }


class W3LguOperationalRuntime:
    """Operational W3Lgu engine with explicit policy and an LRC2 ledger."""

    def __init__(self, *, ledger: LRC2Ledger | None = None) -> None:
        self.ledger = ledger if ledger is not None else LRC2Ledger()

    def process_line(
        self,
        text: str,
        *,
        cross_id: str | None = None,
        timestamp: str | None = None,
    ) -> OperationalResult:
        return self.process_packet(parse_line(text), cross_id=cross_id, timestamp=timestamp)

    def process_packet(
        self,
        packet: W3LguPacket,
        *,
        cross_id: str | None = None,
        timestamp: str | None = None,
    ) -> OperationalResult:
        _require_unique_packet_keys(packet)
        room, room_basis = classify_room(packet)
        px, px_basis = resolve_px(packet, room)
        supplied_cross_id = cross_id if cross_id is not None else packet.get("CROSS_ID")
        if supplied_cross_id is None:
            resolved_cross_id = _stable_id("CROSS", packet.to_dict(), length=16)
        else:
            resolved_cross_id = _normalize_operational_identifier(
                supplied_cross_id,
                field="POC cross_id",
            )
        poc = PointOfConvergence(resolved_cross_id, px.x, px.y)
        tags = _derive_tags(packet, room, room_basis, px_basis)
        package_body = {
            "packet": packet.to_dict(),
            "room": room.code,
            "px": px.to_text(),
            "poc": poc.to_text(),
            "tags": tags,
        }
        package = OperationalPackage(
            package_id=_stable_id("PKG", package_body),
            packet=packet,
            room=room,
            px=px,
            poc=poc,
            tags=tags,
        )
        event_id = _stable_id("EVT", {"package": package.package_id, "cross": resolved_cross_id})

        redr = OperationalStage(
            "REDR",
            "PACKAGED",
            "READ_CLASSIFY_TAG_DUPLICATE",
            {
                "room": room.code,
                "room_basis": room_basis,
                "tags": tags,
                "duplicate_to": package.duplicate_to,
            },
        )
        target = str(packet.get("TARGET") or room.code).strip().upper()
        psp2 = OperationalStage(
            "PSP2",
            "ROUTED",
            "STAMP_ROUTE_ONLY",
            {
                "stamp": f"PSP2'{event_id}",
                "route": ("W3LGU", px.to_text(), target, "LRC2"),
                "payload_changed": False,
            },
        )
        decision, signal, reasons = _dtml_decision(packet, target)
        dtml = OperationalStage(
            "DTML",
            decision,
            "INSPECT_DESTINATION_SIGNAL_INTENT",
            {
                "target": target,
                "signal": signal,
                "reasons": reasons,
                "external_authority": False,
            },
        )
        lrc2 = OperationalStage(
            "LRC2",
            "RECORDED",
            "APPEND_HASH_LINKED_HISTORY",
            {
                "event_id": event_id,
                "decision": decision,
                "record_count": len(STAGES),
            },
        )
        stages = (redr, psp2, dtml, lrc2)
        records = tuple(
            self.ledger.append(
                event_id=f"{event_id}:{stage.stage}",
                package_id=package.package_id,
                stage=stage.stage,
                status=stage.status,
                payload=stage.to_dict(),
                timestamp=timestamp,
            )
            for stage in stages
        )
        return OperationalResult(
            event_id=event_id,
            package=package,
            stages=stages,
            decision=decision,
            signal=signal,
            execute_allowed=False,
            lrc2_records=records,
        )


def classify_room(packet: W3LguPacket) -> tuple[RoomSpec, str]:
    """Classify an event room using explicit fields before deterministic hints."""

    explicit = packet.get("ROOM") or packet.get("TYPE")
    if explicit:
        code = str(explicit).strip().upper()
        if code.startswith("ROOM") and code[4:].isdigit():
            number = int(code[4:])
            if 1 <= number <= len(ROOMS):
                return ROOMS[number - 1], "explicit_number"
        if code in ROOM_BY_CODE:
            return ROOM_BY_CODE[code], "explicit_code"
        raise W3LguError(f"Unknown W3Lgu room declaration: {explicit!r}")

    keys = set(packet.to_dict())
    if {"CAUSE", "RESULT"} <= keys:
        return ROOM_BY_CODE["CU"], "keys:CAUSE+RESULT"
    hints = (
        ("CA", {"CAUSE"}),
        ("RE", {"RESULT", "OUTCOME"}),
        ("SI", {"SITUATION", "CONTEXT"}),
        ("AP", {"APPEARANCE", "OBSERVED", "PHENOMENON"}),
        ("EV", {"EVENT", "TASK", "ACTION"}),
    )
    for code, candidates in hints:
        matched = keys & candidates
        if matched:
            return ROOM_BY_CODE[code], f"keys:{'+'.join(sorted(matched))}"
    return ROOM_BY_CODE["EV"], "default_event"


def resolve_px(packet: W3LguPacket, room: RoomSpec) -> tuple[PXPosition, str]:
    explicit = packet.get("PX")
    if explicit:
        px = PXPosition.parse(str(explicit))
        if px.room != room.code:
            raise W3LguError(
                f"PX room {px.room} conflicts with classified room {room.code}"
            )
        return px, "explicit"
    digest = hashlib.sha256(_canonical(packet.to_dict()).encode("utf-8")).digest()
    position = int.from_bytes(digest[:2], "big") % 9999 + 1
    return PXPosition(room.code, position), "derived_stable"


def operational_template() -> dict[str, object]:
    """Return the minimum contract other W3 systems can adopt."""

    return {
        "version": "1.0",
        "rooms": [room.to_dict() for room in ROOMS],
        "stages": list(STAGES),
        "laws": [
            {"number": law.number, "code": law.code, "statement": law.statement}
            for law in MINIMUM_LAWS
        ],
        "px_example": PXPosition("CU", 1).to_text(),
        "poc": "Cross-X",
        "external_execution": "approved_adapter_only",
    }


def _derive_tags(
    packet: W3LguPacket,
    room: RoomSpec,
    room_basis: str,
    px_basis: str,
) -> tuple[str, ...]:
    tags = {
        f"ROOM_{room.code}",
        f"ROOM_BASIS_{room_basis.upper().replace(':', '_').replace('+', '_')}",
        f"PX_{px_basis.upper()}",
    }
    source = packet.source
    if "!" in source:
        tags.add("UNRESOLVED")
    if "#" in source:
        tags.add("GOVERNED_BOUNDARY")
    if "~" in source:
        tags.add("CONCURRENT")
    if '"' in source:
        tags.add("KNOWN_PATTERN")
    return tuple(sorted(tags))


def _dtml_decision(packet: W3LguPacket, target: str) -> tuple[str, str, tuple[str, ...]]:
    reasons: list[str] = []
    state = str(packet.get("STATE") or "").strip().upper()
    confidence = _parse_confidence(packet.get("CONF"))
    source = packet.source

    if not target:
        reasons.append("TARGET_MISSING")
    if "!" in source:
        reasons.append("UNRESOLVED_OR_HARMFUL_MARKER")
    if state in {"STOP", "BLOCK", "FAIL"}:
        reasons.append(f"STATE_{state}")
    if confidence is not None and confidence <= 0:
        reasons.append("CONFIDENCE_ZERO")

    if reasons:
        return "STOP", "RED", tuple(reasons)
    if confidence == 0.5:
        return "REVIEW", "YELLOW", ("CONFIDENCE_HALF",)
    return "READY", "GREEN", ("BOUNDARY_CLEAR",)


def _parse_confidence(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        confidence = float(value)
    except (TypeError, ValueError) as exc:
        raise W3LguError(f"CONF must be numeric, got {value!r}") from exc
    if not 0 <= confidence <= 1:
        raise W3LguError("CONF must be between 0 and 1")
    return confidence


def validate_minimum_laws(laws: Iterable[MinimumLaw] = MINIMUM_LAWS) -> bool:
    values = tuple(laws)
    return (
        len(values) == 27
        and tuple(law.number for law in values) == tuple(range(1, 28))
        and len({law.code for law in values}) == 27
    )
