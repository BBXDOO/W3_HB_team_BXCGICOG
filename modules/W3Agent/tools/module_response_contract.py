"""Module response contract helpers for W3Agent.

This file is report-only.
It does not execute modules.
It does not mutate repository content.
It only builds a response preview for IGET @module:<name> dispatch tags.
"""

from __future__ import annotations

from typing import Iterable


DEFAULT_RETURN_TO = "IGET"
DEFAULT_ACTION_MODE = "report_only"


MODULE_RESPONSE_PROFILES = {
    "IGET": {
        "status": "can_acknowledge",
        "ready_level": "3/5",
        "capability": "issue brief, module tag dispatch, governance summary, proof trace",
        "need": "BBX19 approval before creating or dispatching work",
        "risk": "low",
    },
    "W3-API": {
        "status": "can_review_gateway_scope",
        "ready_level": "2/5",
        "capability": "cross gateway scope review and endpoint boundary check",
        "need": "endpoint, intent, payload shape, and no-mutation rule",
        "risk": "medium",
    },
    "DTML": {
        "status": "can_review_docs_structure",
        "ready_level": "2/5",
        "capability": "docs, report, template, and structure review",
        "need": "target document path and expected report type",
        "risk": "low",
    },
    "W3DB": {
        "status": "can_review_memory_trace",
        "ready_level": "2/5",
        "capability": "memory, log, state, and trace inspection",
        "need": "trace target, memory surface, and persistence boundary",
        "risk": "medium",
    },
    "MPCP": {
        "status": "can_review_protocol_boundary",
        "ready_level": "3/5",
        "capability": "boundary, rule, approval, ROT, Paper, and MODEW relation review",
        "need": "event scope, responsible module, assist modules, and return path",
        "risk": "medium",
    },
    "CROLL": {
        "status": "can_review_cross_l_plan",
        "ready_level": "2/5",
        "capability": "Cross-L and CROLL planning review",
        "need": "language boundary, source block, target block, and denial rule",
        "risk": "medium",
    },
    "EP_SIGNAL": {
        "status": "can_review_signal_preview",
        "ready_level": "2/5",
        "capability": "signal, preview, and pulse trace review",
        "need": "signal source, expected pulse, and no-mutation boundary",
        "risk": "medium",
    },
    "W3Lgu": {
        "status": "can_review_language_packet",
        "ready_level": "3/5",
        "capability": "W3Lgu packet, meaning, and line structure review",
        "need": "packet lines, intended meaning, and return contract",
        "risk": "medium",
    },
    "REDR": {
        "status": "can_review_routing_package",
        "ready_level": "2/5",
        "capability": "event, package, and routing preparation review",
        "need": "event package, target route, and evidence before routing",
        "risk": "medium-high",
    },
    "PSP2": {
        "status": "can_review_process_preview",
        "ready_level": "2/5",
        "capability": "process preview and route preparation review",
        "need": "process unit, route intent, and return target",
        "risk": "medium",
    },
    "LRC2": {
        "status": "can_review_log_trace",
        "ready_level": "2/5",
        "capability": "log, record, and continuity trace review",
        "need": "event id, trace target, and record boundary",
        "risk": "low-medium",
    },
}


DEFAULT_MODULE_RESPONSE = {
    "status": "needs_registry_review",
    "ready_level": "0/5",
    "capability": "unknown module capability",
    "need": "module profile or explicit BBX19 instruction",
    "risk": "unknown",
}


def dedupe(items: Iterable[str]) -> list[str]:
    """Return unique items while preserving order."""
    ordered: list[str] = []

    for item in items:
        clean = str(item).strip()
        if clean and clean not in ordered:
            ordered.append(clean)

    return ordered


def module_response_contract(module: str) -> dict[str, object]:
    """Return one report-only response contract for a dispatched module tag."""
    profile = MODULE_RESPONSE_PROFILES.get(module, DEFAULT_MODULE_RESPONSE)

    return {
        "module": module,
        "status": profile["status"],
        "ready_level": profile["ready_level"],
        "capability": profile["capability"],
        "need": profile["need"],
        "risk": profile["risk"],
        "return_to": DEFAULT_RETURN_TO,
        "approval_required": True,
        "action_mode": DEFAULT_ACTION_MODE,
        "mutation": False,
    }


def build_module_response_contracts(modules: Iterable[str]) -> list[dict[str, object]]:
    """Build response contracts for all detected module tags."""
    return [module_response_contract(module) for module in dedupe(modules)]


def render_module_response_contracts(modules: Iterable[str]) -> str:
    """Render module response contracts for a GitHub issue/PR comment."""
    contracts = build_module_response_contracts(modules)

    if not contracts:
        return ""

    blocks: list[str] = []

    for contract in contracts:
        blocks.append(
            f"#### @module:{contract['module']}\n"
            f"- STATUS: `{contract['status']}`\n"
            f"- READY_LEVEL: `{contract['ready_level']}`\n"
            f"- CAPABILITY: {contract['capability']}\n"
            f"- NEED: {contract['need']}\n"
            f"- RISK: `{contract['risk']}`\n"
            f"- RETURN_TO: `{contract['return_to']}`\n"
            f"- ACTION_MODE: `{contract['action_mode']}`\n"
            f"- MUTATION: `{str(contract['mutation']).lower()}`"
        )

    return (
        "### 🧭 Module Response Contract Preview\n"
        + "\n\n".join(blocks)
        + "\n\nBoundary: acknowledgement only. BBX19 approval is required before follow-up action."
    )
