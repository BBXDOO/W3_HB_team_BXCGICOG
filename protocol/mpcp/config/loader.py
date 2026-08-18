"""Load and validate MPCP configuration without external dependencies."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import json
from pathlib import Path
from typing import Any, Mapping


DEFAULT_CONFIG_PATH = Path(__file__).with_name("default.json")


@dataclass(frozen=True)
class MPCPConfig:
    """Validated immutable view of the MPCP runtime configuration."""

    source: Path
    data: Mapping[str, Any]

    @property
    def tag_families(self) -> frozenset[str]:
        return frozenset(str(item).upper() for item in self.data["tag_families"])

    @property
    def data_formats(self) -> frozenset[str]:
        return frozenset(str(item).upper() for item in self.data["data_formats"])

    @property
    def language_runtime(self) -> Mapping[str, tuple[str, ...]]:
        return {
            str(key).upper(): tuple(str(command) for command in value)
            for key, value in self.data["language_runtime"].items()
        }

    @property
    def libraries(self) -> Mapping[str, tuple[str, ...]]:
        return {
            str(group): tuple(str(item) for item in values)
            for group, values in self.data["libraries"].items()
        }

    @property
    def allowed_variable_names(self) -> tuple[str, ...]:
        return tuple(self.data["environment"]["allowed_variable_names"])


def _validate(raw: Any) -> Mapping[str, Any]:
    if not isinstance(raw, dict):
        raise ValueError("MPCP_CONFIG:ROOT_MUST_BE_OBJECT")
    if raw.get("schema") != "mpcp.config.1" or raw.get("system") != "mpcp":
        raise ValueError("MPCP_CONFIG:IDENTITY_INVALID")
    for key in ("environment", "libraries", "language_runtime", "language_aliases", "data_formats", "tag_families"):
        if key not in raw:
            raise ValueError(f"MPCP_CONFIG:MISSING:{key}")
    if not isinstance(raw["environment"], dict):
        raise ValueError("MPCP_CONFIG:ENVIRONMENT_MUST_BE_OBJECT")
    for group in ("core", "bridge", "optional"):
        values = raw["libraries"].get(group)
        if not isinstance(values, list) or not all(isinstance(item, str) and item for item in values):
            raise ValueError(f"MPCP_CONFIG:LIBRARY_GROUP_INVALID:{group}")
    if not isinstance(raw["language_runtime"], dict):
        raise ValueError("MPCP_CONFIG:LANGUAGE_RUNTIME_MUST_BE_OBJECT")
    return raw


@lru_cache(maxsize=8)
def load_config(path: str | Path | None = None) -> MPCPConfig:
    """Load one configuration file; callers may supply a platform profile."""

    source = Path(path).expanduser().resolve() if path else DEFAULT_CONFIG_PATH.resolve()
    with source.open("r", encoding="utf-8") as handle:
        raw = json.load(handle)
    return MPCPConfig(source=source, data=_validate(raw))
