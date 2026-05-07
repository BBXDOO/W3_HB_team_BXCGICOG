"""
W3DB Relation Flow Engine
--------------------------
Implements the automatic W3 execution flow:

    INPUT → XIZ → (PROCESS) → TUF → FBD → WHB → PRX

Rules (from W3memoriea.md):
  - Process must complete (no interrupts).
  - State ≠ Decision: state values are OBSERVATION only.
  - Failure = Boundary: a non-True state creates a FBD record.
  - Action must answer: "Why is this action taken based on observed reality?"
  - XIZ records are immutable once created.
  - PRX is derived only — never user-created.

Entry point: ``run_flow(xiz, tuf, config)``

Returns a ``FlowResult`` with every domain record that was created.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from src.w3db import crud
from src.w3db.crud import fbd as fbd_crud
from src.w3db.crud import prx as prx_crud
from src.w3db.crud import whb as whb_crud
from src.w3db.crud import xiz as xiz_crud
from src.w3db.crud import tuf as tuf_crud
from src.w3db.models import FBD, PRX, TUF, WHB, XIZ


def _uid(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8].upper()}"


@dataclass
class FlowResult:
    """Structured output of a single flow run."""
    xiz: Dict = field(default_factory=dict)
    tuf: Dict = field(default_factory=dict)
    fbd: Optional[Dict] = None       # only when state != 1 (deviation detected)
    whb: Optional[Dict] = None       # only when FBD was created
    prx: Dict = field(default_factory=dict)
    state: float = 0.5               # TUF final state
    deviation_detected: bool = False

    def to_dict(self) -> dict:
        return {
            "xiz": self.xiz,
            "tuf": self.tuf,
            "fbd": self.fbd,
            "whb": self.whb,
            "prx": self.prx,
            "state": self.state,
            "deviation_detected": self.deviation_detected,
        }


def run_flow(xiz: XIZ, tuf: TUF, scale: float = 2.0) -> FlowResult:
    """
    Execute the W3 relation flow for a given XIZ + TUF pair.

    Steps
    -----
    1. Persist XIZ (immutable execution trace).
    2. Persist TUF (state observation).
    3. Observe state — if state != 1.0, a deviation is detected.
    4. If deviation → create FBD + WHB (law/patch).
    5. Render PRX (always).

    Parameters
    ----------
    xiz:   XIZ record to persist.
    tuf:   TUF record to persist.  Its ``tuf_id`` must match ``xiz.tuf_id``.
    scale: PRX intensity scale; default 2.0 per spec.

    Returns
    -------
    FlowResult with all created records.

    Raises
    ------
    ValueError  if xiz.tuf_id != tuf.tuf_id (referential integrity).
    """
    if xiz.tuf_id != tuf.tuf_id:
        raise ValueError(
            f"Referential integrity error: xiz.tuf_id={xiz.tuf_id!r} "
            f"does not match tuf.tuf_id={tuf.tuf_id!r}"
        )

    # Step 1 — XIZ (immutable)
    xiz_crud.create(xiz)

    # Step 2 — TUF
    tuf_crud.create(tuf)

    # Step 3 — Observe
    observed_state = tuf.state()
    deviation = observed_state != 1.0

    fbd_dict: Optional[Dict] = None
    whb_dict: Optional[Dict] = None

    if deviation:
        # Step 4a — FBD
        fbd = FBD(
            fbd_id=_uid("FBD"),
            source_tuf=tuf.tuf_id,
            first_deviation=f"state={observed_state} (expected 1.0)",
            failure_point=xiz.action,
            conditions=f"confidence={tuf.confidence}",
            impact=xiz.result,
            line3_patch=f"IF state={observed_state} THEN observe({tuf.tuf_id})",
        )
        fbd_crud.create(fbd)
        fbd_dict = fbd.to_dict()

        # Step 4b — WHB (law derived from FBD)
        whb = WHB(
            law_id=_uid("WHB"),
            fbd_id=fbd.fbd_id,
            condition=f"IF confidence < 0.8 AND source_tuf = {tuf.tuf_id!r}",
            action=(
                "THEN escalate observation AND re-evaluate after next process run"
            ),
        )
        whb_crud.create(whb)
        whb_dict = whb.to_dict()

    # Step 5 — PRX (always derived)
    prx = PRX.derive(tuf, prx_id=_uid("PRX"), scale=scale)
    prx_crud.create(prx)

    return FlowResult(
        xiz=xiz.to_dict(),
        tuf=tuf.to_dict(),
        fbd=fbd_dict,
        whb=whb_dict,
        prx=prx.to_dict(),
        state=observed_state,
        deviation_detected=deviation,
    )


def run_flow_from_input(
    cix_id: str,
    action: str,
    result: str,
    confidence: float,
    initial_state: float = 0.5,
    scale: float = 2.0,
    xiz_id: Optional[str] = None,
    tuf_id: Optional[str] = None,
) -> FlowResult:
    """
    Convenience wrapper: build XIZ + TUF from raw input and run the flow.

    Parameters
    ----------
    cix_id:        Identity root (CIX).
    action:        What action was executed.
    result:        Observed result text.
    confidence:    Float in [0, 1] — drives TUF state and PRX intensity.
    initial_state: TUF initial state before process ran (default 0.5).
    scale:         PRX intensity scale (default 2.0).
    xiz_id:        Optional explicit XIZ ID (auto-generated if omitted).
    tuf_id:        Optional explicit TUF ID (auto-generated if omitted).
    """
    _tuf_id = tuf_id or _uid("TUF")
    _xiz_id = xiz_id or _uid("XIZ")

    tuf = TUF(
        tuf_id=_tuf_id,
        cix_id=cix_id,
        initial=initial_state,
        final=confidence,    # final = observed confidence level
        confidence=confidence,
    )
    xiz = XIZ(
        xiz_id=_xiz_id,
        tuf_id=_tuf_id,
        action=action,
        result=result,
    )
    return run_flow(xiz=xiz, tuf=tuf, scale=scale)
