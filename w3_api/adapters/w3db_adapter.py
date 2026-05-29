"""W3-API → W3DB gateway adapter.

The first W3-API gateway does not write to W3DB. It returns a trace plan so
callers can see how the request would be appended by a future persistence layer.
"""

from __future__ import annotations

from typing import Any

from protocol.w3lgu import W3LguFiveLineProgram


def build_w3db_trace_plan(event_id: str, program: W3LguFiveLineProgram) -> dict[str, Any]:
    """Return deterministic W3DB append-intent metadata without mutating W3DB."""

    return {
        "mode": "append_plan_only",
        "mutated": False,
        "xiz_hint": f"XIZ-API-{event_id[:8]}",
        "tuf_hint": f"TUF-API-{event_id[:8]}",
        "source": program.memory.get("SOURCE"),
        "target": program.law.get("TARGET"),
    }
