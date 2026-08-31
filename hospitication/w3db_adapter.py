"""Hospitication → W3DB adapter.

Adapters append signal observations to W3DB. They do not modify the source
HealthReport, SignalEnvelope, or W3DB records created earlier.

Semantic boundary
-----------------
Hospitication confidence means confidence that structural pressure was
detected; a higher value therefore means stronger pressure. W3DB confidence
is an observation of process stability/truth strength; a higher value produces
a stronger/pass state. The adapter must translate between those opposite axes
instead of forwarding the number unchanged.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from hospitication.core.types import HealthReport, SignalEnvelope
from src.w3db.flow import run_flow
from src.w3db.store import W3DBStore


TRANSLATION_CONTRACT = "inverse_detection_to_stability_v1"


@dataclass(frozen=True)
class HospiticationW3DBResult:
    signal_id: str
    xiz_id: str
    tuf_id: str
    fbd_id: str
    prx_id: str
    source_detection_confidence: float
    translated_stability_confidence: float
    translation_contract: str
    output: dict[str, Any]


def store_hospitication_signal_to_w3db(
    signal: SignalEnvelope,
    *,
    store: W3DBStore | None = None,
    cix_id: str = "HOSPITICATION",
) -> HospiticationW3DBResult:
    """Append one Hospitication signal to W3DB as a derived observation."""

    prefix = _id_suffix(signal.signal_id)
    stability_confidence = _translate_detection_to_stability_confidence(signal.confidence)
    flow = run_flow(
        input_event=(
            f"Hospitication signal:{signal.signal_id} "
            f"type={signal.detector_type} pressure={signal.pressure} "
            f"detection_confidence={signal.confidence} "
            f"translation={TRANSLATION_CONTRACT}"
        ),
        cix_id=cix_id,
        confidence=stability_confidence,
        xiz_id=f"XIZ-HOSP-{prefix}",
        tuf_id=f"TUF-HOSP-{prefix}",
        fbd_id=f"FBD-HOSP-{prefix}",
        whb_id=f"WHB-HOSP-{prefix}",
        prx_id=f"PRX-HOSP-{prefix}",
        store=store,
    )
    return HospiticationW3DBResult(
        signal_id=signal.signal_id,
        xiz_id=flow["xiz"].xiz_id,
        tuf_id=flow["tuf"].tuf_id,
        fbd_id=flow["fbd"].fbd_id,
        prx_id=flow["prx"].prx_id,
        source_detection_confidence=signal.confidence,
        translated_stability_confidence=stability_confidence,
        translation_contract=TRANSLATION_CONTRACT,
        output=flow["output"],
    )


def store_hospitication_report_to_w3db(
    report: HealthReport,
    *,
    store: W3DBStore | None = None,
    cix_id: str = "HOSPITICATION",
) -> tuple[HospiticationW3DBResult, ...]:
    """Append all emitted signals from a HealthReport to W3DB."""

    return tuple(
        store_hospitication_signal_to_w3db(signal, store=store, cix_id=cix_id)
        for signal in sorted(report.signals, key=lambda item: item.signal_id)
    )


def _translate_detection_to_stability_confidence(detection_confidence: float) -> float:
    """Translate pressure-detection confidence to W3DB stability confidence."""

    return round(1.0 - detection_confidence, 4)


def _id_suffix(signal_id: str) -> str:
    clean = "".join(ch for ch in signal_id.upper() if ch.isalnum())
    return (clean[-8:] or "SIGNAL00")[:8]
