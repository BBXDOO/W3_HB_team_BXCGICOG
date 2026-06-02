"""Codex agent workspace helpers for W3.

Codex is registered as an implementation/repo-executor agent. The package is
intentionally small and read-only by default: helpers create execution packets
and trace plans, but do not mutate W3 truth stores or merge pull requests.
"""

from .agent import CODEX_VERSION, build_execution_packet, load_manifest, validate_manifest

__all__ = [
    "CODEX_VERSION",
    "build_execution_packet",
    "load_manifest",
    "validate_manifest",
]
