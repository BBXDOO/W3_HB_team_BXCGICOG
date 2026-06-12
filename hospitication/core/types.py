# ==========================================
# Hospitication — Core Type Contracts
# Data structures only — no orchestration logic
# ==========================================

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Mapping

# ── Hard limits ────────────────────────────────────────────────
GRID_SIZE = 16  # 16x16 = 256 nodes max
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
AnalyzerName = Literal[
    "semantic_pressure",
    "dependency_fatigue",
    "replay_complexity",
    "recovery_resistance",
    "cognitive_cost",
]
ProposalStatus = Literal["proposed"]


@dataclass(frozen=True)
class NodeRef:
    """
    Reference to a node in the 16x16 grid.
    Signal locality — every signal anchors to a node.
    Immutable by design.
    """

    x: int  # 0-15
    y: int  # 0-15

    def __post_init__(self) -> None:
        if not 0 <= self.x < GRID_SIZE:
            raise ValueError(f"NodeRef.x must be in 0..{GRID_SIZE - 1}: {self.x}")
        if not 0 <= self.y < GRID_SIZE:
            raise ValueError(f"NodeRef.y must be in 0..{GRID_SIZE - 1}: {self.y}")


@dataclass(frozen=True)
class FileObservation:
    """Read-only structural observation for one repository file."""

    path: str
    suffix: str
    line_count: int
    byte_count: int
    imports: tuple[str, ...] = ()
    markers: tuple[str, ...] = ()


@dataclass(frozen=True)
class ObservationSnapshot:
    """Immutable repository snapshot used by analyzers and detectors."""

    repo_root: str
    files: tuple[FileObservation, ...]
    observed_at: str
    ignored_dirs: tuple[str, ...] = ()

    @property
    def total_lines(self) -> int:
        return sum(file.line_count for file in self.files)

    @property
    def total_bytes(self) -> int:
        return sum(file.byte_count for file in self.files)


@dataclass(frozen=True)
class MetricScore:
    """Analyzer output. A score is pressure evidence, not a recovery action."""

    name: AnalyzerName
    score: float
    summary: str
    evidence: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 1.0:
            raise ValueError(f"MetricScore.score must be 0.0..1.0: {self.score}")


@dataclass(frozen=True)
class DetectorResult:
    """
    What the detector found — NOT a diagnosis.

    "detected" is not "root cause known". Detection must not recommend recovery.
    """

    detector_type: DetectorType
    detected: bool
    confidence: float  # 0.0 - 1.0
    locality: NodeRef
    evidence: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(
                f"DetectorResult.confidence must be 0.0..1.0: {self.confidence}"
            )


@dataclass(frozen=True)
class SignalEnvelope:
    """
    Immutable signal event.
    Once emitted — cannot be rewritten.
    Reinterpretation creates a new derived signal, not a mutation.

    signal ≠ logging
    signal = structural nervous response
    """

    signal_id: str
    timestamp: str
    origin_node: NodeRef
    detector_type: DetectorType
    pressure: PressureGrade
    confidence: float
    evidence: Mapping[str, Any] = field(default_factory=dict)
    retention: RetentionPolicy = "standard"
    persistence: PersistenceScope = "session"
    parent_id: str | None = None
    is_derived: bool = False

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(
                f"SignalEnvelope.confidence must be 0.0..1.0: {self.confidence}"
            )

    def to_shadow(self) -> dict[str, Any]:
        """Minimal lineage — always retained even after decay."""
        return {
            "signal_id": self.signal_id,
            "timestamp": self.timestamp,
            "origin_node": (self.origin_node.x, self.origin_node.y),
            "retention": self.retention,
        }


@dataclass(frozen=True)
class RecoveryProposal:
    """Non-mutating recovery proposal. This is never an applied change."""

    proposal_id: str
    title: str
    rationale: str
    target_paths: tuple[str, ...] = ()
    actions: tuple[str, ...] = ()
    source_metrics: tuple[AnalyzerName, ...] = ()
    status: ProposalStatus = "proposed"
    destructive: bool = False


@dataclass(frozen=True)
class HealthReport:
    """Complete deterministic Hospitication report payload."""

    generated_at: str
    repo_root: str
    metrics: tuple[MetricScore, ...]
    signals: tuple[SignalEnvelope, ...]
    proposals: tuple[RecoveryProposal, ...]
    summary: str

    @property
    def overall_score(self) -> float:
        if not self.metrics:
            return 0.0
        return round(sum(metric.score for metric in self.metrics) / len(self.metrics), 4)
