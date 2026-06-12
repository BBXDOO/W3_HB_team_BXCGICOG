# ==========================================
# IGET v8.0 — Causal Layer (foundation)
# Data structures only — no logic
# Ontology tag: iget:module = "causal"
# ==========================================

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Literal

# ── Hard limits (entropy control) ─────────────────────────────
MAX_REPLAY_DEPTH       = 5
MAX_CAUSAL_FANOUT      = 10
MAX_SEMANTIC_EXPANSION = 3

# ── Edge types ─────────────────────────────────────────────────
EdgeType = Literal[
    "triggers",
    "escalates",
    "mitigates",
    "invalidates",
    "recovers",
]

# ── Severity ───────────────────────────────────────────────────
Severity = Literal["critical", "caution", "info"]

# ── ReplayScope (frozen) ───────────────────────────────────────
ReplayScope = Literal["full", "boundary_only", "critical_only"]

# ── BoundaryComparison ─────────────────────────────────────────
BoundaryComparison = Literal["lt", "gt", "eq"]


# ── BoundarySnapshot ──────────────────────────────────────────

@dataclass
class BoundarySnapshot:
    """
    State of the boundary at the moment it was crossed.

    Preserves historical truth for replay.
    Must NOT be updated after creation.

    Ontology tag: iget:boundary_snapshot
    """
    threshold:  float              # rule value at that time
    observed:   float              # actual measured value
    delta:      float              # observed - threshold
    policy:     str                # policy name that applied
    comparison: BoundaryComparison = "lt"  # how boundary is evaluated

    def was_crossed(self) -> bool:
        """True if observed value violated the boundary."""
        if self.comparison == "lt":
            return self.observed < self.threshold
        if self.comparison == "gt":
            return self.observed > self.threshold
        if self.comparison == "eq":
            return self.observed != self.threshold
        return False


# ── CausalNode ────────────────────────────────────────────────

@dataclass
class CausalNode:
    """
    A single node in the causal graph.

    Represents one point where the system changed behavior —
    not every event, only outcome-affecting ones.

    Ontology tag: iget:causal_node

    # TODO (technical debt): trigger/evaluation/outcome are unbounded
    # dicts — risk of recursive payload and serialization drift.
    # Consider typed contracts in v8.1.
    """
    node_id:       str
    parent_id:     str | None
    timestamp:     float           # mandatory — replay truth anchor

    event_type:    str             # "boundary_cross" | "score_delta" | "risk_found"
    semantic_tag:  str             # "iget:boundary" | "iget:risk" | ...
    severity:      Severity

    trigger:       dict            # what caused this node
    evaluation:    dict            # what was measured
    boundary:      BoundarySnapshot | None  # snapshot if boundary crossed
    outcome:       dict            # what changed as result

    recovery_path: list[str]       = field(default_factory=list)

    # ── Retention control ──────────────────────────────────────
    retained:      bool            = True
    replay_scope:  ReplayScope     = "full"

    def to_shadow(self) -> dict:
        """
        Minimal lineage — preserved even when pruned.
        node_id + parent_id + timestamp = mandatory replay truth.
        Ensures replay chain never breaks.
        """
        return {
            "node_id":   self.node_id,
            "parent_id": self.parent_id,
            "timestamp": self.timestamp,
            "retained":  self.retained,
        }

    def to_dict(self) -> dict:
        """Full representation for active nodes."""
        return {
            "node_id":       self.node_id,
            "parent_id":     self.parent_id,
            "timestamp":     self.timestamp,
            "event_type":    self.event_type,
            "semantic_tag":  self.semantic_tag,
            "severity":      self.severity,
            "trigger":       self.trigger,
            "evaluation":    self.evaluation,
            "boundary":      vars(self.boundary) if self.boundary else None,
            "outcome":       self.outcome,
            "recovery_path": self.recovery_path,
            "retained":      self.retained,
            "replay_scope":  self.replay_scope,
        }


# ── CausalEdge ────────────────────────────────────────────────

@dataclass
class CausalEdge:
    """
    Directed relationship between two causal nodes.

    edge_type describes HOW one node relates to another,
    not just that a relation exists.

    Ontology tag: iget:causal_edge

    # ROADMAP v8.1: add timestamp to edge — edge relations
    # may change over time (invalidate, recover after the fact).
    """
    from_id:     str
    to_id:       str
    edge_type:   EdgeType
    edge_weight: float = 1.0  # 0.0-1.0: how much this edge changed outcome
