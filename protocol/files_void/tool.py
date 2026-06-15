"""MPCP/Blueprint-callable File.void tool wrapper."""

from __future__ import annotations

from typing import Any, Mapping

from protocol.files_void.core import FileVoidError, create_void


def file_void_tool(
    *,
    action: str = "manifest",
    source_ref: str,
    source_body: str = "",
    env: str = "void.env",
    lib: str = "void.lib",
    artifact_type: str = "text",
    target_ref: str | None = None,
    blueprint_ref: str | None = None,
    mpcp_task: str | None = None,
    context: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Run one safe File.void action and return an MPCP-compatible payload.

    Supported actions:
    - plan: create UNRESOLVED record only
    - manifest: UNRESOLVED -> RESOLVING -> MANIFESTED
    - copy: manifest then duplicate active manifestation state
    - save/persist: manifest then create a persistence handoff record
    - release: manifest then release the temporary manifestation

    This function never writes files, never stores final artifacts, and never
    mutates source truth.  ``save`` means handoff request, not direct write.
    """

    try:
        normalized_action = str(action or "manifest").strip().lower()
        record = create_void(source_ref=source_ref, source_body=source_body, env=env, lib=lib)
        record = record._append_trace(
            "tool_invoked",
            action=normalized_action,
            blueprint_ref=blueprint_ref,
            mpcp_task=mpcp_task,
            context_keys=sorted(str(key) for key in (context or {}).keys()),
        )

        if normalized_action == "plan":
            return record.as_mpcp_result(cause=mpcp_task or "file_void.plan")

        record = record.resolve(env=env, lib=lib).manifest(
            artifact_type=artifact_type,
            metadata={"blueprint_ref": blueprint_ref, "mpcp_task": mpcp_task},
        )

        if normalized_action == "manifest":
            return record.as_mpcp_result(cause=mpcp_task or "file_void.manifest")
        if normalized_action == "copy":
            return record.copy_manifestation().as_mpcp_result(cause=mpcp_task or "file_void.copy")
        if normalized_action in {"save", "persist"}:
            if not target_ref:
                raise FileVoidError("save/persist requires target_ref")
            return record.persist(
                target_ref=target_ref,
                blueprint_ref=blueprint_ref,
                mpcp_task=mpcp_task,
            ).as_mpcp_result(cause=mpcp_task or "file_void.persist")
        if normalized_action == "release":
            return record.release().as_mpcp_result(cause=mpcp_task or "file_void.release")

        raise FileVoidError(f"unknown File.void action: {action}")

    except Exception as exc:
        return {
            "state": "STOP",
            "cause": mpcp_task or "file_void",
            "error": str(exc),
            "mutated": False,
            "review": True,
        }
