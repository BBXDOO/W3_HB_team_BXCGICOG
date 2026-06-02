"""W3Lgu validation helpers."""

from __future__ import annotations

from dataclasses import dataclass

from protocol.w3lgu.core import FIVE_LINE_ROLES, W3LguFiveLineProgram, W3LguPacket


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    errors: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()


def validate_packet(packet: W3LguPacket) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = list(packet.warnings)
    seen: set[str] = set()
    for pair in packet.pairs:
        if pair.key in seen:
            warnings.append(f"duplicate_key:{pair.key}")
        seen.add(pair.key)
        if pair.key != pair.key.upper():
            errors.append(f"key_not_upper:{pair.key}")
    return ValidationResult(not errors, tuple(errors), tuple(warnings))


def validate_five_line(program: W3LguFiveLineProgram) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    roles = tuple(line.role for line in program.lines)
    if roles != FIVE_LINE_ROLES:
        errors.append("invalid_five_line_roles")
    for line in program.lines:
        result = validate_packet(line.packet)
        errors.extend(f"{line.role}:{error}" for error in result.errors)
        warnings.extend(f"{line.role}:{warning}" for warning in result.warnings)
    signal_state = program.signal.get("STATE")
    signal_color = program.signal.get("COLOR")
    signal_event = program.signal.get("EVENT")
    if not (signal_state or signal_color or signal_event in {"signal", "SIGNAL"}):
        warnings.append("SIGNAL:line5_should_expose_signal_state")
    return ValidationResult(not errors, tuple(errors), tuple(warnings))
