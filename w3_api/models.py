"""Pydantic models for the W3-API cross gateway."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class W3CrossRequest(BaseModel):
    """External/agent request entering the W3 cross gateway."""

    source: str = Field(..., min_length=1)
    intent: str = Field(..., min_length=1)
    target: str | None = None
    mode: str = "observe"
    payload: dict[str, Any] = Field(default_factory=dict)


class W3CrossResponse(BaseModel):
    """Traceable response from the W3 cross gateway."""

    id: str
    timestamp: str
    status: str
    w3lgu: str
    signal: dict[str, Any]


class W3CrossPlanRequest(BaseModel):
    """Plan-only Cross-L request using a Table-X PX reference."""

    px: str = Field(..., min_length=1)
    paper_context: dict[str, Any] | None = None
    include_box_suggestion: bool = False


class W3CrossPlanResponse(BaseModel):
    """Safe dispatch plan from Cross-L dispatcher."""

    contract_version: str = "1.0"
    state: str
    reason: str
    scope: str
    px: list[int] | None = None
    modew: str
    modew_style: str
    action: str
    execution_allowed: bool
    mutated: bool
    review: bool
    workset: dict[str, Any]
    safety: dict[str, bool]
    suggested_template: dict[str, Any] | None = None
