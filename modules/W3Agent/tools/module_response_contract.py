"""Module response contract helpers for W3Agent.

Purpose:
- Build report-only response previews for IGET @module:<name> dispatch tags.
- Describe what a module can review, what it needs, and its current readiness.
- Keep BBX19 approval as the boundary before any follow-up action.

This file does not execute modules.
This file does not mutate repository content.
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
    "Codex": {
        "status": "can_review_code_patch",
        "ready_level": "2/5",
        "capability": "code patch inspection and implementation support",
        "need": "target files, expected behavior, tests, and no-mutation boundary",
        "risk": "medium",
    },
    "Copilot-GM": {
        "status": "can_review_code_assist",
        "ready_level": "2/5",
        "capability": "code assist, patch suggestion, and implementation comparison",
        "need": "target scope, expected output, and review boundary",
        "risk": "medium",
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


def normalize_module_name(module: str) -> str:
    """Normalize common module spelling from IGET issue text."""
    raw = str(module).strip()

    aliases = {
        "codex": "Codex",
        "copilot-gm": "Copilot-GM",
        "copilot_gm": "Copilot-GM",
        "copilotgm": "Copilot-GM",
        "w3api": "W3-API",
        "w3-api": "W3-API",
        "ep-signal": "EP_SIGNAL",
        "ep_signal": "EP_SIGNAL",
        "lrc2": "LRC2",
        "redr": "REDR",
        "psp2": "PSP2",
        "w3lgu": "W3Lgu",
        "iget": "IGET",
        "mpcp": "MPCP",
        "w3db": "W3DB",
        "dtml": "DTML",
        "croll": "CROLL",
    }

    return aliases.get(raw.lower(), raw)


def module_response_contract(module: str) -> dict[str, object]:
    """Return one report-only response contract for a dispatched module tag."""
    normalized = normalize_module_name(module)
    profile = MODULE_RESPONSE_PROFILES.get(normalized, DEFAULT_MODULE_RESPONSE)

    return {
        "module": normalized,
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
    normalized = [normalize_module_name(module) for module in modules]
    return [module_response_contract(module) for module in dedupe(normalized)]


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
