"""Importable File.void runtime package.

The documentation lives in ``protocol/Files.void/`` because that is the W3
concept name.  Python imports use ``protocol.files_void`` so MPCP, Blueprint,
and tests can call the runtime as a normal tool.
"""

from protocol.files_void.core import (
    FileVoidError,
    FileVoidManifestation,
    FileVoidRecord,
    FileVoidState,
    create_void,
)
from protocol.files_void.tool import file_void_tool

__all__ = [
    "FileVoidError",
    "FileVoidManifestation",
    "FileVoidRecord",
    "FileVoidState",
    "create_void",
    "file_void_tool",
]
