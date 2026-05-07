"""
W3DB Data Models
----------------
Plain dataclasses for each domain in the W3 relation flow:

  XIZ  — Execution trace (action log)
  TUF  — Process state snapshot (observation: 0 / 0.5 / 1)
  FBD  — Failed boundary detection
  WHB  — Contextual law / IF-THEN patch (Line 3)
  PRX  — Perception output (visual signaling — derived only)

All IDs are caller-assigned strings (e.g. "XIZ-001").
Timestamps are ISO-8601 strings; pass datetime.utcnow().isoformat() or
any comparable string.
"""

from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Allowed observation states (0 = Fail, 0.5 = Uncertain, 1 = True)
# ---------------------------------------------------------------------------

OBSERVATION_STATES = frozenset({"0", "0.5", "1"})

# Allowed symbols & colors (PRX)
PRX_SYMBOLS = frozenset({"▲", "●", "■", "◆"})
PRX_COLORS = frozenset({"RED", "YELLOW", "GREEN", "BLUE"})

# Failure levels (FBD)
FBD_FAILURE_LEVELS = frozenset({"Red", "Yellow", "Green", "Blue"})


# ---------------------------------------------------------------------------
# Domain models
# ---------------------------------------------------------------------------

@dataclass
class XIZ:
    """
    Execution trace record.

    Fields:
      xiz_id    — unique identifier  (e.g. "XIZ-001")
      tuf_id    — FK to linked TUF record (may be set after creation)
      action    — human-readable description of the action taken
      timestamp — ISO-8601 creation time
      result    — outcome text
      immutable — once True, record must not be modified
    """

    xiz_id: str
    action: str
    timestamp: str
    result: str = ""
    tuf_id: Optional[str] = None
    immutable: bool = False

    def to_dict(self) -> dict:
        return {
            "xiz_id": self.xiz_id,
            "tuf_id": self.tuf_id,
            "action": self.action,
            "timestamp": self.timestamp,
            "result": self.result,
            "immutable": self.immutable,
        }


@dataclass
class TUF:
    """
    Process state snapshot (observation only).

    Fields:
      tuf_id     — unique identifier  (e.g. "TUF-001")
      cix_id     — FK to identity (CIX_IDENTITY)
      initial    — observation state at start   "0" | "0.5" | "1"
      final      — observation state at end     "0" | "0.5" | "1"
      confidence — float in [0.0, 1.0] (optional — used by PRX intensity)
      resolution — free-text resolution note
      note       — additional notes
    """

    tuf_id: str
    cix_id: Optional[str] = None
    initial: str = "0.5"
    final: str = "0.5"
    confidence: float = 0.5
    resolution: str = ""
    note: str = ""

    def __post_init__(self) -> None:
        if self.initial not in OBSERVATION_STATES:
            raise ValueError(
                f"TUF.initial must be one of {sorted(OBSERVATION_STATES)}, got {self.initial!r}"
            )
        if self.final not in OBSERVATION_STATES:
            raise ValueError(
                f"TUF.final must be one of {sorted(OBSERVATION_STATES)}, got {self.final!r}"
            )
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(
                f"TUF.confidence must be in [0.0, 1.0], got {self.confidence}"
            )

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


@dataclass
class FBD:
    """
    Failed boundary detection record.

    Fields:
      fbd_id          — unique identifier  (e.g. "FBD-001")
      tuf_id          — FK to source TUF
      first_deviation — description of the first detected deviation
      failure_point   — where in the process the failure occurred
      failure         — severity level: "Red" | "Yellow" | "Green" | "Blue"
      conditions      — formula / text describing boundary conditions
      impact          — impact assessment text
      line3_patch     — WHB patch string "IF ... THEN ..."
    """

    fbd_id: str
    tuf_id: str
    first_deviation: str = ""
    failure_point: str = ""
    failure: str = "Yellow"
    conditions: str = ""
    impact: str = ""
    line3_patch: str = ""

    def __post_init__(self) -> None:
        if self.failure not in FBD_FAILURE_LEVELS:
            raise ValueError(
                f"FBD.failure must be one of {sorted(FBD_FAILURE_LEVELS)}, got {self.failure!r}"
            )

    def to_dict(self) -> dict:
        return {
            "fbd_id": self.fbd_id,
            "tuf_id": self.tuf_id,
            "first_deviation": self.first_deviation,
            "failure_point": self.failure_point,
            "failure": self.failure,
            "conditions": self.conditions,
            "impact": self.impact,
            "line3_patch": self.line3_patch,
        }


@dataclass
class WHB:
    """
    Contextual law record (Line 3 — IF → THEN patch).

    Fields:
      law_id    — unique identifier  (e.g. "WHB-001")
      fbd_id    — FK to source FBD
      condition — "IF ..." clause referencing TUF state
      action    — "THEN ..." clause
    """

    law_id: str
    fbd_id: str
    condition: str = ""
    action: str = ""

    def to_dict(self) -> dict:
        return {
            "law_id": self.law_id,
            "fbd_id": self.fbd_id,
            "condition": self.condition,
            "action": self.action,
        }


@dataclass
class PRX:
    """
    Perception output (derived / visual signaling — not a decision node).

    Fields:
      prx_id    — unique identifier  (e.g. "PRX-001")
      tuf_id    — FK to source TUF
      symbol    — "▲" | "●" | "■" | "◆"
      color     — "RED" | "YELLOW" | "GREEN" | "BLUE"
      intensity — abs(confidence - 0.5) * scale  (computed on creation)
      scale     — multiplier used in intensity formula  (default: 2.0)
    """

    prx_id: str
    tuf_id: str
    symbol: str = "●"
    color: str = "YELLOW"
    intensity: float = 0.0
    scale: float = 2.0

    def __post_init__(self) -> None:
        if self.symbol not in PRX_SYMBOLS:
            raise ValueError(
                f"PRX.symbol must be one of {sorted(PRX_SYMBOLS)}, got {self.symbol!r}"
            )
        if self.color not in PRX_COLORS:
            raise ValueError(
                f"PRX.color must be one of {sorted(PRX_COLORS)}, got {self.color!r}"
            )

    @classmethod
    def from_tuf(cls, prx_id: str, tuf: "TUF", scale: float = 2.0) -> "PRX":
        """
        Derive a PRX record from a TUF record.

        Mapping (per W3memoriea spec):
          confidence == 1.0  → ▲ RED    (FORCE / SYSTEM)
          confidence == 0.5  → ● YELLOW (UNCERTAIN / HUMAN)
          confidence == 0.0  → ■ GREEN  (STABLE / RESULT)
          else               → ◆ BLUE   (EXTERNAL — default for in-between)

        Intensity = abs(confidence - 0.5) * scale
        """
        c = tuf.confidence
        if c == 1.0:
            symbol, color = "▲", "RED"
        elif c == 0.0:
            symbol, color = "■", "GREEN"
        elif c == 0.5:
            symbol, color = "●", "YELLOW"
        else:
            symbol, color = "◆", "BLUE"

        intensity = abs(c - 0.5) * scale
        return cls(
            prx_id=prx_id,
            tuf_id=tuf.tuf_id,
            symbol=symbol,
            color=color,
            intensity=round(intensity, 6),
            scale=scale,
        )

    def to_dict(self) -> dict:
        return {
            "prx_id": self.prx_id,
            "tuf_id": self.tuf_id,
            "symbol": self.symbol,
            "color": self.color,
            "intensity": self.intensity,
            "scale": self.scale,
        }
