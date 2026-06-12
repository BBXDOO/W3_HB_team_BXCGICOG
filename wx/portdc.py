"""Read-only PortDC export boundary for registered BOX templates."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .engine_index import REPOSITORY_ROOT, load_template_registry


class BoxExportError(LookupError):
    """Raised when a requested BOX reference is not registered."""


def export_registered_template(template_id: str) -> dict[str, Any]:
    """Return a registered source as data; never write or copy it to a target."""
    templates = load_template_registry()["templates"]
    template = next((item for item in templates if item["template_id"] == template_id), None)
    if template is None:
        raise BoxExportError(f"unknown BOX template_id: {template_id}")
    path = (REPOSITORY_ROOT / template["path"]).resolve()
    return {
        "contract_version": "1.0",
        "template_id": template_id,
        "source_path": template["path"],
        "content": path.read_text(encoding="utf-8"),
        "execution_allowed": False,
        "mutated": False,
        "write_performed": False,
        "human_copy_required": True,
    }
