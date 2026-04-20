"""
W3 Module Loader Router
Path: core/module-loader/router.py

Purpose:
- Route incoming tasks to the correct AI module
- Load identity profile (.idp.json)
- Return execution plan

Author: BBX19 / W3
"""

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
IDENTITY_DIR = BASE_DIR / "identity"
REGISTRY_FILE = BASE_DIR / "module-registry.json"


class RouterError(Exception):
    pass


def load_json(path):
    if not path.exists():
        raise RouterError(f"Missing file: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_registry():
    return load_json(REGISTRY_FILE)


def load_identity(module_name):
    path = IDENTITY_DIR / f"{module_name}.idp.json"
    return load_json(path)


def route_task(task_name):
    """
    Example:
        route_task("design")
        route_task("verify")
    """
    registry = load_registry()

    if task_name not in registry:
        raise RouterError(f"No route for task: {task_name}")

    module_name = registry[task_name]
    identity = load_identity(module_name)

    return {
        "task": task_name,
        "assigned_module": module_name,
        "identity": identity
    }


def execution_plan(task_name):
    routed = route_task(task_name)

    return {
        "task": routed["task"],
        "run_with": routed["assigned_module"],
        "role": routed["identity"]["identity"]["designation"],
        "status": routed["identity"]["identity"]["status"],
        "next_step": f"Execute task '{task_name}' using {routed['assigned_module']}"
    }


if __name__ == "__main__":
    # demo
    demo_tasks = ["design", "verify", "research"]

    for task in demo_tasks:
        try:
            result = execution_plan(task)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"[ERROR] {task}: {e}")
