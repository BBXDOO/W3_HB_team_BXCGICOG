"""W3Lgu parser.

The parser accepts compact human-readable lines and normalizes them into explicit
KEY:VALUE packets. It repairs only obvious separator omissions (Line C behavior)
and records warnings instead of hiding ambiguity.
"""

from __future__ import annotations

import re

from protocol.w3lgu.core import FIVE_LINE_ROLES, W3LguError, W3LguFiveLineProgram, W3LguLine, W3LguPacket, W3LguPair

_FIELD_RE = re.compile(r"([A-Za-z][A-Za-z0-9_]*)\s*:")


def parse_line(text: str, *, event_name: str | None = None) -> W3LguPacket:
    """Parse one W3Lgu line into a normalized packet."""

    if not isinstance(text, str):
        raise TypeError("W3Lgu line must be a string")
    source = text.strip()
    if not source:
        raise W3LguError("Cannot parse empty W3Lgu line")

    line = source[:-1].strip() if source.endswith(".") else source
    pairs: list[W3LguPair] = []
    warnings: list[str] = []

    matches = list(_FIELD_RE.finditer(line))
    if not matches:
        if event_name:
            return W3LguPacket((W3LguPair("EVENT", event_name), W3LguPair("TEXT", line)), source=source)
        raise W3LguError(f"No KEY:VALUE pairs found in line: {text!r}")

    if event_name and not line.upper().startswith("EVENT:"):
        pairs.append(W3LguPair("EVENT", event_name))

    for index, match in enumerate(matches):
        key = match.group(1)
        value_start = match.end()
        value_end = matches[index + 1].start() if index + 1 < len(matches) else len(line)
        raw_value = line[value_start:value_end].strip(" ,;")
        if " " in raw_value and "," not in raw_value and "'" not in raw_value:
            warnings.append(f"repaired_separator:{key.upper()}")
            raw_value = "/".join(part for part in raw_value.split() if part)
        pairs.append(W3LguPair(key, raw_value))

    return W3LguPacket(tuple(pairs), source=source, warnings=tuple(warnings))


def normalize_line(text: str, *, event_name: str | None = None) -> str:
    return parse_line(text, event_name=event_name).to_text()


def split_events(text: str) -> tuple[W3LguPacket, ...]:
    """Split semicolon-separated W3Lgu events."""

    parts = [part.strip() for part in text.strip().split(";") if part.strip()]
    return tuple(parse_line(part) for part in parts)


def parse_five_line_program(text: str) -> W3LguFiveLineProgram:
    """Parse canonical 5-line W3Lgu program text."""

    raw_lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(raw_lines) != 5:
        raise W3LguError(f"W3Lgu five-line program requires 5 lines, got {len(raw_lines)}")

    parsed: list[W3LguLine] = []
    for expected_role, raw in zip(FIVE_LINE_ROLES, raw_lines):
        if ":" not in raw:
            raise W3LguError(f"Missing role prefix for line {expected_role}")
        role, payload = raw.split(":", 1)
        role = role.strip().upper()
        if role != expected_role:
            raise W3LguError(f"Expected line role {expected_role}, got {role}")
        parsed.append(W3LguLine(expected_role, parse_line(payload)))
    return W3LguFiveLineProgram(tuple(parsed))
