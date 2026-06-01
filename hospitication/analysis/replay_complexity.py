"""Replay complexity analyzer for event, outcome, ledger, and replay surfaces."""

from __future__ import annotations

from hospitication.analysis._helpers import clamp
from hospitication.core.types import MetricScore, ObservationSnapshot

REPLAY_TERMS = ("replay", "outcome", "ledger", "event", "trace", "checkpoint", "rollback")


def analyze_replay_complexity(snapshot: ObservationSnapshot) -> MetricScore:
    paths = [file.path for file in snapshot.files]
    replay_paths = [path for path in paths if any(term in path.lower() for term in REPLAY_TERMS)]
    marker_hits = sum(
        1
        for file in snapshot.files
        for marker in file.markers
        if marker.lower() in REPLAY_TERMS
    )
    score = clamp((len(replay_paths) / max(1, len(snapshot.files))) * 3.0 + marker_hits / 60.0)
    return MetricScore(
        name="replay_complexity",
        score=score,
        summary="Replay complexity from event/outcome/ledger/checkpoint surfaces.",
        evidence={
            "replay_related_files": tuple(sorted(replay_paths)[:20]),
            "replay_related_file_count": len(replay_paths),
            "replay_marker_hits": marker_hits,
        },
    )
