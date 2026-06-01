"""Pattern detectors for Hospitication signals.

Detectors only detect drift/spike/oscillation/divergence. They never diagnose,
recommend, or mutate truth.
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

    oscillation = _oscillation_score(scores)
    if oscillation >= 0.5:
        results.append(
            DetectorResult(
                detector_type="oscillation",
                detected=True,
                confidence=round(oscillation, 4),
                locality=NodeRef(14, 15),
                evidence={"direction_changes": oscillation},
            )
        )

    return tuple(results)


def _oscillation_score(scores: list[float]) -> float:
    if len(scores) < 3:
        return 0.0
    changes = 0
    previous_direction = 0
    for left, right in zip(scores, scores[1:]):
        direction = 1 if right > left else -1 if right < left else 0
        if direction and previous_direction and direction != previous_direction:
            changes += 1
        if direction:
            previous_direction = direction
    return min(1.0, changes / max(1, len(scores) - 2))
