"""W3-API → W3Lgu adapter.

This adapter creates a five-line W3Lgu packet. It does not execute runtime
actions and does not mutate W3DB, MPCP, EP_SIGNAL, or existing W3Lgu state.
"""

from __future__ import annotations

from typing import Any

from protocol.w3lgu import W3LguFiveLineProgram, parse_five_line_program, validate_five_line


def build_cross_w3lgu_packet(
    *,
    source: str,
    intent: str,
    target: str | None,
    mode: str,
    payload: dict[str, Any] | None = None,
) -> W3LguFiveLineProgram:
    """Build a valid five-line W3Lgu gateway packet."""

    payload = payload or {}
    target_value = target or "auto"
    contract = str(payload.get("contract", "observe_only"))
    text = "\n".join(
        (
            f"MEM:SOURCE:{_clean(source)}",
            f"PATCH:MODE:{_clean(mode)}",
            f"LAW:TARGET:{_clean(target_value)},CONTRACT:{_clean(contract)}",
            f"EVENT:INTENT:{_clean(intent)}",
            "SIGNAL:STATUS:received,TRACEABLE:true",
        )
    )
    program = parse_five_line_program(text)
    result = validate_five_line(program)
    if not result.ok:
        raise ValueError(f"Invalid W3Lgu cross packet: {result.errors}")
    return program


def _clean(value: str) -> str:
    """Keep W3Lgu text single-line and packet-safe without changing meaning."""

    return " ".join(str(value).replace("\n", " ").replace("\r", " ").split())
