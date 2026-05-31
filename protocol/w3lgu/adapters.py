"""W3Lgu adapters for text, dict, MPCP, and environment hints."""

from __future__ import annotations

from typing import Mapping

from protocol.w3lgu.core import W3LguPacket, W3LguPair, packet_from_mapping
from protocol.w3lgu.parser import parse_line


def from_text(text: str, *, env: str | None = None, channel: str = "text") -> W3LguPacket:
    packet = parse_line(text, event_name="input")
    if env and not packet.get("ENV"):
        packet = packet.with_pair("ENV", env)
    if not packet.get("CHANNEL"):
        packet = packet.with_pair("CHANNEL", channel)
    return packet


def from_mapping(values: Mapping[str, object], *, env: str | None = None) -> W3LguPacket:
    packet = packet_from_mapping(values)
    if env and not packet.get("ENV"):
        packet = packet.with_pair("ENV", env)
    return packet


def to_mpcp(packet: W3LguPacket) -> dict[str, str]:
    """Bridge W3Lgu packet to a minimal MPCP-style execution packet."""

    task = packet.get("TASK") or packet.get("EVENT") or ""
    state = packet.get("STATE") or "ready"
    return {
        "CAUSE": task,
        "state": state,
        "error": "" if state not in {"fail", "STOP"} else state,
        "w3lgu": packet.to_text(),
    }


def from_mpcp(payload: Mapping[str, object]) -> W3LguPacket:
    pairs = [
        W3LguPair("EVENT", "mpcp.receive"),
        W3LguPair("TASK", str(payload.get("CAUSE", ""))),
        W3LguPair("STATE", str(payload.get("state", "ready"))),
    ]
    error = payload.get("error")
    if error:
        pairs.append(W3LguPair("ERROR", str(error)))
    return W3LguPacket(tuple(pairs))
