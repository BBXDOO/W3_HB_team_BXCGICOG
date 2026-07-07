"""Pytest collection guardrails for standalone protocol smoke scripts.

Some protocol checks are executable smoke scripts with top-level harnesses and
``sys.exit`` calls. They remain runnable directly, but collecting them as pytest
modules aborts the suite during import.
"""

collect_ignore = [
    "protocol/mpcp/test_agent_mpcp_alignment.py",
    "protocol/mpcp/test_condien_blueprint.py",
    "protocol/w3db/test_crud.py",
    "protocol/w3db/test_flow.py",
]
