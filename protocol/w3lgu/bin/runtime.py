from __future__ import annotations

from pathlib import Path
from typing import Dict, List


SYSTEM_NAME = "W3Lgu Runtime"
VERSION = "1.0"
MUTATION_ALLOWED = False

BASE_DIR = Path(__file__).resolve().parent
W3LGU_DIR = BASE_DIR.parent

REQUIRED_NODES = [
    "adapters",
    "signals",
    "memory",
]


def check_node(node: str) -> Dict[str, str]:
    path = W3LGU_DIR / node
    status = "FOUND" if path.exists() else "MISSING"

    return {
        "node": node,
        "path": str(path),
        "status": status,
    }


def boot_system() -> Dict[str, object]:
    nodes: List[Dict[str, str]] = [check_node(node) for node in REQUIRED_NODES]

    missing = [
        item["node"]
        for item in nodes
        if item["status"] == "MISSING"
    ]

    status = "ACTIVE" if not missing else "DEGRADED"

    report: Dict[str, object] = {
        "system": SYSTEM_NAME,
        "version": VERSION,
        "status": status,
        "mutation_allowed": MUTATION_ALLOWED,
        "base_dir": str(BASE_DIR),
        "w3lgu_dir": str(W3LGU_DIR),
        "nodes": nodes,
        "missing": missing,
    }

    return report


def print_report(report: Dict[str, object]) -> None:
    print(f"--- [G-State: {report['status']}] ---")
    print(f"{report['system']} v{report['version']} is initializing...")
    print(f"Mutation allowed: {report['mutation_allowed']}")
    print(f"W3Lgu dir: {report['w3lgu_dir']}")

    for node in report["nodes"]:
        print(f"Node {node['node'].upper()}: {node['status']}")


if __name__ == "__main__":
    print_report(boot_system())
