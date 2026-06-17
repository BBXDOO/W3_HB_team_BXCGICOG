import json
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed

from core.module_loader.router import execution_plan
from core.memory.memory_bus import add_memory, search_memory, get_memory
from core.runtime.agents import get_agent

MAX_WORKERS = 3

class EngineError(Exception):
    pass

def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def trace_id():
    return uuid.uuid4().hex

# -------------------------------------------------
# CONTEXT
# -------------------------------------------------

def build_context(task, request=None):
    hits = search_memory(task)
    request = request or {}

    return {
        "trace_id": trace_id(),
        "matches": len(hits),
        "records": hits[:5],
        "request": request,
        "source": request.get("source"),
        "target": request.get("target"),
        "mode": request.get("mode"),
        "payload": request.get("payload", {}),
        "timestamp": now()
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

def run(task, request=None):
    started = time.time()
    plan = execution_plan(task)
    context = build_context(task, request)

    try:
        output = dispatch(plan["run_with"], task, plan, context)

        result = {
            "status": "SUCCESS",
            "task": task,
            "module": plan["run_with"],
            "output": output,
            "latency_ms": int((time.time() - started) * 1000),
            "time": now(),
            "trace_id": context["trace_id"]
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
        error_result = {
            "status": "FAILED",
            "task": task,
            "error": str(e),
            "time": now(),
            "trace_id": context["trace_id"]
        }

        add_memory(
            source="runtime",
            topic=task,
            content=str(e),
            tags=["runtime", "error"],
            score=1
        )

        return error_result

# -------------------------------------------------
# PARALLEL RUN
# -------------------------------------------------

def run_many(tasks, max_workers=MAX_WORKERS):
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
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
        "time": now(),
        "trace_id": trace_id()
    }

# -------------------------------------------------
# DEMO
# -------------------------------------------------

if __name__ == "__main__":
    print(json.dumps(run("design"), indent=2, ensure_ascii=False))
    print(json.dumps(run_many(["verify", "audit", "security"]), indent=2, ensure_ascii=False))
    print(json.dumps(heartbeat(), indent=2, ensure_ascii=False))
