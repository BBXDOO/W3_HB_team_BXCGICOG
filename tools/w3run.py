#!/usr/bin/env python3
"""
W3 Runtime CLI — tools/w3run.py

Quick wrapper to call core/runtime/engine_v2.run() from the command line.

Usage:
    python tools/w3run.py design
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

import sys
import json
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
    print("\n📋 Available Task Keywords (W3 Routing Table)\n")
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


def cmd_run(tasks):
    """Run one or more tasks."""
    from core.runtime.engine_v2 import run, run_many
    if len(tasks) == 1:
        print_json(run(tasks[0]))
    else:
        print_json(run_many(tasks))


def main():
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    if args[0] == "--heartbeat":
        cmd_heartbeat()
        return

    if args[0] == "--list-tasks":
        cmd_list_tasks()
        return

    # Validate task keywords
    unknown = [t for t in args if t not in TASK_ROUTING]
    if unknown:
        print(f"[ERROR] Unknown task(s): {unknown}", file=sys.stderr)
        print(f"Run 'python tools/w3run.py --list-tasks' to see valid task keywords.", file=sys.stderr)
        sys.exit(1)

    cmd_run(args)


if __name__ == "__main__":
    main()
