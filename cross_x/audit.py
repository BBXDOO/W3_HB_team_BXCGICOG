"""Cross-X configuration audit helpers.

The audit reports integration readiness only.  It never imports, starts, or
executes a configured subsystem.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from config.loader import W3ConfigBundle


def audit_cross_systems(
    config: W3ConfigBundle,
    *,
    repository_root: str | Path | None = None,
) -> dict[str, Any]:
    """Audit chain membership, contracts, status, and repository paths."""

    root = (
        Path(repository_root) if repository_root is not None else Path(__file__).resolve().parent.parent
    ).resolve()
    components: Mapping[str, Any] = config.ecosystem.get("components", {})
    contracts: Mapping[str, Any] = config.cross_system.get("contracts", {})
    chain = tuple(config.cross_system.get("chain", ()))
    records = []
    issues = []

    for system in chain:
        component = components.get(system)
        system_issues = []
        if not isinstance(component, Mapping):
            system_issues.append("component_not_registered")
            component = {}
        path_value = component.get("path")
        path_exists = isinstance(path_value, str) and bool(path_value) and (root / path_value).exists()
        path_exists = False
        if isinstance(path_value, str) and path_value:
            path_obj = Path(path_value)
            candidate = (root / path_obj).resolve()
            path_exists = (
                not path_obj.is_absolute()
                and candidate.is_relative_to(root)
                and candidate.exists()
            )
        if not path_exists:
            system_issues.append("component_path_missing")
        if system not in contracts:
            system_issues.append("contract_missing")

        configured_state = str(component.get("status", "active")).strip().lower()
        active = configured_state in {"active", "ready", "enabled"}
        if not active:
            system_issues.append("system_inactive")

        records.append(
            {
                "system": system,
                "status": "ready" if not system_issues else "attention",
                "configured_state": configured_state,
                "active": active,
                "path": path_value,
                "path_exists": path_exists,
                "contract": contracts.get(system),
                "issues": system_issues,
            }
        )
        issues.extend(f"{system}:{issue}" for issue in system_issues)

    return {
        "status": "ready" if not issues else "attention",
        "mutated": False,
        "checked": len(records),
        "issues": issues,
        "systems": records,
    }
