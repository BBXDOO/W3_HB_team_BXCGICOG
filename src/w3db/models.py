"""
W3DB Domain Models
------------------
Pure data containers (no persistence logic).

Flow: INPUT → XIZ → TUF → FBD → WHB → PRX
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── XIZ — Execution Trace ─────────────────────────────────────────────────────

@dataclass
class XIZ:
    """
    .xiz  — immutable execution trace record.

    Created at the moment an action is executed.  Once written, the record
    must not be modified (immutable=True enforced by the CRUD layer).
    """
    xiz_id: str
    tuf_id: str                     # FK → TUF
    action: str
    result: str
    timestamp: str = field(default_factory=_now_iso)
    immutable: bool = True

    def to_dict(self) -> dict:
        return {
            "xiz_id": self.xiz_id,
            "tuf_id": self.tuf_id,
            "action": self.action,
            "result": self.result,
            "timestamp": self.timestamp,
            "immutable": self.immutable,
        }


# ── TUF — Process State Snapshot ─────────────────────────────────────────────

@dataclass
class TUF:
    """
    .tuf  — state observation snapshot.

    STATE values: 0 (fail/stable), 0.5 (uncertain), 1 (true/force).
    confidence is a float in [0, 1] that feeds the PRX intensity formula.
    """
    tuf_id: str
    cix_id: str                     # FK → CIX_IDENTITY
    initial: float                  # 0 | 0.5 | 1
    final: float                    # 0 | 0.5 | 1
    confidence: float = 0.5
    resolution: str = ""
    note: str = ""

    def state(self) -> float:
        """Return the canonical observation state derived from confidence."""
        if self.confidence >= 0.8:
            return 1.0
        if self.confidence >= 0.4:
            return 0.5
        return 0.0

    def to_dict(self) -> dict:
        return {
            "tuf_id": self.tuf_id,
            "cix_id": self.cix_id,
            "initial": self.initial,
            "final": self.final,
            "confidence": self.confidence,
            "resolution": self.resolution,
            "note": self.note,
        }


# ── FBD — Failed Boundary Detection ──────────────────────────────────────────

@dataclass
class FBD:
    """
    .fbd  — first deviation / failure boundary record.

    Created when TUF.state() != 1 (i.e. the process did not reach True).
    """
    fbd_id: str
    source_tuf: str                 # FK → TUF.tuf_id
    first_deviation: str
    failure_point: str
    conditions: str
    impact: str
    line3_patch: str = ""           # "IF … THEN …" seed for WHB

    def to_dict(self) -> dict:
        return {
            "fbd_id": self.fbd_id,
            "source_tuf": self.source_tuf,
            "first_deviation": self.first_deviation,
            "failure_point": self.failure_point,
            "conditions": self.conditions,
            "impact": self.impact,
            "line3_patch": self.line3_patch,
        }


# ── WHB — Contextual Law (LINE 3) ─────────────────────────────────────────────

@dataclass
class WHB:
    """
    .whb  — IF → THEN behavioral patch generated from FBD.

    WHB records capture "why this action is taken based on observed reality"
    and are the only place where corrective rules are stored.
    """
    law_id: str
    fbd_id: str                     # FK → FBD.fbd_id
    condition: str                  # "IF …"
    action: str                     # "THEN …"

    def to_dict(self) -> dict:
        return {
            "law_id": self.law_id,
            "fbd_id": self.fbd_id,
            "condition": self.condition,
            "action": self.action,
        }


# ── PRX — Perception Output ───────────────────────────────────────────────────

# Mapping from TUF.state() → (symbol, color)
_STATE_TO_SYMBOL: dict = {
    1.0: ("▲", "RED"),
    0.5: ("●", "YELLOW"),
    0.0: ("■", "GREEN"),
}
_EXTERNAL_SYMBOL = ("◆", "BLUE")


@dataclass
class PRX:
    """
    .prx  — derived visual perception output.

    Rendered from TUF state — never created directly from user input.

    intensity = abs(confidence - 0.5) * scale
    """
    prx_id: str
    tuf_id: str                     # FK → TUF.tuf_id
    symbol: str                     # ▲ | ● | ■ | ◆
    color: str                      # RED | YELLOW | GREEN | BLUE
    intensity: float
    action_required: str = "Observe"

    def to_dict(self) -> dict:
        return {
            "prx_id": self.prx_id,
            "tuf_id": self.tuf_id,
            "symbol": self.symbol,
            "color": self.color,
            "intensity": self.intensity,
            "action_required": self.action_required,
        }

    @staticmethod
    def derive(tuf: TUF, prx_id: str, scale: float = 2.0) -> "PRX":
        """Derive a PRX record from a TUF snapshot."""
        state = tuf.state()
        sym, color = _STATE_TO_SYMBOL.get(state, _EXTERNAL_SYMBOL)
        intensity = abs(tuf.confidence - 0.5) * scale
        action = "Observe" if state == 0.5 else ("Check" if state == 0.0 else "Monitor")
        return PRX(
            prx_id=prx_id,
            tuf_id=tuf.tuf_id,
            symbol=sym,
            color=color,
            intensity=round(intensity, 4),
            action_required=action,
        )
