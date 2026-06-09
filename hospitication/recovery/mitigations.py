"""Mitigation text catalog. Text only; no filesystem mutation."""

from __future__ import annotations

MITIGATIONS = {
    "semantic_pressure": (
        "Create or refresh a compact glossary for overloaded W3 terms.",
        "Add causal anchors when a document introduces new governance/replay meaning.",
    ),
    "dependency_fatigue": (
        "Review high-frequency imports and document intended dependency boundaries.",
        "Prefer boundary modules over direct cross-layer imports when pressure rises.",
    ),
    "replay_complexity": (
        "Keep replay, event, and outcome-ledger contracts explicitly versioned.",
        "Add replay fixtures before changing recovery or ledger behavior.",
    ),
    "recovery_resistance": (
        "Split large change surfaces with tests before attempting recovery work.",
        "Prefer proposal-first recovery plans and avoid direct truth mutation.",
    ),
    "cognitive_cost": (
        "Add index documents for high-breadth areas and remove stale navigation paths.",
        "Group operational docs by owner, lifecycle, and replay relevance.",
    ),
}
