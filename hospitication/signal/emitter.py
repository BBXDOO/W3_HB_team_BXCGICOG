"""Signal emitter. Emits immutable envelopes; does not interpret or recover."""

from __future__ import annotations

import hashlib

from hospitication.core.config import DEFAULT_TIMESTAMP, HospiticationConfig
from hospitication.core.types import DetectorResult, PressureGrade, SignalEnvelope


def pressure_for_confidence(confidence: float) -> PressureGrade:
    if confidence >= 0.85:
        return "critical_collapse_risk"
    if confidence >= 0.65:
        return "structural_instability"
    if confidence >= 0.35:
        return "caution_pressure"
    return "informational_drift"


def emit_signals(
    detections: tuple[DetectorResult, ...],
    config: HospiticationConfig | None = None,
) -> tuple[SignalEnvelope, ...]:
    cfg = config or HospiticationConfig()
    emitted: list[SignalEnvelope] = []
    for detection in sorted(
        detections,
        key=lambda item: (item.detector_type, item.locality.x, item.locality.y, repr(item.evidence)),
    ):
        if not detection.detected or detection.confidence < cfg.emit_threshold:
            continue
        signal_id = _stable_signal_id(detection, cfg.deterministic_timestamp)
        pressure = pressure_for_confidence(detection.confidence)
        emitted.append(
            SignalEnvelope(
                signal_id=signal_id,
                timestamp=cfg.deterministic_timestamp or DEFAULT_TIMESTAMP,
                origin_node=detection.locality,
                detector_type=detection.detector_type,
                pressure=pressure,
                confidence=detection.confidence,
                evidence=dict(sorted(detection.evidence.items())),
                retention="critical" if pressure == "critical_collapse_risk" else "standard",
                persistence="permanent" if pressure == "critical_collapse_risk" else "session",
            )
        )
    return tuple(emitted)


def _stable_signal_id(detection: DetectorResult, timestamp: str) -> str:
    seed = "|".join(
        [
            timestamp,
            detection.detector_type,
            str(detection.locality.x),
            str(detection.locality.y),
            f"{detection.confidence:.4f}",
            repr(sorted(detection.evidence.items())),
        ]
    )
    return "sig_" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]
