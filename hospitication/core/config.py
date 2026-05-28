"""Configuration for Hospitication read-only observation and reporting."""

from __future__ import annotations

from dataclasses import dataclass

VERSION = "0.1.0"
DEFAULT_TIMESTAMP = "1970-01-01T00:00:00Z"

CODE_EXTENSIONS = (
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".go",
    ".java",
    ".rs",
    ".rb",
    ".php",
    ".c",
    ".cpp",
    ".h",
    ".sh",
)
DOC_EXTENSIONS = (".md", ".txt", ".rst", ".adoc")
CONFIG_EXTENSIONS = (".json", ".yml", ".yaml", ".toml", ".ini", ".cfg")
DEFAULT_IGNORED_DIRS = (
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
)
DEFAULT_MAX_FILE_BYTES = 1_000_000


@dataclass(frozen=True)
class HospiticationConfig:
    """Read-only configuration for an observation run."""

    ignored_dirs: tuple[str, ...] = DEFAULT_IGNORED_DIRS
    code_extensions: tuple[str, ...] = CODE_EXTENSIONS
    doc_extensions: tuple[str, ...] = DOC_EXTENSIONS
    config_extensions: tuple[str, ...] = CONFIG_EXTENSIONS
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES
    deterministic_timestamp: str = DEFAULT_TIMESTAMP
    emit_threshold: float = 0.2
