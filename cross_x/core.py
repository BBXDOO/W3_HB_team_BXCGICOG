"""Cross-X ecosystem coordination.

Cross-X is not a bug finder. It pulls the relevant W3 systems to the cross point
and builds a traceable improvement plan: W3-API intent → W3Lgu packet → PX anchor
→ W3DB append envelope → EP_SIGNAL preview. The default behavior is plan-only
and non-mutating.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping
from uuid import uuid4

from config.loader import W3ConfigBundle, load_w3_config
from protocol.EP_SIGNAL.ep_signal_adapter import to_ep_signal
from core.runtime.process_layer import run_w3_process_layer
from protocol.EP_SIGNAL.rytm import build_rytm_preview
from protocol.w3lgu import W3LguFiveLineProgram, encode_w3lgu_value, parse_five_line_program, px_from_five_line, px_to_append_envelope, validate_five_line
from protocol.w3lgu.px import PXAnchor
from src.w3db.append_flow import AppendEnvelope
from cross_x.event_chain import EventChain, build_event_chain, normalize_ecs_identifier
from cross_x.audit import audit_cross_systems


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _build_cross_w3lgu_packet(
    *,
    chain_id: str,
    source: str,
    intent: str,
    target: str | None,
    mode: str,
    payload: Mapping[str, Any],
) -> W3LguFiveLineProgram:
    target_value = target or "auto"
    contract = str(payload.get("contract", "observe_only"))
    text = "\n".join(
        (
            f"MEM:SOURCE:{encode_w3lgu_value(source)},CHAIN_ID:{chain_id}",
            f"PATCH:MODE:{encode_w3lgu_value(mode)}",
            f"LAW:TARGET:{encode_w3lgu_value(target_value)},CONTRACT:{encode_w3lgu_value(contract)}",
            f"EVENT:INTENT:{encode_w3lgu_value(intent)},ECS_STATE:planned",
            "SIGNAL:STATUS:received,TRACEABLE:true,EXECUTE_ALLOWED:false",
        )
    )
    program = parse_five_line_program(text)
    result = validate_five_line(program)
    if not result.ok:
        raise ValueError(f"Invalid W3Lgu cross packet: {result.errors}")
    return program


def _build_ep_signal_preview(w3lgu_text: str) -> dict[str, object]:
    digest_bits = "".join(f"{byte:08b}" for byte in w3lgu_text.encode("utf-8")[:8])
    binary = digest_bits or "0"
    return {
        "mode": "preview_only",
        "mutated": False,
        "format": "BIN",
        "ep_signal": to_ep_signal(binary),
        "rytm": build_rytm_preview(binary, meta=("CROSS_X", "EP_SIGNAL")),
    }


@dataclass(frozen=True)
class CrossXRequest:
    """Immutable request to coordinate systems at the Cross-X point."""

    source: str
    intent: str
    target: str | None = None
    mode: str = "observe"
    payload: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "intent": self.intent,
            "target": self.target,
            "mode": self.mode,
            "payload": dict(self.payload),
        }


@dataclass(frozen=True)
class CrossXPlan:
    """Plan-only Cross-X result.

    The plan contains trace artifacts and append intent. It does not persist to
    W3DB, mutate EP_SIGNAL, execute MPCP, or approve truth.
    """

    cross_id: str
    timestamp: str
    request: CrossXRequest
    chain: tuple[str, ...]
    event_chain: EventChain
    program: W3LguFiveLineProgram
    px: PXAnchor
    append_envelope: AppendEnvelope
    ep_signal: Mapping[str, Any]
    process_trace: Mapping[str, Any] = field(default_factory=dict)
    system_audit: Mapping[str, Any] = field(default_factory=dict)
    status: str = "planned"
    mutated: bool = False
    governance: Mapping[str, bool] = field(
        default_factory=lambda: {
            "human_review_required": True,
            "governance_gate_required": True,
            "truth_mutation_allowed": False,
            "execute_allowed": False,
        }
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "cross_id": self.cross_id,
            "timestamp": self.timestamp,
            "status": self.status,
            "mutated": self.mutated,
            "request": self.request.to_dict(),
            "chain": list(self.chain),
            "event_chain": self.event_chain.to_dict(),
            "w3lgu": self.program.to_text(),
            "px": self.px.to_dict(),
            "append_envelope": self.append_envelope.to_dict(),
            "ep_signal": dict(self.ep_signal),
            "process_trace": dict(self.process_trace),
            "system_audit": dict(self.system_audit),
            "governance": dict(self.governance),
        }


def build_cross_x_plan(
    request: CrossXRequest | None = None,
    *,
    source: str | None = None,
    intent: str | None = None,
    target: str | None = None,
    mode: str | None = None,
    payload: Mapping[str, Any] | None = None,
    config: W3ConfigBundle | None = None,
    cross_id: str | None = None,
    timestamp: str | None = None,
) -> CrossXPlan:
    """Build a non-mutating Cross-X coordination plan."""

    cfg = config or load_w3_config()
    cross_x = cfg.cross_system["cross_x"]
    resolved_request = request or CrossXRequest(
        source=source or "unknown",
        intent=intent or "observe",
        target=target,
        mode=mode or str(cross_x["default_mode"]),
        payload=dict(payload or {}),
    )
    allowed_modes = set(cross_x.get("allowed_modes", ()))
    if resolved_request.mode not in allowed_modes:
        raise ValueError(f"Cross-X mode {resolved_request.mode!r} is not allowed")

    resolved_cross_id = normalize_ecs_identifier(
        str(uuid4()) if cross_id is None else cross_id,
        field="chain_id",
    )
    program = _build_cross_w3lgu_packet(
        chain_id=resolved_cross_id,
        source=resolved_request.source,
        intent=resolved_request.intent,
        target=resolved_request.target,
        mode=resolved_request.mode,
        payload=dict(resolved_request.payload),
    )
    px = px_from_five_line(
        program,
        relation="cross_x.workflow_improvement",
        mode=resolved_request.mode,
        extra_payload={
            "cross_id": resolved_cross_id,
            "purpose": cross_x["purpose"],
            "truth_mutation": cross_x["truth_mutation"],
        },
    )
    append_envelope = px_to_append_envelope(px, confidence=float(resolved_request.payload.get("confidence", 0.5)))
    process_trace = run_w3_process_layer(
        source=resolved_request.source,
        intent=resolved_request.intent,
        target=resolved_request.target,
        mode=resolved_request.mode,
        payload=resolved_request.payload,
        process_id=resolved_cross_id,
        timestamp=timestamp,
    ).to_dict()
    system_audit = audit_cross_systems(cfg)
    component_states = {
        system: str(cfg.ecosystem["components"].get(system, {}).get("status", "active"))
        for system in cfg.cross_system["chain"]
    }
    return CrossXPlan(
        cross_id=resolved_cross_id,
        timestamp=timestamp or _now_iso(),
        request=resolved_request,
        chain=tuple(cfg.cross_system["chain"]),
        event_chain=build_event_chain(
            chain_id=resolved_cross_id,
            systems=tuple(cfg.cross_system["chain"]),
            contracts=cfg.cross_system["contracts"],
            system_states=component_states,
            supervisor=str(cross_x.get("event_chain_supervisor", "AI_SUPERVISOR")),
        ),
        program=program,
        px=px,
        append_envelope=append_envelope,
        ep_signal=_build_ep_signal_preview(program.to_text()),
        process_trace=process_trace,
        system_audit=system_audit,
    )
