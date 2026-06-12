"""BOX Knowledge Infrastructure public reference API.

BOX is planner-only: it locates and exports references but never executes,
copies, writes, or mutates repository content.
"""

from .engine_index import (
    BoxRegistryError,
    find_templates,
    load_template_registry,
    search_by_px,
    search_by_rytm,
    search_by_work_type,
)
from .indexor import suggest_references
from .portdc import export_registered_template

__all__ = [
    "BoxRegistryError",
    "export_registered_template",
    "find_templates",
    "load_template_registry",
    "search_by_px",
    "search_by_rytm",
    "search_by_work_type",
    "suggest_references",
]

__version__ = "1.0.0"
