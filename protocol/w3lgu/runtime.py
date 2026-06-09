"""Low-overhead W3Lgu runtime."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from protocol.w3lgu.core import W3LguFiveLineProgram, W3LguPacket, W3LguPair
from protocol.w3lgu.parser import parse_line
from protocol.w3lgu.signals import signal_for_state


@dataclass(frozen=True)
class W3LguRuntimeResult:
    input_packet: W3LguPacket
    normalized_packet: W3LguPacket
    signal_packet: W3LguPacket
    memory_packet: W3LguPacket | None = None

    def to_text(self) -> str:
        lines = [
            f"EVENT:runtime.receive,{self.input_packet.to_text()}",
            f"EVENT:runtime.normalized,{self.normalized_packet.to_text()}",
            self.signal_packet.to_text(),
        ]
        if self.memory_packet:
            lines.append(f"EVENT:commit,{self.memory_packet.to_text()}")
        return "\n".join(lines)


def run_packet(packet: W3LguPacket, *, context: Mapping[str, object] | None = None) -> W3LguRuntimeResult:
    """Normalize and signal a packet without executing external side effects."""

    context = context or {}
    state = packet.get("STATE") or "ready"
    modew = packet.get("MODEW") or context.get("MODEW")
    normalized = packet
    if not packet.get("EVENT"):
        normalized = W3LguPacket((W3LguPair("EVENT", "runtime.receive"),) + packet.pairs, source=packet.source)
    if modew and not normalized.get("MODEW"):
        normalized = normalized.with_pair("MODEW", str(modew))

    confidence = _confidence(packet.get("CONF"))
    signal = signal_for_state(str(state), confidence=confidence)
    memory = W3LguPacket((
        W3LguPair("LAST_STATE", signal.get("STATE") or str(state)),
        W3LguPair("LAST_EVENT", normalized.get("EVENT") or "runtime.receive"),
    ))
    return W3LguRuntimeResult(packet, normalized, signal, memory)


def run_line(text: str, *, context: Mapping[str, object] | None = None) -> W3LguRuntimeResult:
    return run_packet(parse_line(text), context=context)


def run_five_line(program: W3LguFiveLineProgram) -> W3LguRuntimeResult:
    """Run the event line while preserving MEM/PATCH/LAW/SIGNAL boundaries."""

    context = {
        "MEM": program.memory.to_text(),
        "PATCH": program.patch.to_text(),
        "LAW": program.law.to_text(),
    }
    return run_packet(program.event, context=context)


def _confidence(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None
