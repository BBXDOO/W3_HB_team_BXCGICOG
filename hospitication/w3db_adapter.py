"""Hospitication → W3DB adapter.

Adapters append signal observations to W3DB. They do not modify the source
HealthReport, SignalEnvelope, or W3DB records created earlier.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from hospitication.core.types import HealthReport, SignalEnvelope
from src.w3db.flow import run_flow
from src.w3db.store import W3DBStore


@dataclass(frozen=True)
class HospiticationW3DBResult:
    signal_id: str
    xiz_id: str
    tuf_id: str
    fbd_id: str
    prx_id: str
    output: dict[str, Any]


def store_hospitication_signal_to_w3db(
    signal: SignalEnvelope,
    *,
    store: W3DBStore | None = None,
    cix_id: str = "HOSPITICATION",
) -> HospiticationW3DBResult:
    """Append one Hospitication signal to W3DB as a derived observation."""

    prefix = _id_suffix(signal.signal_id)
    flow = run_flow(
        input_event=(
            f"Hospitication signal:{signal.signal_id} "
            f"type={signal.detector_type} pressure={signal.pressure}"
        ),
        cix_id=cix_id,
        confidence=signal.confidence,
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


def _id_suffix(signal_id: str) -> str:
    clean = "".join(ch for ch in signal_id.upper() if ch.isalnum())
    return (clean[-8:] or "SIGNAL00")[:8]
