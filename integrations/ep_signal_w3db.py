"""EP_SIGNAL → W3DB adapter.

The adapter records a decoded EP_SIGNAL as a new W3DB flow. It does not mutate
EP_SIGNAL payloads or historical W3DB records; it only appends XIZ/TUF/FBD/WHB/PRX
records through the existing W3DB flow API.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any

from protocol.EP_SIGNAL.reference_implementation import decode, validate
from src.w3db.flow import run_flow
from src.w3db.store import W3DBStore


@dataclass(frozen=True)
class EPSignalW3DBResult:
    """Stable adapter result for traceable EP_SIGNAL storage."""

    signal_hash: str
    binary_length: int
    ones_count: int
    xiz_id: str
    tuf_id: str
    fbd_id: str
    prx_id: str
    output: dict[str, Any]


def store_ep_signal_to_w3db(
    ep_signal: str,
    *,
    store: W3DBStore | None = None,
    cix_id: str = "EP_SIGNAL",
) -> EPSignalW3DBResult:
    """Append an EP_SIGNAL observation to W3DB and return trace IDs.

    The confidence is derived from the decoded binary density. This is an
    observation signal only; callers must not treat PRX/FBD output as execution.
    """

    if not validate(ep_signal):
        raise ValueError("Invalid EP_SIGNAL payload")

    binary = decode(ep_signal)
    signal_hash = _stable_hash(ep_signal)
    ones_count = binary.count("1")
    confidence = ones_count / max(1, len(binary))
    flow = run_flow(
        input_event=f"EP_SIGNAL observed:{signal_hash}",
        cix_id=cix_id,
        confidence=confidence,
        xiz_id=f"XIZ-EP-{signal_hash[:8]}",
        tuf_id=f"TUF-EP-{signal_hash[:8]}",
        fbd_id=f"FBD-EP-{signal_hash[:8]}",
        whb_id=f"WHB-EP-{signal_hash[:8]}",
        prx_id=f"PRX-EP-{signal_hash[:8]}",
        store=store,
    )
    return EPSignalW3DBResult(
        signal_hash=signal_hash,
        binary_length=len(binary),
        ones_count=ones_count,
        xiz_id=flow["xiz"].xiz_id,
        tuf_id=flow["tuf"].tuf_id,
        fbd_id=flow["fbd"].fbd_id,
        prx_id=flow["prx"].prx_id,
        output=flow["output"],
    )


def _stable_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16].upper()
