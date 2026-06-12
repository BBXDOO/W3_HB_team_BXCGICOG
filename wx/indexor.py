"""Planner-only BOX Indexor (Binder-style librarian)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional, Union

from .engine_index import find_templates


def suggest_references(
    *,
    px: Any = None,
    work_type: Optional[str] = None,
    rytm: Optional[str] = None,
    registry_path: Optional[Union[str, Path]] = None,
) -> dict[str, Any]:
    """Suggest registered references without copying or modifying any file."""
    matches = find_templates(
        px=px,
        work_type=work_type,
        rytm=rytm,
        registry_path=registry_path,
    )
    suggestions = [
        {
            "template_id": item["template_id"],
            "name": item["name"],
            "path": item["path"],
            "version": item["version"],
            "boundary": item["boundary"],
            "deny": list(item["deny"]),
            "external_ref": item.get("external_ref"),
        }
        for item in matches
    ]
    return {
        "contract_version": "1.0",
        "state": "suggested" if suggestions else "not_found",
        "planner_only": True,
        "execution_allowed": False,
        "mutated": False,
        "copy_allowed_by_runtime": False,
        "human_review_required": True,
        "suggestions": suggestions,
    }
