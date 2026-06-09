"""Routes for the W3-API cross gateway."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter

from croll.cross_l_dispatcher import dispatch_workset
from w3_api.adapters.ep_signal_adapter import build_ep_signal_preview
from w3_api.adapters.w3db_adapter import build_w3db_trace_plan
from w3_api.adapters.w3lgu_adapter import build_cross_w3lgu_packet
from w3_api.models import W3CrossPlanRequest, W3CrossPlanResponse, W3CrossRequest, W3CrossResponse

router = APIRouter(prefix="/w3", tags=["w3-cross"])


@router.post("/cross", response_model=W3CrossResponse)
def cross(req: W3CrossRequest) -> W3CrossResponse:
    """Cross-gateway entrypoint for external/AI-agent intents.

    Flow: request intent → W3Lgu five-line packet → W3DB/EP_SIGNAL trace plans →
    traceable signal response. No underlying W3 subsystem is mutated here.
    """

    event_id = str(uuid4())
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    program = build_cross_w3lgu_packet(
        source=req.source,
        intent=req.intent,
        target=req.target,
        mode=req.mode,
        payload=req.payload,
    )
    w3lgu_text = program.to_text()
    signal = {
        "type": "W3_API_CROSS",
        "source": req.source,
        "target": req.target,
        "mode": req.mode,
        "traceable": True,
        "mutated": False,
        "w3db": build_w3db_trace_plan(event_id, program),
        "ep_signal": build_ep_signal_preview(w3lgu_text),
        "references": [
            "protocol/w3lgu/RML01.md",
            "docs/integration_guide.md",
            "docs/standards/referencing_standard.md",
        ],
    }
    return W3CrossResponse(
        id=event_id,
        timestamp=now,
        status="accepted",
        w3lgu=w3lgu_text,
        signal=signal,
    )


@router.post("/cross/plan", response_model=W3CrossPlanResponse)
def cross_plan(req: W3CrossPlanRequest) -> W3CrossPlanResponse:
    """Return a safe Cross-L dispatch plan from a PX reference.

    This endpoint is planner-only. It does not execute Modew, mutate truth,
    write repository files, merge changes, or call external systems.
    """

    plan = dispatch_workset(req.px, paper_context=req.paper_context)
    return W3CrossPlanResponse(**plan)
