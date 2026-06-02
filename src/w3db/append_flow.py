"""W3DB append-only observation flow.

This module provides a small production-oriented append contract for cross-system
signals. It does not replace the existing XIZ/TUF/FBD/WHB/PRX relation flow; it
wraps it with deterministic IDs, idempotency, and source references so W3Lgu,
PX, W3-API, EP_SIGNAL, and observers can share one append shape.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping

from src.w3db.config import W3DBConfig
from src.w3db.flow import run_flow
from src.w3db.store import W3DBStore, get_store


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _canonical_payload(value: Mapping[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _stable_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest().upper()


def _safe_token(value: str, *, fallback: str = "OBS") -> str:
    clean = "".join(ch for ch in value.upper() if ch.isalnum())
    return (clean or fallback)[:12]


@dataclass(frozen=True)
class AppendEnvelope:
    """Immutable cross-system append request.

    The envelope is perception/trace input only. It carries enough metadata to
    append an observation without giving the caller authority to rewrite history
    or decide execution.
    """

    append_id: str
    kind: str
    source: str
    subject: str
    payload: Mapping[str, Any]
    confidence: float = 0.5
    target: str = "W3DB"
    timestamp: str = field(default_factory=_now_iso)
    references: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.append_id.strip():
            raise ValueError("append_id is required")
        if not self.kind.strip():
            raise ValueError("kind is required")
        if not self.source.strip():
            raise ValueError("source is required")
        if not self.subject.strip():
            raise ValueError("subject is required")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be in [0.0, 1.0]")

    @property
    def suffix(self) -> str:
        return _safe_token(self.append_id[-12:], fallback="APPEND")

    def to_dict(self) -> dict[str, Any]:
        return {
            "append_id": self.append_id,
            "kind": self.kind,
            "source": self.source,
            "target": self.target,
            "subject": self.subject,
            "payload": dict(self.payload),
            "confidence": self.confidence,
            "timestamp": self.timestamp,
            "references": list(self.references),
        }


@dataclass(frozen=True)
class AppendFlowResult:
    """Trace IDs returned by an append-only W3DB write or idempotent replay."""

    append_id: str
    status: str
    appended: bool
    xiz_id: str
    tuf_id: str
    fbd_id: str
    whb_id: str
    prx_id: str
    output: Mapping[str, Any]
    references: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "append_id": self.append_id,
            "status": self.status,
            "appended": self.appended,
            "xiz_id": self.xiz_id,
            "tuf_id": self.tuf_id,
            "fbd_id": self.fbd_id,
            "whb_id": self.whb_id,
            "prx_id": self.prx_id,
            "output": dict(self.output),
            "references": list(self.references),
        }


def build_append_envelope(
    *,
    kind: str,
    source: str,
    subject: str,
    payload: Mapping[str, Any],
    confidence: float = 0.5,
    target: str = "W3DB",
    references: tuple[str, ...] = (),
    timestamp: str | None = None,
) -> AppendEnvelope:
    """Create a deterministic append envelope from cross-system metadata."""

    canonical = _canonical_payload(
        {
            "kind": kind,
            "source": source,
            "target": target,
            "subject": subject,
            "payload": dict(payload),
            "references": list(references),
        }
    )
    append_id = f"APP-{_safe_token(kind, fallback='OBS')}-{_stable_hash(canonical)[:16]}"
    return AppendEnvelope(
        append_id=append_id,
        kind=kind,
        source=source,
        subject=subject,
        payload=dict(payload),
        confidence=confidence,
        target=target,
        timestamp=timestamp or _now_iso(),
        references=tuple(sorted(references)),
    )


def append_envelope_to_w3db(
    envelope: AppendEnvelope,
    *,
    store: W3DBStore | None = None,
    cix_id: str | None = None,
    idempotent: bool = True,
) -> AppendFlowResult:
    """Append an envelope to W3DB through XIZ/TUF/FBD/WHB/PRX.

    Existing records are never updated. When ``idempotent`` is true and the XIZ
    record already exists, the function returns the existing trace IDs instead
    of raising or writing duplicates.
    """

    s = store or get_store()
    prefix = _safe_token(envelope.kind, fallback="OBS")
    suffix = envelope.suffix
    xiz_id = f"XIZ-{prefix}-{suffix}"
    tuf_id = f"TUF-{prefix}-{suffix}"
    fbd_id = f"FBD-{prefix}-{suffix}"
    whb_id = f"WHB-{prefix}-{suffix}"
    prx_id = f"PRX-{prefix}-{suffix}"

    if idempotent and s.read_xiz(xiz_id) is not None:
        prx = s.read_prx(prx_id)
        return AppendFlowResult(
            append_id=envelope.append_id,
            status="already_appended",
            appended=False,
            xiz_id=xiz_id,
            tuf_id=tuf_id,
            fbd_id=fbd_id,
            whb_id=whb_id,
            prx_id=prx_id,
            output={"prx": prx.to_dict() if prx else {}, "idempotent": True},
            references=envelope.references,
        )

    flow = run_flow(
        input_event=(
            f"Append {envelope.kind}:{envelope.append_id} "
            f"source={envelope.source} subject={envelope.subject}"
        ),
        cix_id=cix_id or envelope.source,
        confidence=envelope.confidence,
        xiz_id=xiz_id,
        tuf_id=tuf_id,
        fbd_id=fbd_id,
        whb_id=whb_id,
        prx_id=prx_id,
        store=s,
        config=W3DBConfig(env="append", immutable_xiz=True),
    )
    return AppendFlowResult(
        append_id=envelope.append_id,
        status="appended",
        appended=True,
        xiz_id=flow["xiz"].xiz_id,
        tuf_id=flow["tuf"].tuf_id,
        fbd_id=flow["fbd"].fbd_id,
        whb_id=flow["whb"].law_id,
        prx_id=flow["prx"].prx_id,
        output=flow["output"],
        references=envelope.references,
    )
