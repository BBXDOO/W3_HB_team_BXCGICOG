"""MPCP adapter for File.void.

This adapter lets MPCP/Blueprint-style contexts call File.void as a bounded tool.
It returns MPCP-compatible SUCCESS/STOP payloads and never performs direct file
writes or source-truth mutation.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Callable

from protocol.files_void.tool import file_void_tool


def call_file_void_tool(context: Mapping[str, Any]) -> dict[str, Any]:
    """Call File.void from an MPCP/Blueprint context dictionary."""

    return file_void_tool(
        action=str(context.get("ACTION", context.get("action", "manifest"))),
        source_ref=str(context.get("SOURCE_REF", context.get("source_ref", "mpcp://unknown"))),
        source_body=str(context.get("SOURCE_BODY", context.get("source_body", ""))),
        env=str(context.get("ENV", context.get("env", "void.env"))),
        lib=str(context.get("LIB", context.get("lib", "void.lib"))),
        artifact_type=str(context.get("ARTIFACT_TYPE", context.get("artifact_type", "text"))),
        target_ref=context.get("TARGET_REF", context.get("target_ref")),
        blueprint_ref=context.get("BLUEPRINT_REF", context.get("blueprint_ref")),
        mpcp_task=str(context.get("TASK", context.get("task", "file_void"))),
        context=context,
    )


def build_file_void_stage(action: str = "manifest") -> Callable[[Any, dict[str, Any]], dict[str, Any]]:
    """Return an A-F stage function usable by ``protocol.mpcp.lib.Pillar``.

    Example:
        pillar.set_stage("D", build_file_void_stage("manifest"))
    """

    def _stage(previous: Any, context: dict[str, Any]) -> dict[str, Any]:
        stage_context = dict(context)
        stage_context.setdefault("ACTION", action)
        if previous is not None:
            stage_context["PREVIOUS_STAGE_RESULT"] = previous
        return call_file_void_tool(stage_context)

    return _stage
