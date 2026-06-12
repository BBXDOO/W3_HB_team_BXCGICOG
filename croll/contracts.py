"""Lightweight contract checks for CROLL artifacts.

The JSON Schema files in :mod:`croll.schema` are the portable contract documents.
These checks enforce the safety invariants needed by the dependency-free runtime.
They deliberately do not implement a general JSON Schema engine.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Callable, Dict

CONTRACT_VERSION = "1.0"
REQUIRED_SAFETY_FALSE = (
    "modew_execution_allowed",
    "truth_mutation_allowed",
    "repo_write_allowed",
    "direct_merge_allowed",
)


class ContractError(ValueError):
    """Raised when a CROLL artifact violates its declared contract."""


def _mapping(value: Any, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ContractError(f"{field} must be an object")
    return value


def _required(data: Mapping[str, Any], *fields: str) -> None:
    missing = [field for field in fields if field not in data]
    if missing:
        raise ContractError(f"missing required fields: {', '.join(missing)}")


def _string_list(value: Any, field: str, *, nonempty: bool = False) -> None:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise ContractError(f"{field} must be an array of strings")
    if nonempty and not value:
        raise ContractError(f"{field} must not be empty")
    if any(not isinstance(item, str) or not item for item in value):
        raise ContractError(f"{field} must contain non-empty strings")


def _version(data: Mapping[str, Any]) -> None:
    if data.get("contract_version") != CONTRACT_VERSION:
        raise ContractError(f"contract_version must be {CONTRACT_VERSION!r}")


def validate_workset(value: Any) -> Dict[str, Any]:
    """Validate a Table-X workset and return a plain dictionary copy."""
    data = _mapping(value, "workset")
    _required(
        data,
        "contract_version",
        "px",
        "rytm",
        "work_type",
        "modew_style",
        "boundary",
        "mutated",
        "review",
    )
    _version(data)
    if data["mutated"] is not False:
        raise ContractError("workset.mutated must be false")
    if data["review"] is not True:
        raise ContractError("workset.review must be true")
    px = data["px"]
    if px is not None:
        if not isinstance(px, list) or len(px) != 2:
            raise ContractError("workset.px must be null or a two-item array")
        if any(isinstance(item, bool) or not isinstance(item, int) or item < 1 for item in px):
            raise ContractError("workset.px coordinates must be positive integers")
    for field in ("rytm", "work_type", "modew_style", "boundary"):
        if not isinstance(data[field], str) or not data[field]:
            raise ContractError(f"workset.{field} must be a non-empty string")
    for field in ("deny", "return_contract"):
        if field in data:
            _string_list(data[field], f"workset.{field}")
    return dict(data)


def validate_dispatch_plan(value: Any) -> Dict[str, Any]:
    """Validate a planner-only dispatch plan and its nested workset."""
    data = _mapping(value, "dispatch_plan")
    _required(
        data,
        "contract_version",
        "state",
        "reason",
        "scope",
        "action",
        "execution_allowed",
        "mutated",
        "review",
        "workset",
        "safety",
    )
    _version(data)
    if data["scope"] != "CROSS_L_ONLY":
        raise ContractError("dispatch_plan.scope must be 'CROSS_L_ONLY'")
    for field in ("execution_allowed", "mutated"):
        if data[field] is not False:
            raise ContractError(f"dispatch_plan.{field} must be false")
    if data["review"] is not True:
        raise ContractError("dispatch_plan.review must be true")
    safety = _mapping(data["safety"], "dispatch_plan.safety")
    if safety.get("planner_only") is not True:
        raise ContractError("dispatch_plan.safety.planner_only must be true")
    for field in REQUIRED_SAFETY_FALSE:
        if safety.get(field) is not False:
            raise ContractError(f"dispatch_plan.safety.{field} must be false")
    validate_workset(data["workset"])
    return dict(data)


def validate_boundary_manifest(value: Any) -> Dict[str, Any]:
    """Validate a lightweight W3-network boundary declaration."""
    data = _mapping(value, "boundary_manifest")
    _required(
        data,
        "contract_version",
        "kind",
        "ecosystem",
        "network_scope",
        "owner",
        "purpose",
        "boundary",
        "review",
    )
    _version(data)
    if data["kind"] != "croll-boundary":
        raise ContractError("boundary_manifest.kind must be 'croll-boundary'")
    if data["ecosystem"] != "W3":
        raise ContractError("boundary_manifest.ecosystem must be 'W3'")
    if data["network_scope"] not in ("w3-internal", "w3-partner"):
        raise ContractError("boundary_manifest.network_scope must be W3-scoped")
    for field in ("owner", "purpose"):
        if not isinstance(data[field], str) or not data[field].strip():
            raise ContractError(f"boundary_manifest.{field} must be a non-empty string")
    boundary = _mapping(data["boundary"], "boundary_manifest.boundary")
    _required(boundary, "mode", "allow", "deny")
    if boundary["mode"] not in ("planner_only", "observe", "record_only"):
        raise ContractError("boundary_manifest.boundary.mode is not allowed")
    _string_list(boundary["allow"], "boundary_manifest.boundary.allow", nonempty=True)
    _string_list(boundary["deny"], "boundary_manifest.boundary.deny", nonempty=True)
    required_denies = {"truth_mutation", "direct_merge", "unreviewed_execution"}
    missing_denies = required_denies.difference(boundary["deny"])
    if missing_denies:
        raise ContractError(
            "boundary_manifest.boundary.deny must include: "
            + ", ".join(sorted(missing_denies))
        )
    review = _mapping(data["review"], "boundary_manifest.review")
    _required(review, "required", "on_uncertainty")
    if review["required"] is not True or review["on_uncertainty"] is not True:
        raise ContractError("boundary_manifest review safeguards must be true")
    return dict(data)


VALIDATORS: Dict[str, Callable[[Any], Dict[str, Any]]] = {
    "boundary": validate_boundary_manifest,
    "plan": validate_dispatch_plan,
    "workset": validate_workset,
}


def validate_artifact(kind: str, value: Any) -> Dict[str, Any]:
    """Validate an artifact by stable CLI kind name."""
    try:
        validator = VALIDATORS[kind]
    except KeyError as exc:
        raise ContractError(f"unknown artifact kind: {kind}") from exc
    return validator(value)
