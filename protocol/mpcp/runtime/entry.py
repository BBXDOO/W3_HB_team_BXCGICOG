"""Stable MPCP runtime entry surface.

Modew implementations are registered by their owning system. MPCP does not
register a pretend implementation or execute work at import time.
"""

from .executor import PILLAR_REGISTRY, parse_mpcp, register, run, run_packet, to_mpcp_output

__all__ = [
    "PILLAR_REGISTRY",
    "parse_mpcp",
    "register",
    "run",
    "run_packet",
    "to_mpcp_output",
]
