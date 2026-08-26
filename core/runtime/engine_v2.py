import json
import time
import uuid
from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict

from core.module_loader.router import execution_plan
from core.memory.memory_bus import add_memory, search_memory, get_memory
from core.runtime.agents import get_agent

MAX_WORKERS = 3
W3LGU_RUNTIME_MODULES = {"REDR", "PSP2", "DTML", "LRC2"}
W3LGU_REQUIRED_RESULT_FIELDS = {
    "confidence",
    "decision",
    "details",
    "input_type",
    "module",
    "mutated",
    "next",
    "reason",
    "standby",
    "status",
    "traceable",
}
W3LGU_REQUIRED_IDENTITY_FIELDS = {"chain_id", "event_id", "package_id"}


class EngineError(Exception):
    pass


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def trace_id():
    return uuid.uuid4().hex


# -------------------------------------------------
# CONTEXT
# -------------------------------------------------

def build_context(task, request=None, *, authority_context=None):
    hits = search_memory(task)
    request = dict(request) if isinstance(request, Mapping) else {}

    trusted_authority = dict(authority_context) if isinstance(authority_context, Mapping) else {}

    return {
        "trace_id": trace_id(),
        "matches": len(hits),
        "records": hits[:5],
        "request": request,
        "source": request.get("source"),
        "target": request.get("target"),
        "mode": request.get("mode"),
        "payload": request.get("payload", {}),
        # This field is deliberately supplied out-of-band by the calling ENV.
        # Values inside request/payload can never create Creator/Origin authority.
        "authority_context": trusted_authority,
        "request_boundary": "UNTRUSTED_INPUT",
        "timestamp": now(),
    }


# -------------------------------------------------
# DISPATCH LAYER
# -------------------------------------------------

def dispatch(module_name, task, plan, context):
    agent = get_agent(module_name)
    return agent.execute(task, plan, context)


def _memory_content(agent_result: Dict[str, Any]) -> str:
    return json.dumps(agent_result, ensure_ascii=False, sort_keys=True)


def validate_agent_result(module_name: str, agent_result: Dict[str, Any]) -> Dict[str, Any]:
    """Return a non-mutating validation summary for engine result contracts."""
    missing = []
    identity_missing = []
    blocking_status = None
    if module_name in W3LGU_RUNTIME_MODULES:
        missing = sorted(field for field in W3LGU_REQUIRED_RESULT_FIELDS if field not in agent_result)
        details = agent_result.get("details") if isinstance(agent_result.get("details"), dict) else {}
        identity = details.get("identity") if isinstance(details.get("identity"), dict) else {}
        identity_expected = bool(
            details.get("route_scope")
            or details.get("route_stamp")
            or details.get("cross_routes")
            or details.get("unknown_routes")
            or agent_result.get("status") == "COMPLETED"
        )
        if identity_expected:
            identity_missing = sorted(field for field in W3LGU_REQUIRED_IDENTITY_FIELDS if not identity.get(field))
        if identity_missing:
            blocking_status = "REVIEW_REQUIRED"

    status = "valid" if not missing and not identity_missing else "review_required"
    return {
        "status": status,
        "module": module_name,
        "missing_fields": missing,
        "identity_missing_fields": identity_missing,
        "blocking_status": blocking_status,
        "mutated": bool(agent_result.get("mutated", False)),
        "traceable": bool(agent_result.get("traceable", True)) and not missing and not identity_missing,
        "review": bool(agent_result.get("review", False)) or bool(missing) or bool(identity_missing),
    }


# -------------------------------------------------
# SINGLE RUN
# -------------------------------------------------

def run(task, request=None, *, authority_context=None):
    started = time.time()
    plan = execution_plan(task)
    context = build_context(task, request, authority_context=authority_context)

    try:
        agent_result = dispatch(plan["run_with"], task, plan, context)
        if not isinstance(agent_result, dict):
            agent_result = {
                "contract_version": "1.0",
                "status": "UNAVAILABLE",
                "module": plan["run_with"],
                "task": task,
                "action": "invalid_agent_result",
                "summary": "Agent execute() returned a non-dictionary result; no task was completed.",
                "reason": "Agent execute() must return a result dictionary.",
                "artifacts": [],
                "mutated": False,
                "traceable": True,
                "review": True,
                "details": {"invalid_result_type": type(agent_result).__name__},
            }

        status = str(agent_result.get("status") or "FAILED")
        summary = str(agent_result.get("summary") or "No result summary provided.")
        result_validation = validate_agent_result(plan["run_with"], agent_result)
        successful = status == "COMPLETED"

        result = {
            "status": status,
            "task": task,
            "module": plan["run_with"],
            "output": summary,
            "agent_result": agent_result,
            "result_validation": result_validation,
            "artifacts": agent_result.get("artifacts", []),
            "latency_ms": int((time.time() - started) * 1000),
            "time": now(),
            "trace_id": context["trace_id"],
        }

        add_memory(
            source=plan["run_with"],
            topic=task,
            content=_memory_content(agent_result),
            tags=["runtime", "success" if successful else status.lower()],
            score=5 if successful else 1,
            record_type="runtime_result",
        )

        return result

    except Exception as e:
        error_result = {
            "status": "FAILED",
            "task": task,
            "error": str(e),
            "time": now(),
            "trace_id": context["trace_id"],
        }

        add_memory(
            source="runtime",
            topic=task,
            content=str(e),
            tags=["runtime", "error"],
            score=1,
            record_type="runtime_result",
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
        "trace_id": trace_id(),
    }


if __name__ == "__main__":
    print(json.dumps(run("design"), indent=2, ensure_ascii=False))
    print(json.dumps(run_many(["verify", "audit", "security"]), indent=2, ensure_ascii=False))
    print(json.dumps(heartbeat(), indent=2, ensure_ascii=False))
