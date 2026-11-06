"""Shared pure helpers for Hospitication analyzers."""

from __future__ import annotations

from collections import Counter

from hospitication.core.config import CODE_EXTENSIONS, CONFIG_EXTENSIONS, DOC_EXTENSIONS
from hospitication.core.types import FileObservation, ObservationSnapshot


def clamp(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 4)


def files_by_suffix(snapshot: ObservationSnapshot, suffixes: tuple[str, ...]) -> tuple[FileObservation, ...]:
    return tuple(file for file in snapshot.files if file.suffix in suffixes)


def code_files(snapshot: ObservationSnapshot) -> tuple[FileObservation, ...]:
    return files_by_suffix(snapshot, snapshot.scope.code_extensions if snapshot.scope else CODE_EXTENSIONS)


def doc_files(snapshot: ObservationSnapshot) -> tuple[FileObservation, ...]:
    return files_by_suffix(snapshot, snapshot.scope.doc_extensions if snapshot.scope else DOC_EXTENSIONS)


def config_files(snapshot: ObservationSnapshot) -> tuple[FileObservation, ...]:
    return files_by_suffix(snapshot, snapshot.scope.config_extensions if snapshot.scope else CONFIG_EXTENSIONS)


def top_counts(values: list[str], limit: int = 10) -> dict[str, int]:
    counter = Counter(values)
    return dict(sorted(counter.most_common(limit), key=lambda item: (-item[1], item[0])))
