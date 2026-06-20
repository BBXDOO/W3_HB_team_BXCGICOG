#!/usr/bin/env python3
"""
W3 Runtime CLI — tools/w3run.py

Usage:
    python tools/w3run.py design
    python tools/w3run.py flow --request-file modules/ChatGPT/requests/flow_request.json
    python tools/w3run.py design verify audit
    python tools/w3run.py --heartbeat
    python tools/w3run.py --list-tasks

Supported task keywords (from core/module-loader/module-registry.json):
    design, architecture, flow, simulation   -> ChatGPT
    verify, verification, audit, security    -> Gemini
    pattern, signals, insight                -> Grok
    research, scale, planning                -> DeepSeek
    governance, policy, compliance           -> Copilot-Gm
    reason, critical_reasoning, interpret, document -> Cast
    identity, philosophy                     -> BBEX-Core
    vision                                   -> BBX19
"""

import argparse
import json
import sys
from pathlib import Path

# Add repo root to path so imports resolve from any working directory
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

TASK_ROUTING = {
    "design": "ChatGPT",
    "architecture": "ChatGPT",
    "flow": "ChatGPT",
    "simulation": "ChatGPT",
    "verify": "Gemini",
    "verification": "Gemini",
    "audit": "Gemini",
    "security": "Gemini",
    "pattern": "Grok",
    "signals": "Grok",
    "insight": "Grok",
    "research": "DeepSeek",
    "scale": "DeepSeek",
    "planning": "DeepSeek",
    "governance": "Copilot-Gm",
    "policy": "Copilot-Gm",
    "compliance": "Copilot-Gm",
    "reason": "Cast",
    "critical_reasoning": "Cast",
    "interpret": "Cast",
    "document": "Cast",
    "identity": "BBEX-Core",
    "philosophy": "BBEX-Core",
    "vision": "BBX19",
}


def print_json(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_list_tasks():
    """Print all available task keywords grouped by module."""
    print("\nAvailable Task Keywords (W3 Routing Table)\n")
    by_module = {}
    for task, module in TASK_ROUTING.items():
        by_module.setdefault(module, []).append(task)
    for module, tasks in by_module.items():
        print(f"  {module:15s}: {', '.join(tasks)}")
    print()


def cmd_heartbeat():
    """Check engine status."""
    from core.runtime.engine_v2 import heartbeat

    print_json(heartbeat())


def cmd_run(tasks, request=None):
    """Run one or more tasks."""
    from core.runtime.engine_v2 import run, run_many

    if len(tasks) == 1:
        print_json(run(tasks[0], request=request))
    else:
        if request:
            raise ValueError("--request-file is supported for one task at a time.")
        print_json(run_many(tasks))


def load_request_file(path_text):
    path = Path(path_text).expanduser()
    if not path.exists():
        raise ValueError(f"Request file not found: {path}")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Request file must contain a JSON object: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("Request file must contain one JSON object.")

    data["_request_file"] = str(path)
    return data


def main():
    parser = argparse.ArgumentParser(description="Run W3 runtime task routing.")
    parser.add_argument("--heartbeat", action="store_true", help="show runtime status")
    parser.add_argument("--list-tasks", action="store_true", help="show task routing table")
    parser.add_argument(
        "--request-file",
        help="JSON request context for one task; the path is recorded in the generated artifact",
    )
    parser.add_argument("tasks", nargs="*", help="one or more registered task keywords")
    args = parser.parse_args()

    if args.heartbeat:
        if args.tasks or args.request_file:
            parser.error("--heartbeat cannot be combined with tasks or --request-file")
        cmd_heartbeat()
        return

    if args.list_tasks:
        if args.tasks or args.request_file:
            parser.error("--list-tasks cannot be combined with tasks or --request-file")
        cmd_list_tasks()
        return

    if not args.tasks:
        parser.print_help()
        return

    unknown = [task for task in args.tasks if task not in TASK_ROUTING]
    if unknown:
        parser.error(f"Unknown task(s): {unknown}. Use --list-tasks to see valid keywords.")

    if args.request_file and len(args.tasks) != 1:
        parser.error("--request-file supports one task at a time.")

    try:
        request = load_request_file(args.request_file) if args.request_file else None
        cmd_run(args.tasks, request=request)
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
