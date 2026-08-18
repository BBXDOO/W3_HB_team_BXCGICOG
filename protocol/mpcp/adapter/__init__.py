"""MPCP external adapters."""

from .w3_bridge import execute_with_w3
from .w3db import build_w3db_evidence_candidate

__all__ = [
    "build_w3db_evidence_candidate",
    "execute_with_w3",
]
