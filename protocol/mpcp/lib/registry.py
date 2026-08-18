"""MPCP survival-library and language-runtime registry."""

from __future__ import annotations

from dataclasses import dataclass
import shutil
from typing import Iterable, Mapping

from ..config import MPCPConfig, load_config


@dataclass(frozen=True)
class RuntimeBinding:
    language: str
    available: bool
    command: str | None
    kind: str

    def to_dict(self) -> dict:
        return {
            "language": self.language,
            "available": self.available,
            "command": self.command,
            "kind": self.kind,
        }


class LibraryRegistry:
    """Resolve capabilities without allowing libraries to govern MPCP flow."""

    def __init__(self, config: MPCPConfig | None = None) -> None:
        self.config = config or load_config()

    def library_group(self, name: str) -> tuple[str, ...]:
        try:
            return self.config.libraries[name.lower()]
        except KeyError as exc:
            raise KeyError(f"MPCP_LIB:UNKNOWN_GROUP:{name}") from exc

    def resolve_language(self, language: str) -> RuntimeBinding:
        supplied = language.strip().upper()
        short = str(self.config.data["language_aliases"].get(supplied, supplied)).upper()
        if not short:
            raise ValueError("MPCP_LIB:LANGUAGE_REQUIRED")
        if short in self.config.data_formats:
            return RuntimeBinding(short, True, None, "data_format")
        commands = self.config.language_runtime.get(short, ())
        for command in commands:
            resolved = shutil.which(command)
            if resolved:
                return RuntimeBinding(short, True, resolved, "runtime")
        return RuntimeBinding(short, False, None, "runtime")

    def resolve_candidates(self, languages: Iterable[str]) -> list[RuntimeBinding]:
        return [self.resolve_language(language) for language in languages]

    def select_available(self, languages: Iterable[str]) -> RuntimeBinding | None:
        for binding in self.resolve_candidates(languages):
            if binding.available:
                return binding
        return None

    def short_name(self, language: str) -> str:
        supplied = language.strip().upper()
        return str(self.config.data["language_aliases"].get(supplied, supplied)).upper()

    def validate_tag(self, tag: str) -> tuple[str, str]:
        if not isinstance(tag, str) or tag.count(":") != 1:
            raise ValueError(f"MPCP_LIB:INVALID_CROSS_L_TAG:{tag!r}")
        family, short = (part.strip().upper() for part in tag.split(":", 1))
        if family not in self.config.tag_families or not short:
            raise ValueError(f"MPCP_LIB:INVALID_CROSS_L_TAG:{tag!r}")
        return family, short

    def capability_report(self, languages: Iterable[str]) -> Mapping[str, dict]:
        return {item.language: item.to_dict() for item in self.resolve_candidates(languages)}
