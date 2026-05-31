# ==========================================
# IGET v8.0 — Proof Tracer
# Semantic annotation + causal proof engine
# Ontology tag: iget:module = "proof"
# ==========================================

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from .config import PROOF_MAX_ENTRIES, PROOF_TRACE_ENABLED


@dataclass
class ProofEntry:
    """
    A single causal proof entry.
    Ontology tag: iget:proof_entry
    """
    step: str           # e.g. "classify_files", "compute_score"
    claim: str          # what was decided / observed
    evidence: Any       # raw data that supports the claim
    semantic_tag: str   # ontology tag for this event
    timestamp: float    = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            "step":         self.step,
            "claim":        self.claim,
            "evidence":     self.evidence,
            "semantic_tag": self.semantic_tag,
            "timestamp":    self.timestamp,
        }


class ProofTracer:
    """
    Lightweight causal proof + semantic annotation collector.

    Usage:
        tracer = ProofTracer()
        tracer.record("classify", "found 3 risky files", {...}, "iget:risk")
        tracer.to_mpcp_result()

    Ontology tag: iget:proof_tracer
    MPCP role: governance_assistant
    """

    def __init__(self, enabled: bool = PROOF_TRACE_ENABLED):
        self.enabled   = enabled
        self._entries: list[ProofEntry] = []
        self._start    = time.time()

    def record(
        self,
        step: str,
        claim: str,
        evidence: Any = None,
        semantic_tag: str = "iget:event",
    ) -> None:
        """Append a proof entry (no-op when disabled)."""
        if not self.enabled:
            return
        if len(self._entries) >= PROOF_MAX_ENTRIES:
            return  # silent cap — avoid memory blow-up
        self._entries.append(ProofEntry(step, claim, evidence, semantic_tag))

    def entries(self) -> list[ProofEntry]:
        return list(self._entries)

    def elapsed(self) -> float:
        return round(time.time() - self._start, 4)

    def to_mpcp_result(self) -> dict:
        """
        Produce an MPCP-compatible result/trace payload.
        Ontology tag: iget:mpcp_result
        """
        return {
            "mpcp_role":    "governance_assistant",
            "mpcp_version": "1.0",
            "elapsed_sec":  self.elapsed(),
            "trace":        [e.to_dict() for e in self._entries],
        }

    def summary(self) -> str:
        """Human-readable one-line summary of recorded steps."""
        steps = [e.step for e in self._entries]
        return " → ".join(steps) if steps else "(no trace)"

