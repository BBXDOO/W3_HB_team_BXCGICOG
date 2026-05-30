"""Dependency fatigue analyzer for import breadth and dependency concentration."""

from __future__ import annotations

from hospitication.analysis._helpers import clamp, code_files, top_counts
from hospitication.core.types import MetricScore, ObservationSnapshot


def analyze_dependency_fatigue(snapshot: ObservationSnapshot) -> MetricScore:
    code = code_files(snapshot)
    imports: list[str] = []
    for file in code:
        imports.extend(file.imports)
    unique_imports = set(imports)
    breadth = len(unique_imports) / max(1, len(code))
    concentration = max(top_counts(imports, limit=1).values(), default=0) / max(1, len(imports))
    score = clamp((breadth / 8.0) + (concentration * 0.25))
    return MetricScore(
        name="dependency_fatigue",
        score=score,
        summary="Dependency fatigue from import breadth and repeated coupling points.",
        evidence={
            "code_files": len(code),
            "unique_imports": len(unique_imports),
            "import_mentions": len(imports),
            "top_imports": top_counts(imports, limit=8),
        },
    )
