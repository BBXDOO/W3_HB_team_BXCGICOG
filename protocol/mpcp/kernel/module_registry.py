# mpcp/kernel/module_registry.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


DEFAULT_MODULE_REGISTRY: Dict[str, List[str]] = {
    "MPCP": ["Cross-X", "Cross-L", "W3Lgu", "ECS", "W3DB", "Table-X", "Modew-dynamic", "file.void"],
    "Cross-L": ["MPCP", "Cross-X", "W3Lgu", "ECS", "Table-X", "Modew-dynamic"],
    "W3Lgu": ["MPCP", "Cross-X", "Cross-L", "Table-X"],
    "Cross-X": ["MPCP", "Cross-L", "W3Lgu", "ECS", "Table-X", "Modew-dynamic"],
    "ECS": ["MPCP", "Cross-X", "Cross-L", "W3DB"],
    "W3DB": ["MPCP", "ECS"],
    "Table-X": ["MPCP", "W3Lgu", "Cross-X"],
    "Modew-dynamic": ["MPCP", "Cross-X"],
    "file.void": ["MPCP", "Cross-X"],
}


@dataclass(frozen=True)
class ModuleRegistry:
    """Allow-list for cooperative module return / assist relations.

    The registry does not command a route.
    It only answers whether a proposed relation is allowed by the current map.
    """

    routes: Dict[str, List[str]] = field(default_factory=lambda: dict(DEFAULT_MODULE_REGISTRY))

    def can_return_to(self, source: str, target: str) -> bool:
        return target in self.routes.get(source, [])

    def can_assist(self, responsible_module: str, assist_module: str) -> bool:
        return assist_module in self.routes.get(responsible_module, [])

    def allowed_targets(self, source: str) -> List[str]:
        return list(self.routes.get(source, []))

    def explain(self, source: str, target: str) -> dict:
        return {
            "SOURCE": source,
            "TARGET": target,
            "ALLOWED": self.can_return_to(source, target),
            "ALLOWED_TARGETS": self.allowed_targets(source),
        }


DEFAULT_REGISTRY = ModuleRegistry()


def can_return_to(source: str, target: str, *, registry: Optional[ModuleRegistry] = None) -> bool:
    active = registry or DEFAULT_REGISTRY
    return active.can_return_to(source, target)


def can_assist(responsible_module: str, assist_module: str, *, registry: Optional[ModuleRegistry] = None) -> bool:
    active = registry or DEFAULT_REGISTRY
    return active.can_assist(responsible_module, assist_module)
