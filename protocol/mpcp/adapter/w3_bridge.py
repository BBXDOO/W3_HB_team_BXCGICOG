"""Explicit W3 bridge interface for MPCP.

The bridge owns no W3 executor and never reports success on behalf of one.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any


def execute_with_w3(
    task: Mapping[str, Any],
    *,
    executor: Callable[[Mapping[str, Any]], Mapping[str, Any]],
) -> dict:
    """Call an injected W3 executor and preserve its inspectable result."""
    if not isinstance(task, Mapping) or not task:
        raise ValueError("W3_BRIDGE:TASK_MAPPING_REQUIRED")
    if not callable(executor):
        raise TypeError("W3_BRIDGE:EXECUTOR_REQUIRED")
    result = executor(dict(task))
    if not isinstance(result, Mapping):
        raise TypeError("W3_BRIDGE:RESULT_MAPPING_REQUIRED")
    return {
        "schema": "mpcp.w3_bridge.1",
        "task": dict(task),
        "result": dict(result),
        "executor": getattr(executor, "__name__", executor.__class__.__name__),
        "bridge_mutated": False,
    }
