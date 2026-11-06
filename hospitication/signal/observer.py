"""Read-only repository observer for Hospitication."""

from __future__ import annotations

import ast
from collections import Counter
import os
from pathlib import Path, PurePosixPath

from hospitication.core.config import HospiticationConfig, TEXT_EXTENSIONS, TEXT_FILENAMES, VERSION
from hospitication.core.types import FileObservation, ObservationScope, ObservationSnapshot

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
    "truth",
    "signal",
    "recovery",
    "protocol",
    "outcome",
    "ledger",
    "event",
    "trace",
    "checkpoint",
)


def observe_repository(
    repo_root: str | Path,
    config: HospiticationConfig | None = None,
) -> ObservationSnapshot:
    """Return an immutable structural snapshot without mutating the repository."""

    cfg = config or HospiticationConfig()
    if not isinstance(cfg.max_file_bytes, int) or isinstance(cfg.max_file_bytes, bool) or cfg.max_file_bytes < 1:
        raise ValueError('max_file_bytes must be a positive integer')
    root = Path(repo_root).resolve()
    if not root.is_dir():
        raise ValueError(f"Repository root is not a directory: {root}")
    observations: list[FileObservation] = []
    skipped: Counter[str] = Counter()
    excluded = tuple(sorted(set(cfg.excluded_paths)))
    for name in excluded:
        part = PurePosixPath(name)
        if not name or part.is_absolute() or '..' in part.parts or part == PurePosixPath('.') or '\\' in name:
            raise ValueError('Excluded paths must be repository-relative subpaths')
    extensions = set(cfg.code_extensions + cfg.doc_extensions + cfg.config_extensions + TEXT_EXTENSIONS)

    def excluded_path(path: Path) -> bool:
        relative = PurePosixPath(path.relative_to(root).as_posix())
        return any(relative == PurePosixPath(name) or PurePosixPath(name) in relative.parents for name in excluded)

    def walk_error(error: OSError) -> None:
        skipped['unreadable_directories'] += 1

    # Prune ignored directories before walking them; never follow symbolic links.
    for folder, dirs, names in os.walk(root, followlinks=False, onerror=walk_error):
        base = Path(folder)
        kept = []
        for name in sorted(dirs):
            path = base / name
            if path.is_symlink():
                skipped['symlink_directories'] += 1
            elif name in cfg.ignored_dirs:
                skipped['ignored_directories'] += 1
            elif excluded_path(path):
                skipped['excluded_directories'] += 1
            else:
                kept.append(name)
        dirs[:] = kept
        for name in sorted(names):
            path = base / name
            if path.is_symlink():
                skipped['symlink_files'] += 1
                continue
            if excluded_path(path):
                skipped['excluded_files'] += 1
                continue
            if path.suffix.lower() not in extensions and name not in TEXT_FILENAMES:
                skipped['unsupported_files'] += 1
                continue
            try:
                if not path.is_file():
                    skipped['non_regular_files'] += 1
                    continue
                if path.stat().st_size > cfg.max_file_bytes:
                    skipped['oversized_files'] += 1
                    continue
                # Bound the read even if a file grows after stat().
                with path.open('rb') as stream:
                    raw = stream.read(cfg.max_file_bytes + 1)
                if len(raw) > cfg.max_file_bytes:
                    skipped['oversized_files'] += 1
                    continue
                text = raw.decode('utf-8-sig')
                if '\x00' in text or any(ord(c) < 32 and c not in '\n\r\t\f' for c in text):
                    skipped['binary_files'] += 1
                    continue
                observations.append(_observe_file(root, path, raw, text))
            except UnicodeDecodeError:
                skipped['non_utf8_files'] += 1
            except OSError:
                skipped['unreadable_files'] += 1

    return ObservationSnapshot(
        repo_root=str(root),
        files=tuple(sorted(observations, key=lambda file: file.path)),
        observed_at=cfg.deterministic_timestamp,
        ignored_dirs=tuple(sorted(cfg.ignored_dirs)),
        scope=ObservationScope(
            version=VERSION,
            code_extensions=cfg.code_extensions,
            doc_extensions=cfg.doc_extensions,
            config_extensions=cfg.config_extensions,
            text_extensions=TEXT_EXTENSIONS,
            text_filenames=TEXT_FILENAMES,
            max_file_bytes=cfg.max_file_bytes,
            excluded_paths=excluded,
            ignored_dirs=tuple(sorted(cfg.ignored_dirs)),
            observed_files=len(observations),
            skipped_entries=tuple(sorted(skipped.items())),
        ),
    )


def _observe_file(
    root: Path,
    path: Path,
    raw: bytes,
    text: str,
) -> FileObservation:
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
