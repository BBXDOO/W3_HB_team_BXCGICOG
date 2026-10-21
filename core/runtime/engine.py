"""
W3 Runtime Engine
Path: core/runtime/engine.py

Purpose:
- Receive task input
- Route to correct module
- Read shared memory
- Produce execution result
- Save output to memory

Author: BBX19 / W3
"""

import json
from pathlib import Path

# import internal systems
from core.modules_loader.router import execution_plan
from core.memory.memory_bus import (
    add_memory,
    search_memory,
    get_memory
)


class EngineError(Exception):
    pass


def build_context(task):
    """
    Search memory for relevant context
    """
    hits = search_memory(task)

    return {
        "matches": len(hits),
        "records": hits[:5]
    }


def simulate_agent(task, plan, context):
    """
    Legacy placeholder executor.

    It must not fabricate success. Use ``engine_v2.run`` with a module-specific
    ``execute()`` implementation when a task needs to report completion.
    """

    return {
        "task": task,
        "module": plan["run_with"],
        "role": plan["role"],
        "memory_matches": context["matches"],
        "status": "UNAVAILABLE",
        "result": (
            f"{plan['run_with']} has no legacy executor for task '{task}'. "
            "No task was completed and no artifact was created."
        ),
        "mutated": False,
        "traceable": True,
        "review": True,
    }


def run(task, request=None, *, authority_context=None):
    """Compatibility envelope over the single v2 execution path.

    The old status/plan/context/output keys remain; output is the actual
    agent result. New callers should use engine_v2 or WorkflowRuntime.
    """
    from . import engine_v2
    result = engine_v2.run(task, request, authority_context=authority_context)
    try:
        plan = execution_plan(task)
    except Exception:
        plan = None
    return {
        **result,
        "plan": plan,
        "context": {"trace_id": result["trace_id"]},
        "output": result.get("agent_result", {"status": result["status"],
                                                "reason": result.get("error")}),
    }


def heartbeat():
    """
    Runtime health check
    """
    return {
        "engine": "ONLINE",
        "recent_memory": len(get_memory(20))
    }


if __name__ == "__main__":
    demo = run("design")

    print(json.dumps(demo, indent=2, ensure_ascii=False))
    print(json.dumps(heartbeat(), indent=2, ensure_ascii=False))
