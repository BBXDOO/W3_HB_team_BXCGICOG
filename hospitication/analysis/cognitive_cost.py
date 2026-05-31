"""Cognitive cost analyzer for repository breadth and file size distribution."""

from __future__ import annotations

from hospitication.analysis._helpers import clamp, config_files
from hospitication.core.types import MetricScore, ObservationSnapshot


def analyze_cognitive_cost(snapshot: ObservationSnapshot) -> MetricScore:
    file_count = len(snapshot.files)
    total_lines = snapshot.total_lines
    configs = config_files(snapshot)
    average_lines = total_lines / max(1, file_count)
    score = clamp((file_count / 900.0) + (average_lines / 450.0) + (len(configs) / 250.0))
    return MetricScore(
        name="cognitive_cost",
        score=score,
        summary="Cognitive cost from file count, average size, and configuration breadth.",
        evidence={
            "file_count": file_count,
            "total_lines": total_lines,
            "average_lines_per_file": round(average_lines, 2),
            "config_files": len(configs),
        },
    )
