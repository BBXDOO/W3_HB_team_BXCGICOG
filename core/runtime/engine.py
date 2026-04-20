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
from core.module_loader.router import execution_plan
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
    Placeholder executor.
    Future = real AI dispatch layer
    """

    return {
        "task": task,
        "module": plan["run_with"],
        "role": plan["role"],
        "memory_matches": context["matches"],
        "result": f"{plan['run_with']} processed task '{task}'"
    }


def run(task):
    """
    Main runtime pipeline
    """

    # STEP 1 route task
    plan = execution_plan(task)

    # STEP 2 collect memory context
    context = build_context(task)

    # STEP 3 execute assigned module
    result = simulate_agent(task, plan, context)

    # STEP 4 save result
    add_memory(
        source=plan["run_with"],
        topic=task,
        content=result["result"],
        tags=["runtime", "task"],
        score=5
    )

    return {
        "status": "SUCCESS",
        "plan": plan,
        "context": context,
        "output": result
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
