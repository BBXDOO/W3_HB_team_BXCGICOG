from __future__ import annotations

from hashlib import sha1
import json
from typing import Any, Dict, Mapping

from .contracts import ACTIVE, WAIT, make_result, normalize_text


def _as_payload(record: Any) -> Dict[str, Any]:
    if isinstance(record, Mapping):
        return dict(record)
    return {"text": normalize_text(record)}


def _stable_key(payload: Dict[str, Any]) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)
    return sha1(raw.encode("utf-8")).hexdigest()[:16]


def checkpoint_lifecycle(record: Any) -> object:
    """Create a lifecycle checkpoint preview for W3Lgu module flow.

    LRC2 already has richer runtime behavior. This function only gives the MFC
    layer a shared contract-shaped checkpoint result.
    """

    payload = _as_payload(record)
    text = normalize_text(payload)

    if not text:
        return make_result(
            module="LRC2",
            status=WAIT,
            confidence=0.0,
            input_type="empty",
            decision="wait_for_record",
            reason="no record was provided for checkpoint preview",
            next_modules=[],
            standby=["REDR", "PSP2", "DTML"],
            details={"payload": payload},
        )

    checkpoint_key = f"LRC2-{_stable_key(payload)}"
    return make_result(
        module="LRC2",
        status=ACTIVE,
        confidence=0.8,
        input_type="record:checkpoint_preview",
        decision="checkpoint_preview_ready",
        reason="record can be represented as a lifecycle checkpoint preview",
        next_modules=[],
        standby=["REDR", "PSP2", "DTML"],
        details={
            "checkpoint_key": checkpoint_key,
            "record_length": len(text),
            "payload": payload,
        },
    )
