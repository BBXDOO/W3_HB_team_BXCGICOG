from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional


ACTIVE = "ACTIVE"
STANDBY = "STANDBY"
WAIT = "WAIT"
STOP = "STOP"
REVIEW_REQUIRED = "REVIEW_REQUIRED"
ERROR = "ERROR"

VALID_STATUSES = {ACTIVE, STANDBY, WAIT, STOP, REVIEW_REQUIRED, ERROR}


@dataclass(frozen=True)
class W3LguLogicResult:
    """Shared return contract for the first W3Lgu MFC logic layer.

    This object is intentionally small and side-effect free. It can be used by
    unit tests, agent wrappers, W3-API adapters, or future E-CS routing without
    requiring runtime mutation.
    """

    module: str
    status: str
    confidence: float
    input_type: str
    decision: str
    reason: str
    next: List[str] = field(default_factory=list)
    standby: List[str] = field(default_factory=list)
    mutated: bool = False
    traceable: bool = True
    details: Dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "module": self.module,
            "status": self.status,
            "confidence": self.confidence,
            "input_type": self.input_type,
            "decision": self.decision,
            "reason": self.reason,
            "next": list(self.next),
            "standby": list(self.standby),
            "mutated": self.mutated,
            "traceable": self.traceable,
            "details": dict(self.details),
        }

    def as_signal_line(self) -> str:
        next_text = ",".join(self.next) if self.next else "-"
        standby_text = ",".join(self.standby) if self.standby else "-"
        return (
            f"module={self.module} status={self.status} "
            f"confidence={self.confidence} input_type={self.input_type} "
            f"decision={self.decision} next={next_text} standby={standby_text} "
            f"mutated={self.mutated} traceable={self.traceable} reason={self.reason}"
        )


def clamp_confidence(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.5
    return max(0.0, min(1.0, number))


def normalize_status(status: str) -> str:
    normalized = str(status or WAIT).upper()
    if normalized not in VALID_STATUSES:
        return ERROR
    return normalized


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, Mapping):
        items = []
        for key, item in value.items():
            items.append(f"{key}={item}")
        return " ".join(items).strip()
    if isinstance(value, Iterable) and not isinstance(value, (bytes, bytearray)):
        return " ".join(str(item) for item in value).strip()
    return str(value).strip()


def make_result(
    *,
    module: str,
    status: str,
    confidence: Any,
    input_type: str,
    decision: str,
    reason: str,
    next_modules: Optional[Iterable[str]] = None,
    standby: Optional[Iterable[str]] = None,
    mutated: bool = False,
    traceable: bool = True,
    details: Optional[Dict[str, Any]] = None,
) -> W3LguLogicResult:
    return W3LguLogicResult(
        module=str(module),
        status=normalize_status(status),
        confidence=clamp_confidence(confidence),
        input_type=str(input_type or "unknown"),
        decision=str(decision or "none"),
        reason=str(reason or "no reason provided"),
        next=list(next_modules or []),
        standby=list(standby or []),
        mutated=bool(mutated),
        traceable=bool(traceable),
        details=dict(details or {}),
    )
