"""W3 Module Router.

Canonical module data lives under `modules/`:
- `modules/registry.json` provides task -> module routing.
- `modules/<name>/module.json` provides the module manifest.

The importable runtime adapter remains here so existing
`core.module_loader.router` imports continue to work.
"""

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
MODULES_DIR = REPO_ROOT / "modules"
REGISTRY_FILE = MODULES_DIR / "registry.json"


class RouterError(Exception):
    pass


def load_json(path):
    if not path.exists():
        raise RouterError(f"Missing file: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_registry():
    registry = load_json(REGISTRY_FILE)
    routing = registry.get("routing")
    if not isinstance(routing, dict):
        raise RouterError("modules/registry.json has no valid 'routing' object")
    return routing


def load_identity(module_name):
    """Load the canonical module manifest used as runtime identity metadata."""
    path = MODULES_DIR / module_name / "module.json"
    return load_json(path)


def route_task(task_name):
    registry = load_registry()

    if task_name not in registry:
        raise RouterError(
            f"No route for task: '{task_name}'. Available: {list(registry.keys())}"
        )

    module_name = registry[task_name]
    identity = load_identity(module_name)

    return {
        "task": task_name,
        "assigned_module": module_name,
        "identity": identity,
    }


def execution_plan(task_name):
    routed = route_task(task_name)
    manifest = routed["identity"]

    return {
        "task": routed["task"],
        "run_with": routed["assigned_module"],
        "role": manifest.get("role") or manifest.get("display_name", "—"),
        "status": manifest.get("status", "unknown"),
        "responsibilities": manifest.get("responsibilities", []),
        "next_step": f"Execute task '{task_name}' using {routed['assigned_module']}",
    }


if __name__ == "__main__":
    demo_tasks = [
        "design", "verify", "audit", "pattern", "research",
        "governance", "reason", "identity", "vision", "security",
    ]

    for task in demo_tasks:
        try:
            result = execution_plan(task)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        except Exception as exc:
            print(f"[ERROR] {task}: {exc}")
