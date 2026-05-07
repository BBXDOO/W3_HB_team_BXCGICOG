"""
W3DB Automatic Relation Flow
-----------------------------
Implements the full execution pipeline per the W3memoriea spec:

  INPUT -> XIZ -> PROCESS (full run) -> TUF -> FBD -> WHB -> PRX

Usage
-----
  from src.w3db.flow import run_flow
  from src.w3db.store import W3DBStore

  store = W3DBStore()
  result = run_flow(
      input_event="Patient arrived — BP 140/90",
      cix_id="CIX-001",
      store=store,
  )
  # result contains: xiz, tuf, fbd, whb, prx records + output dict

Design rules (from spec):
  - Process must complete — no mid-run interruption.
  - XIZ is immutable after creation (immutable=True).
  - State (0 / 0.5 / 1) is for observation only — not for decision-making.
  - Action must answer "Why is this action taken based on observed reality?"
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any

from src.w3db.models import XIZ, TUF, FBD, WHB, PRX
from src.w3db.store import W3DBStore, get_store
from src.w3db.config import W3DBConfig, get_config


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _short_id(prefix: str) -> str:
    """Generate a short unique ID with the given prefix."""
    return f"{prefix}-{uuid.uuid4().hex[:8].upper()}"


def _derive_tuf_state(confidence: float) -> str:
    """
    Map confidence [0.0, 1.0] to observation state "0" / "0.5" / "1".

    Thresholds:
      >= 0.75 → "1"   (True / strong)
       > 0.25 → "0.5" (Uncertain)
      <= 0.25 → "0"   (Fail / weak)
    """
    if confidence >= 0.75:
        return "1"
    if confidence > 0.25:
        return "0.5"
    return "0"


def _derive_fbd_failure(final_state: str) -> str:
    """Map TUF final observation state to FBD failure level."""
    return {
        "1": "Green",
        "0.5": "Yellow",
        "0": "Red",
    }.get(final_state, "Yellow")


def _build_whb_condition(tuf: TUF) -> str:
    return f"IF final_state={tuf.final} AND confidence={tuf.confidence}"


def _build_whb_action(fbd: FBD) -> str:
    level_map = {
        "Red": "ESCALATE — boundary exceeded, immediate review required",
        "Yellow": "OBSERVE — boundary approached, monitor closely",
        "Green": "PASS — within boundary, no action required",
        "Blue": "EXTERNAL — defer to external assessment",
    }
    return f"THEN {level_map.get(fbd.failure, 'OBSERVE')}"


def run_flow(
    input_event: str,
    cix_id: Optional[str] = None,
    confidence: float = 0.5,
    xiz_id: Optional[str] = None,
    tuf_id: Optional[str] = None,
    fbd_id: Optional[str] = None,
    whb_id: Optional[str] = None,
    prx_id: Optional[str] = None,
    store: Optional[W3DBStore] = None,
    config: Optional[W3DBConfig] = None,
) -> Dict[str, Any]:
    """
    Execute the full W3 relation flow for a single input event.

    Parameters
    ----------
    input_event : str
        Description of the triggering event / signal.
    cix_id : str, optional
        Identity anchor (CIX_IDENTITY ID).  A new one is generated if omitted.
    confidence : float
        Confidence level in [0.0, 1.0].  Drives TUF state + PRX perception.
    xiz_id … prx_id : str, optional
        Explicit IDs for each generated record.  Auto-generated if omitted.
    store : W3DBStore, optional
        Target store.  Uses the default singleton if omitted.
    config : W3DBConfig, optional
        Runtime config.  Uses get_config() if omitted.

    Returns
    -------
    dict with keys:
      "xiz", "tuf", "fbd", "whb", "prx"  — the created model instances
      "output"                             — compact perception dict (PRX view)
    """
    s = store or get_store()
    cfg = config or get_config()

    ts = _now_iso()
    resolved_cix = cix_id or _short_id("CIX")

    # Pre-compute IDs so XIZ can reference TUF at creation time
    # (avoids any post-creation mutation, preserving the immutability contract).
    resolved_tuf_id = tuf_id or _short_id("TUF")

    # -----------------------------------------------------------------
    # Step 1 — XIZ: log the input event (immutable after creation)
    # -----------------------------------------------------------------
    xiz = XIZ(
        xiz_id=xiz_id or _short_id("XIZ"),
        action=input_event,
        timestamp=ts,
        result="",
        tuf_id=resolved_tuf_id,
        immutable=cfg.is_immutable_xiz(),
    )
    s.create_xiz(xiz)

    # -----------------------------------------------------------------
    # Step 2 — TUF: observe the process state
    # -----------------------------------------------------------------
    obs_state = _derive_tuf_state(confidence)
    tuf = TUF(
        tuf_id=resolved_tuf_id,
        cix_id=resolved_cix,
        initial=obs_state,
        final=obs_state,
        confidence=confidence,
        resolution="",
        note=f"Derived from event: {input_event[:60]}",
    )
    s.create_tuf(tuf)

    # -----------------------------------------------------------------
    # Step 3 — FBD: detect boundary / failure point
    # -----------------------------------------------------------------
    fbd_failure = _derive_fbd_failure(tuf.final)
    fbd = FBD(
        fbd_id=fbd_id or _short_id("FBD"),
        tuf_id=tuf.tuf_id,
        first_deviation=f"Confidence={confidence:.3f} → state={tuf.final}",
        failure_point="PROCESS_COMPLETE",
        failure=fbd_failure,
        conditions=f"initial={tuf.initial} final={tuf.final}",
        impact=f"Boundary {'exceeded' if fbd_failure == 'Red' else 'within limits'}",
        line3_patch="",         # set after WHB
    )
    s.create_fbd(fbd)

    # -----------------------------------------------------------------
    # Step 4 — WHB: generate IF → THEN patch (Line 3)
    # -----------------------------------------------------------------
    whb_condition = _build_whb_condition(tuf)
    whb_action = _build_whb_action(fbd)
    whb = WHB(
        law_id=whb_id or _short_id("WHB"),
        fbd_id=fbd.fbd_id,
        condition=whb_condition,
        action=whb_action,
    )
    s.create_whb(whb)

    # Back-fill FBD line3_patch from WHB
    s.update_fbd(fbd.fbd_id, line3_patch=f"{whb_condition} {whb_action}")

    # -----------------------------------------------------------------
    # Step 5 — PRX: derive visual perception (derived only — not a decision)
    # -----------------------------------------------------------------
    prx = PRX.from_tuf(prx_id or _short_id("PRX"), tuf)
    s.create_prx(prx)

    # -----------------------------------------------------------------
    # Compact output (OPD Dashboard view)
    # -----------------------------------------------------------------
    output: Dict[str, Any] = {
        "cix": resolved_cix,
        "xiz": xiz.xiz_id,
        "tuf": {
            "id": tuf.tuf_id,
            "initial": tuf.initial,
            "final": tuf.final,
            "confidence": tuf.confidence,
        },
        "fbd": {
            "id": fbd.fbd_id,
            "failure": fbd.failure,
            "impact": fbd.impact,
        },
        "whb": {
            "id": whb.law_id,
            "condition": whb.condition,
            "action": whb.action,
        },
        "prx": {
            "id": prx.prx_id,
            "symbol": prx.symbol,
            "color": prx.color,
            "intensity": prx.intensity,
        },
    }

    return {
        "xiz": xiz,
        "tuf": tuf,
        "fbd": fbd,
        "whb": whb,
        "prx": prx,
        "output": output,
    }
