"""Signal envelope helpers kept separate from detection/recovery logic."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from hospitication.core.types import SignalEnvelope


def signal_to_dict(signal: SignalEnvelope) -> dict[str, Any]:
    payload = asdict(signal)
    payload["origin_node"] = {
        "x": signal.origin_node.x,
        "y": signal.origin_node.y,
    }
    return payload
