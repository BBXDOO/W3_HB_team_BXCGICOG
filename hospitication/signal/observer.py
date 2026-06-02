"""Read-only repository observer for Hospitication."""

from __future__ import annotations

import ast
from pathlib import Path

from hospitication.core.config import HospiticationConfig
from hospitication.core.types import FileObservation, ObservationSnapshot

MARKER_WORDS = (
    "TODO",
    "FIXME",
    "HACK",
    "XXX",
    "deprecated",
    "rollback",
    "replay",
    "governance",
    "memory",
    "mpcp",
)


def observe_repository(
    repo_root: str | Path,
    config: HospiticationConfig | None = None,
) -> ObservationSnapshot:
    """Return an immutable structural snapshot without mutating the repository."""

    cfg = config or HospiticationConfig()
    root = Path(repo_root).resolve()
    observations: list[FileObservation] = []

    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        relative_parts = path.relative_to(root).parts
        if any(part in cfg.ignored_dirs for part in relative_parts):
            continue
        if path.stat().st_size > cfg.max_file_bytes:
            continue
        observations.append(_observe_file(root, path, cfg))

    return ObservationSnapshot(
        repo_root=str(root),
        files=tuple(observations),
        observed_at=cfg.deterministic_timestamp,
        ignored_dirs=tuple(sorted(cfg.ignored_dirs)),
    )


def _observe_file(
    root: Path,
    path: Path,
    config: HospiticationConfig,
) -> FileObservation:
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="ignore")
    suffix = path.suffix.lower()
    imports: tuple[str, ...] = ()
    if suffix == ".py":
        imports = _python_imports(text)

    markers = tuple(sorted(marker for marker in MARKER_WORDS if marker.lower() in text.lower()))
    return FileObservation(
        path=path.relative_to(root).as_posix(),
        suffix=suffix,
        line_count=len(text.splitlines()),
        byte_count=len(raw),
        imports=imports,
        markers=markers,
    )


def _python_imports(text: str) -> tuple[str, ...]:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return ()
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    return tuple(sorted(imports))
