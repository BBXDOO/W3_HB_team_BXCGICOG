#!/usr/bin/env python3
"""W3 Runtime CLI — tools/w3run.py

Usage:
    python tools/w3run.py design
    python tools/w3run.py flow --request-file modules/ChatGPT/requests/flow_request.json
    python tools/w3run.py design verify audit
    python tools/w3run.py --heartbeat
    python tools/w3run.py --list-tasks
"""
import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

def task_routing():
    from core.module_loader.router import load_registry
    return load_registry()

def print_json(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))

def cmd_list_tasks():
    print("\nAvailable Task Keywords (W3 Routing Table)\n")
    by_module = {}
    for task, module in task_routing().items():
        by_module.setdefault(module, []).append(task)
    for module, tasks in by_module.items():
        print(f"  {module:15s}: {', '.join(tasks)}")
    print()

def cmd_heartbeat():
    from core.runtime.engine_v2 import heartbeat
    print_json(heartbeat())

def cmd_run(tasks, request=None):
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
    parser.add_argument("--request-file", help="JSON request context for one task; the path is recorded in the generated artifact")
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

    routing = task_routing()
    unknown = [task for task in args.tasks if task not in routing]
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
