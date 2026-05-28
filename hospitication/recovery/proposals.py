"""Recovery proposal layer. It only proposes; it never applies changes."""

from __future__ import annotations

import hashlib

from hospitication.core.types import AnalyzerName, MetricScore, RecoveryProposal, SignalEnvelope
from hospitication.recovery.mitigations import MITIGATIONS


def propose_recovery(
    metrics: tuple[MetricScore, ...],
    signals: tuple[SignalEnvelope, ...] = (),
) -> tuple[RecoveryProposal, ...]:
    proposals: list[RecoveryProposal] = []
    pressure_metrics = tuple(sorted((m for m in metrics if m.score >= 0.35), key=lambda item: item.name))
    for metric in pressure_metrics:
        actions = MITIGATIONS.get(metric.name, ("Review this pressure metric before recovery.",))
        target_paths = _target_paths(metric)
        proposals.append(
            RecoveryProposal(
                proposal_id=_proposal_id(metric.name, metric.score, target_paths),
                title=f"Mitigate {metric.name.replace('_', ' ')}",
                rationale=f"Metric score {metric.score:.4f}: {metric.summary}",
                target_paths=target_paths,
                actions=tuple(actions),
                source_metrics=(metric.name,),
                destructive=False,
            )
        )

    if signals and len(signals) >= 4:
        proposals.append(
            RecoveryProposal(
                proposal_id=_proposal_id("signal_review", float(len(signals)), ()),
                title="Review clustered signal pressure",
                rationale=f"{len(signals)} emitted signals indicate structural pressure clustering.",
                actions=(
                    "Review signal evidence in descending confidence order.",
                    "Attach recovery notes as new annotations, not mutations of emitted truth.",
                ),
                source_metrics=tuple(metric.name for metric in pressure_metrics),
                destructive=False,
            )
        )
    return tuple(proposals)


def _target_paths(metric: MetricScore) -> tuple[str, ...]:
    evidence = metric.evidence
    for key in ("large_files", "replay_related_files"):
        values = evidence.get(key)
        if isinstance(values, tuple):
            return tuple(str(value) for value in values[:5])
        if isinstance(values, list):
            return tuple(str(value) for value in values[:5])
    return ()


def _proposal_id(name: AnalyzerName | str, score: float, paths: tuple[str, ...]) -> str:
    seed = f"{name}|{score:.4f}|{repr(paths)}"
    return "prop_" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]
