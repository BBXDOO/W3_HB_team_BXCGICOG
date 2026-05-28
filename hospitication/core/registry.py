"""Analyzer registry used by CLI and production orchestration."""

from __future__ import annotations

from collections.abc import Callable

from hospitication.core.types import MetricScore, ObservationSnapshot

Analyzer = Callable[[ObservationSnapshot], MetricScore]


class AnalyzerRegistry:
    """Small deterministic registry; avoids dynamic imports and hidden mutation."""

    def __init__(self) -> None:
        self._items: dict[str, Analyzer] = {}

    def register(self, name: str, analyzer: Analyzer) -> None:
        if not name:
            raise ValueError("Analyzer name is required")
        self._items[name] = analyzer

    def analyzers(self) -> tuple[Analyzer, ...]:
        return tuple(self._items[name] for name in sorted(self._items))

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._items))


def default_registry() -> AnalyzerRegistry:
    from hospitication.analysis.cognitive_cost import analyze_cognitive_cost
    from hospitication.analysis.dependency_fatigue import analyze_dependency_fatigue
    from hospitication.analysis.recovery_resistance import analyze_recovery_resistance
    from hospitication.analysis.replay_complexity import analyze_replay_complexity
    from hospitication.analysis.semantic_pressure import analyze_semantic_pressure

    registry = AnalyzerRegistry()
    registry.register("cognitive_cost", analyze_cognitive_cost)
    registry.register("dependency_fatigue", analyze_dependency_fatigue)
    registry.register("recovery_resistance", analyze_recovery_resistance)
    registry.register("replay_complexity", analyze_replay_complexity)
    registry.register("semantic_pressure", analyze_semantic_pressure)
    return registry
