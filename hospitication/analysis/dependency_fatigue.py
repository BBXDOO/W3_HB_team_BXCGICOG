"""Dependency fatigue analyzer for import breadth and dependency concentration."""

from __future__ import annotations

from hospitication.analysis._helpers import clamp, code_files, top_counts
from hospitication.core.types import MetricScore, ObservationSnapshot


def analyze_dependency_fatigue(snapshot: ObservationSnapshot) -> MetricScore:
    all_code = code_files(snapshot)
    code = tuple(file for file in all_code if file.suffix == '.py')
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
        summary="Python import breadth and repeated import roots; other languages are unmeasured.",
        evidence={
            "code_files": len(code),
            "unmeasured_code_files": len(all_code) - len(code),
            "import_scope": "python_only",
            "unique_imports": len(unique_imports),
            "import_mentions": len(imports),
            "top_imports": top_counts(imports, limit=8),
        },
    )
