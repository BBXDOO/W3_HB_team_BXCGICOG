"""Example: route Hospitication report interpretation without overwriting truth."""

from __future__ import annotations

from core.semantic_router import interpret_hospitication_report
from src.w3db.store import W3DBStore


def main() -> None:
    store = W3DBStore()
    agent = interpret_hospitication_report(
        "hospitication-report.json",
        store=store,
    )
    print(f"Routed to: {agent.module_name}")
    print(f"W3DB traces: xiz={len(store.list_xiz())} prx={len(store.list_prx())}")


if __name__ == "__main__":
    main()
