"""Recovery resistance analyzer for large files and sparse tests/docs counterweight."""

from __future__ import annotations

from hospitication.analysis._helpers import clamp, code_files, doc_files
from hospitication.core.types import MetricScore, ObservationSnapshot


def analyze_recovery_resistance(snapshot: ObservationSnapshot) -> MetricScore:
    code = code_files(snapshot)
    docs = doc_files(snapshot)
    test_files = tuple(file for file in snapshot.files if "test" in file.path.lower())
    large_files = tuple(file for file in snapshot.files if file.line_count >= 300)
    test_ratio = len(test_files) / max(1, len(code))
    doc_ratio = len(docs) / max(1, len(code))
    large_pressure = len(large_files) / max(1, len(snapshot.files))
    missing_counterweight = max(0.0, 0.6 - min(0.6, test_ratio + doc_ratio * 0.5))
    score = clamp(large_pressure * 2.0 + missing_counterweight)
    return MetricScore(
        name="recovery_resistance",
        score=score,
        summary="Recovery resistance from large surfaces with limited tests/docs counterweight.",
        evidence={
            "large_files": tuple(file.path for file in sorted(large_files, key=lambda item: (-item.line_count, item.path))[:10]),
            "large_file_count": len(large_files),
            "test_files": len(test_files),
            "doc_files": len(docs),
            "code_files": len(code),
        },
    )
