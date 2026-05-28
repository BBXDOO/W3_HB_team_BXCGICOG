# ==========================================
# Hospitication — Core Type Contracts
# Data structures only — no logic
# ==========================================

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

# ── Hard limits ────────────────────────────────────────────────
GRID_SIZE        = 16        # 16x16 = 256 nodes max
MAX_SIGNAL_DEPTH = 5

# ── Node states ────────────────────────────────────────────────
NodeState = Literal["active", "dormant", "shadow"]

# ── Pressure grades (emitter) ──────────────────────────────────
PressureGrade = Literal[
    "informational_drift",
    "caution_pressure",
    "structural_instability",
    "critical_collapse_risk",
]

# ── Signal retention ───────────────────────────────────────────
RetentionPolicy = Literal["critical", "standard", "decay", "compress"]
PersistenceScope = Literal["permanent", "session", "ephemeral"]

# ── Detector types ─────────────────────────────────────────────
DetectorType = Literal["oscillation", "divergence", "spike", "drift"]


# ── NodeRef ────────────────────────────────────────────────────

@dataclass(frozen=True)
class NodeRef:
    """
    Reference to a node in the 16x16 grid.
    Signal locality — every signal anchors to a node.
    Immutable by design.
    """
    x: int   # 0-15
    y: int   # 0-15

    def __post_init__(self):
        assert 0 <= self.x < GRID_SIZE
        assert 0 <= self.y < GRID_SIZE


# ── SignalEnvelope ─────────────────────────────────────────────

@dataclass(frozen=True)
class SignalEnvelope:
    """
    Immutable signal event.
    Once emitted — cannot be rewritten.
    Reinterpretation creates a new derived signal, not a mutation.

    signal ≠ logging
    signal = structural nervous response
    """
    signal_id:    str
    timestamp:    float
    origin_node:  NodeRef

    detector_type: DetectorType
    pressure:      PressureGrade

    # Retention
    retention:     RetentionPolicy  = "standard"
    persistence:   PersistenceScope = "session"

    # Lineage — link to parent signal if derived
    parent_id:    str | None = None
    is_derived:   bool       = False

    def to_shadow(self) -> dict:
        """Minimal lineage — always retained even after decay."""
        return {
            "signal_id":  self.signal_id,
            "timestamp":  self.timestamp,
            "origin_node": (self.origin_node.x, self.origin_node.y),
            "retention":  self.retention,
        }


# ── DetectorResult ─────────────────────────────────────────────

@dataclass
class DetectorResult:
    """
    What the detector found — NOT a diagnosis.

    "detected" ≠ "root cause known"
    System can detect before it understands.
    """
    detector_type: DetectorType
    detected:      bool
    confidence:    float        # 0.0 - 1.0
    locality:      NodeRef
    evidence:      dict         # raw observation data, no interpretation

    # Explicitly not included:
    # - cause
    # - recommendation
    # - recovery path
    # Those belong to evaluation and recovery layers.

