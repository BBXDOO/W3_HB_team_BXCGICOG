"""MPCP adapter for File.void.

This adapter lets MPCP/Blueprint-style contexts call File.void as a bounded tool.
It returns MPCP-compatible SUCCESS/STOP payloads and never performs direct file
writes or source-truth mutation.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Callable

try:
    from protocol.files_void.tool import file_void_tool
except ModuleNotFoundError:  # ``mpcp`` imported with ``protocol/`` as package root
    from files_void.tool import file_void_tool


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


def build_file_void_operation(action: str = "manifest") -> Callable[[Any, dict[str, Any]], dict[str, Any]]:
    """Return a named-operation callback usable by ``protocol.mpcp.lib.Pillar``."""

    def _operation(previous: Any, context: dict[str, Any]) -> dict[str, Any]:
        operation_context = dict(context)
        operation_context.setdefault("ACTION", action)
        if previous is not None:
            operation_context["PREVIOUS_OPERATION_RESULT"] = previous
        return call_file_void_tool(operation_context)

    return _operation


def build_file_void_stage(action: str = "manifest") -> Callable[[Any, dict[str, Any]], dict[str, Any]]:
    """Compatibility alias for callers created before A–F semantic alignment."""
    return build_file_void_operation(action)
