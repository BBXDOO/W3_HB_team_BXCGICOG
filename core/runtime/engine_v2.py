import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from core.module_loader.router import execution_plan
from core.memory.memory_bus import (
    add_memory,
    search_memory,
    get_memory
)
from core.runtime.agents import get_agent

MAX_WORKERS = 3


class EngineError(Exception):
    pass


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


# -------------------------------------------------
# CONTEXT
# -------------------------------------------------

def build_context(task):
    hits = search_memory(task)

    return {
        "matches": len(hits),
        "records": hits[:5]
    }


# -------------------------------------------------
# DISPATCH LAYER
# -------------------------------------------------

def dispatch(module_name, task, plan, context):
    agent = get_agent(module_name)
    return agent.run(task, plan, context)


# -------------------------------------------------
# SINGLE RUN
# -------------------------------------------------

def run(task):
    started = time.time()

    plan = execution_plan(task)
    context = build_context(task)

    try:
        output = dispatch(plan["run_with"], task, plan, context)

        result = {
            "status": "SUCCESS",
            "task": task,
            "module": plan["run_with"],
            "output": output,
            "latency_ms": int((time.time() - started) * 1000),
            "time": now()
        }

        add_memory(
            source=plan["run_with"],
            topic=task,
            content=output,
            tags=["runtime", "success"],
            score=5
        )

        return result

    except Exception as e:
        add_memory(
            source="runtime",
            topic=task,
            content=str(e),
            tags=["runtime", "error"],
            score=1
        )

        return {
            "status": "FAILED",
            "task": task,
            "error": str(e),
            "time": now()
        }


# -------------------------------------------------
# PARALLEL RUN
# -------------------------------------------------

def run_many(tasks):
    results = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = [ex.submit(run, task) for task in tasks]

        for future in as_completed(futures):
            results.append(future.result())

    return results


# -------------------------------------------------
# HEARTBEAT
# -------------------------------------------------

def heartbeat():
    return {
        "engine": "ONLINE",
        "workers": MAX_WORKERS,
        "recent_memory": len(get_memory(20)),
        "time": now()
    }


# -------------------------------------------------
# DEMO
# -------------------------------------------------

if __name__ == "__main__":
    print(json.dumps(run("design"), indent=2, ensure_ascii=False))
    print(json.dumps(run_many([
        "verify",
        "audit",
        "security"
    ]), indent=2, ensure_ascii=False))
    print(json.dumps(heartbeat(), indent=2, ensure_ascii=False))
