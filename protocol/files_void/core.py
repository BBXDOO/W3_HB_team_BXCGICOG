"""File.void runtime state contract.

File.void is a staging/manifestation layer. It may create a temporary
manifestation and a persistence handoff record, but it never writes final
artifacts by itself and never mutates source truth.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from hashlib import sha256
from typing import Any, Callable, Literal, Mapping
from uuid import uuid4

FileVoidState = Literal["UNRESOLVED", "RESOLVING", "MANIFESTED", "PERSISTED", "RELEASED"]


class FileVoidError(ValueError):
    """Raised when a File.void law or state transition is violated."""


@dataclass(frozen=True)
class FileVoidManifestation:
    """Temporary manifestation; not the File.void source and not final storage."""

    artifact_type: str
    content: str
    temporary: bool = True
    artifact_ref: str | None = None
    write_performed: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_type": self.artifact_type,
            "content": self.content,
            "temporary": self.temporary,
            "artifact_ref": self.artifact_ref,
            "write_performed": self.write_performed,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class FileVoidRecord:
    """Immutable state record for one File.void lifecycle."""

    void_id: str
    source_ref: str
    source_hash: str
    source_body: str = ""
    state: FileVoidState = "UNRESOLVED"
    env: str = "void.env"
    lib: str = "void.lib"
    manifestation: FileVoidManifestation | None = None
    trace: tuple[dict[str, Any], ...] = ()
    source_mutated: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "void_id": self.void_id,
            "source_ref": self.source_ref,
            "source_hash": self.source_hash,
            "state": self.state,
            "env": self.env,
            "lib": self.lib,
            "source_mutated": self.source_mutated,
            "manifestation": self.manifestation.to_dict() if self.manifestation else None,
            "trace": [dict(item) for item in self.trace],
            "invariants": {
                "file_void_is_artifact": False,
                "source_continuity_preserved": not self.source_mutated,
                "direct_write_allowed": False,
            },
        }

    def as_mpcp_result(self, *, cause: str = "file_void") -> dict[str, Any]:
        return {
            "state": "SUCCESS",
            "cause": cause,
            "result": self.to_dict(),
            "trace": [dict(item) for item in self.trace],
            "mutated": False,
            "review": self.state == "PERSISTED",
        }

    def _append_trace(self, stage: str, **data: Any) -> "FileVoidRecord":
        entry = {"stage": stage, **data}
        return replace(self, trace=self.trace + (entry,))

    def _require_state(self, *allowed: FileVoidState) -> None:
        if self.state not in allowed:
            raise FileVoidError(f"File.void state {self.state} cannot perform this operation; expected {allowed}")

    def resolve(self, *, env: str | None = None, lib: str | None = None) -> "FileVoidRecord":
        self._require_state("UNRESOLVED")
        resolved = replace(self, state="RESOLVING", env=env or self.env, lib=lib or self.lib)
        return resolved._append_trace("resolve", env=resolved.env, lib=resolved.lib, source_mutated=False)

    def manifest(
        self,
        artifact_type: str = "text",
        *,
        resolver: Callable[["FileVoidRecord"], str] | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> "FileVoidRecord":
        self._require_state("RESOLVING")
        body = resolver(self) if resolver else self.source_body
        manifestation = FileVoidManifestation(
            artifact_type=artifact_type,
            content=body,
            temporary=True,
            write_performed=False,
            metadata=dict(metadata or {}),
        )
        manifested = replace(self, state="MANIFESTED", manifestation=manifestation)
        return manifested._append_trace("manifest", artifact_type=artifact_type, temporary=True, source_mutated=False)

    def copy_manifestation(self) -> "FileVoidRecord":
        self._require_state("MANIFESTED")
        return self._append_trace("copy", copied=True, write_performed=False)

    def persist(
        self,
        *,
        target_ref: str,
        blueprint_ref: str | None = None,
        mpcp_task: str | None = None,
    ) -> "FileVoidRecord":
        self._require_state("MANIFESTED")
        if not target_ref or not str(target_ref).strip():
            raise FileVoidError("persist requires target_ref")
        if self.manifestation is None:
            raise FileVoidError("cannot persist without manifestation")
        manifestation = replace(
            self.manifestation,
            artifact_ref=str(target_ref),
            temporary=False,
            write_performed=False,
            metadata={
                **dict(self.manifestation.metadata),
                "blueprint_ref": blueprint_ref,
                "mpcp_task": mpcp_task,
                "handoff_required": True,
            },
        )
        persisted = replace(self, state="PERSISTED", manifestation=manifestation)
        return persisted._append_trace(
            "persist_handoff",
            target_ref=target_ref,
            blueprint_ref=blueprint_ref,
            mpcp_task=mpcp_task,
            write_performed=False,
            human_review_required=True,
        )

    def release(self) -> "FileVoidRecord":
        self._require_state("MANIFESTED", "PERSISTED")
        released = replace(self, state="RELEASED", manifestation=None)
        return released._append_trace("release", source_restored=True, source_mutated=False)


def create_void(
    *,
    source_ref: str,
    source_body: str = "",
    env: str = "void.env",
    lib: str = "void.lib",
    void_id: str | None = None,
) -> FileVoidRecord:
    if not source_ref or not str(source_ref).strip():
        raise FileVoidError("source_ref is required")
    source_text = str(source_body)
    hash_input = f"{source_ref}|{source_text}".encode("utf-8")
    record = FileVoidRecord(
        void_id=void_id or f"FV-{uuid4()}",
        source_ref=str(source_ref),
        source_body=source_text,
        source_hash=sha256(hash_input).hexdigest(),
        env=str(env),
        lib=str(lib),
    )
    return record._append_trace("unresolved", source_ref=record.source_ref, source_hash=record.source_hash)
