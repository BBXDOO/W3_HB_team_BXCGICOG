"""Read-only Engine-Index for BOX template discovery.

The module resolves paths relative to this package, not the current working
directory. It reads registry metadata and returns detached dictionary copies;
it never writes, copies, executes, or imports referenced templates.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Optional, Union

BOX_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = BOX_ROOT.parent
DEFAULT_TEMPLATE_REGISTRY = BOX_ROOT / "registry" / "template_registry.json"
_REQUIRED_TEMPLATE_FIELDS = {
    "template_id",
    "name",
    "path",
    "version",
    "owner",
    "status",
    "work_type",
    "rytm",
    "px",
    "boundary",
    "deny",
}
_PX_PATTERN = re.compile(r"^(?:PX\s*:\s*\[\s*)?(\d+)\s*,\s*(\d+)(?:\s*\])?$", re.IGNORECASE)


class BoxRegistryError(ValueError):
    """Raised when BOX registry metadata is unreadable or unsafe."""


def _load_json(path: Path) -> Mapping[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise BoxRegistryError(f"cannot read BOX registry {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise BoxRegistryError(f"invalid BOX registry JSON at {path}: {exc.msg}") from exc
    if not isinstance(value, Mapping):
        raise BoxRegistryError("BOX registry root must be an object")
    return value


def _safe_repository_path(value: Any, *, template_id: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise BoxRegistryError(f"{template_id}.path must be a non-empty string")
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        raise BoxRegistryError(f"{template_id}.path must be repository-relative")
    resolved = (REPOSITORY_ROOT / relative).resolve()
    try:
        resolved.relative_to(REPOSITORY_ROOT)
    except ValueError as exc:
        raise BoxRegistryError(f"{template_id}.path escapes the repository") from exc
    if not resolved.is_file():
        raise BoxRegistryError(f"registered BOX source does not exist: {value}")
    return relative.as_posix()



def _front_matter(path: Path, *, template_id: str) -> dict[str, str]:
    """Read the small required metadata subset without adding a YAML dependency."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise BoxRegistryError(f"{template_id} source must start with YAML front matter")
    metadata: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, separator, value = line.partition(":")
        if not separator or not key.strip() or not value.strip():
            raise BoxRegistryError(f"{template_id} has unsupported front matter")
        metadata[key.strip()] = value.strip()
    else:
        raise BoxRegistryError(f"{template_id} front matter is not closed")
    required = {"template_id", "version", "scope", "boundary", "deny", "owner", "status", "created_at"}
    missing = sorted(required.difference(metadata))
    if missing:
        raise BoxRegistryError(f"{template_id} front matter missing: {', '.join(missing)}")
    return metadata


def _string_list(value: Any, *, field: str, nonempty: bool = False) -> list[str]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise BoxRegistryError(f"{field} must be an array of strings")
    result = list(value)
    if nonempty and not result:
        raise BoxRegistryError(f"{field} must not be empty")
    if any(not isinstance(item, str) or not item.strip() for item in result):
        raise BoxRegistryError(f"{field} must contain non-empty strings")
    return result


def normalize_px(px: Any) -> Optional[str]:
    """Normalize supported PX forms to ``"row,column"`` without executing CROLL."""
    if isinstance(px, Sequence) and not isinstance(px, (str, bytes)):
        if len(px) != 2 or any(isinstance(item, bool) or not isinstance(item, int) for item in px):
            return None
        row, column = px
    elif isinstance(px, str):
        match = _PX_PATTERN.fullmatch(px.strip())
        if not match:
            return None
        row, column = (int(match.group(1)), int(match.group(2)))
    else:
        return None
    if row < 1 or column < 1:
        return None
    return f"{row},{column}"


def load_template_registry(path: Optional[Union[str, Path]] = None) -> dict[str, Any]:
    """Load and validate the BOX template registry.

    The returned object is a new dictionary so callers cannot mutate the loaded
    source of truth in memory and mistake that for a repository update.
    """
    registry_path = DEFAULT_TEMPLATE_REGISTRY if path is None else Path(path)
    data = _load_json(registry_path)
    if data.get("version") != "1.0":
        raise BoxRegistryError("template registry version must be '1.0'")
    templates = data.get("templates")
    if not isinstance(templates, list):
        raise BoxRegistryError("template registry templates must be an array")

    seen: set[str] = set()
    validated: list[dict[str, Any]] = []
    for index, raw in enumerate(templates):
        if not isinstance(raw, Mapping):
            raise BoxRegistryError(f"templates[{index}] must be an object")
        missing = sorted(_REQUIRED_TEMPLATE_FIELDS.difference(raw))
        if missing:
            raise BoxRegistryError(f"templates[{index}] missing fields: {', '.join(missing)}")
        template_id = raw["template_id"]
        if not isinstance(template_id, str) or not template_id.strip():
            raise BoxRegistryError(f"templates[{index}].template_id must be a non-empty string")
        if template_id in seen:
            raise BoxRegistryError(f"duplicate template_id: {template_id}")
        seen.add(template_id)

        item = dict(raw)
        item["path"] = _safe_repository_path(item["path"], template_id=template_id)
        metadata = _front_matter(REPOSITORY_ROOT / item["path"], template_id=template_id)
        for field in ("template_id", "version", "owner", "status", "boundary"):
            if str(item[field]) != metadata[field]:
                raise BoxRegistryError(f"{template_id}.{field} does not match source front matter")
        item["px"] = _string_list(item["px"], field=f"{template_id}.px", nonempty=True)
        normalized_px = [normalize_px(value) for value in item["px"]]
        if any(value is None for value in normalized_px):
            raise BoxRegistryError(f"{template_id}.px contains an invalid coordinate")
        item["px"] = normalized_px
        item["deny"] = _string_list(item["deny"], field=f"{template_id}.deny", nonempty=True)
        if item["status"] not in {"active", "draft", "deprecated"}:
            raise BoxRegistryError(f"{template_id}.status is not supported")
        if item.get("external_ref") is not None and not isinstance(item["external_ref"], str):
            raise BoxRegistryError(f"{template_id}.external_ref must be a string or null")
        validated.append(item)

    return {
        "version": data["version"],
        "updated_at": data.get("updated_at"),
        "templates": validated,
    }


def find_templates(
    *,
    px: Any = None,
    work_type: Optional[str] = None,
    rytm: Optional[str] = None,
    status: str = "active",
    registry_path: Optional[Union[str, Path]] = None,
) -> list[dict[str, Any]]:
    """Return deterministic template matches for the supplied reference fields."""
    normalized_px = normalize_px(px) if px is not None else None
    if px is not None and normalized_px is None:
        return []
    work_type_key = work_type.strip().upper() if isinstance(work_type, str) else None
    rytm_key = rytm.strip().upper() if isinstance(rytm, str) else None

    matches = []
    for template in load_template_registry(registry_path)["templates"]:
        if status and template.get("status") != status:
            continue
        if normalized_px is not None and normalized_px not in template.get("px", []):
            continue
        if work_type_key is not None and str(template.get("work_type", "")).upper() != work_type_key:
            continue
        if rytm_key is not None and str(template.get("rytm", "")).upper() != rytm_key:
            continue
        matches.append(dict(template))
    return matches


def search_by_px(px: Any, *, registry_path: Optional[Union[str, Path]] = None) -> Optional[dict[str, Any]]:
    matches = find_templates(px=px, registry_path=registry_path)
    return matches[0] if matches else None


def search_by_work_type(work_type: str, *, registry_path: Optional[Union[str, Path]] = None) -> list[dict[str, Any]]:
    return find_templates(work_type=work_type, registry_path=registry_path)


def search_by_rytm(rytm: str, *, registry_path: Optional[Union[str, Path]] = None) -> list[dict[str, Any]]:
    return find_templates(rytm=rytm, registry_path=registry_path)
