"""Semantic pressure analyzer for overloaded concepts and governance terms."""

from __future__ import annotations

from hospitication.analysis._helpers import clamp, doc_files, top_counts
from hospitication.core.types import MetricScore, ObservationSnapshot

SEMANTIC_TERMS = (
    "truth",
    "governance",
    "memory",
    "replay",
    "signal",
    "recovery",
    "protocol",
    "mpcp",
    "outcome",
    "ledger",
)


def analyze_semantic_pressure(snapshot: ObservationSnapshot) -> MetricScore:
    docs = doc_files(snapshot)
    marker_hits: list[str] = []
    for file in snapshot.files:
        marker_hits.extend(marker.lower() for marker in file.markers if marker.lower() in SEMANTIC_TERMS)
    density = len(marker_hits) / max(1, len(docs) + len(snapshot.files) * 0.15)
    score = clamp(density / 5.0)
    return MetricScore(
        name="semantic_pressure",
        score=score,
        summary="Semantic pressure from repeated W3 governance/replay concepts.",
        evidence={
            "semantic_marker_hits": len(marker_hits),
            "top_terms": top_counts(marker_hits, limit=8),
            "doc_files": len(docs),
        },
    )
