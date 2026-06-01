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
