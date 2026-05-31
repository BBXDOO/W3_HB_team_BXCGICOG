"""Load and validate W3 ecosystem configuration.

The config package is a lightweight orientation layer. It does not replace
module registries, W3DB, W3Lgu, or governance documents; it links them into one
runtime map for Cross-X coordination.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

CONFIG_ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class W3ConfigBundle:
    environment: Mapping[str, Any]
    ecosystem: Mapping[str, Any]
    cross_system: Mapping[str, Any]
    paths: Mapping[str, Any]

    def component_path(self, name: str) -> str:
        return str(self.paths["paths"][name])

    def to_dict(self) -> dict[str, Any]:
        return {
            "environment": dict(self.environment),
            "ecosystem": dict(self.ecosystem),
            "cross_system": dict(self.cross_system),
            "paths": dict(self.paths),
        }


def _load_json(path: Path) -> Mapping[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_w3_config(root: str | Path = CONFIG_ROOT) -> W3ConfigBundle:
    root_path = Path(root)
    bundle = W3ConfigBundle(
        environment=_load_json(root_path / "environment.json"),
        ecosystem=_load_json(root_path / "ecosystem.json"),
        cross_system=_load_json(root_path / "cross_system.json"),
        paths=_load_json(root_path / "paths.json"),
    )
    errors = validate_w3_config(bundle)
    if errors:
        raise ValueError("Invalid W3 config: " + "; ".join(errors))
    return bundle


def validate_w3_config(bundle: W3ConfigBundle) -> list[str]:
    errors: list[str] = []
    env = bundle.environment
    ecosystem = bundle.ecosystem
    cross = bundle.cross_system
    paths = bundle.paths.get("paths", {})

    if env.get("schema_version") != "W3-RUNTIME-0.3":
        errors.append("environment.schema_version must be W3-RUNTIME-0.3")
    compatibility = env.get("compatibility", {})
    for key in ("W3Lgu", "PX", "W3DB_append_flow", "EP_SIGNAL", "Hospitication", "W3_API", "Codex"):
        if compatibility.get(key) is not True:
            errors.append(f"environment.compatibility.{key} must be true")
    if compatibility.get("iget") != "v8.0":
        errors.append("environment.compatibility.iget must be v8.0")

    components = ecosystem.get("components", {})
    for required in ("Codex", "Hospitication", "W3Lgu", "PX", "W3DB_APPEND", "W3-API", "EP_SIGNAL", "IGET"):
        if required not in components:
            errors.append(f"ecosystem.components.{required} is required")

    cross_x = cross.get("cross_x", {})
    if cross_x.get("truth_mutation") is not False:
        errors.append("cross_system.cross_x.truth_mutation must be false")
    if cross_x.get("append_only") is not True:
        errors.append("cross_system.cross_x.append_only must be true")
    if cross_x.get("requires_human_review") is not True:
        errors.append("cross_system.cross_x.requires_human_review must be true")
    if cross_x.get("requires_governance_gate") is not True:
        errors.append("cross_system.cross_x.requires_governance_gate must be true")

    for required_path in ("w3_api", "w3lgu", "px", "w3db_append_flow", "hospitication", "iget", "codex"):
        if required_path not in paths:
            errors.append(f"paths.{required_path} is required")

    return sorted(errors)
