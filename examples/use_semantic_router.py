#!/usr/bin/env python3
"""
Example: Using Semantic Router with W3DB logging.
Run this to see routing decisions recorded in W3DB.
"""

from core.semantic_router import route_task
from src.w3db.store import W3DBStore

def main():
    store = W3DBStore()
    print("=== Semantic Router Demo ===")

    # Route by role
    agent1 = route_task("security audit", required_role="validation", store=store)
    print(f"Role-based routing -> {agent1.__class__.__name__}")

    # Route by concept keywords
    agent2 = route_task("create architecture diagram", concept_keywords=["architecture", "design"], store=store)
    print(f"Concept-based routing -> {agent2.__class__.__name__}")

    # Show W3DB stats
    print(f"\nW3DB Stats: {store.stats()}")

    # Show last XIZ (optional, for debugging)
    from src.w3db.crud.xiz import list_xiz
    all_xiz = list_xiz(store=store)
    if all_xiz:
        last = all_xiz[-1]
        print(f"\nLast routing log: {last.xiz_id} -> {last.result} (action: {last.action})")

if __name__ == "__main__":
    main()
