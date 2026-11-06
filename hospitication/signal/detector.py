"""Pattern detectors for Hospitication signals.

Single-snapshot thresholds produce drift/spike and cross-metric divergence.
They do not establish temporal drift or oscillation, diagnose, or mutate truth.
"""

from __future__ import annotations

from hospitication.core.types import DetectorResult, MetricScore, NodeRef


def detect_signals(metrics: tuple[MetricScore, ...]) -> tuple[DetectorResult, ...]:
    ordered = tuple(sorted(metrics, key=lambda item: item.name))
    results: list[DetectorResult] = []
    scores = [metric.score for metric in ordered]

    for index, metric in enumerate(ordered):
        node = NodeRef(index % 16, index // 16)
        if metric.score >= 0.65:
            results.append(
                DetectorResult(
                    detector_type="spike",
                    detected=True,
                    confidence=round(metric.score, 4),
                    locality=node,
                    evidence={"metric": metric.name, "score": metric.score},
                )
            )
        elif metric.score >= 0.2:
            results.append(
                DetectorResult(
                    detector_type="drift",
                    detected=True,
                    confidence=round(metric.score, 4),
                    locality=node,
                    evidence={"metric": metric.name, "score": metric.score},
                )
            )

    if scores:
        spread = max(scores) - min(scores)
        if spread >= 0.45:
            results.append(
                DetectorResult(
                    detector_type="divergence",
                    detected=True,
                    confidence=round(spread, 4),
                    locality=NodeRef(15, 15),
                    evidence={"score_spread": round(spread, 4)},
                )
            )

    return tuple(results)
