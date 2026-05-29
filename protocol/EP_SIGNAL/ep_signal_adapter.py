"""Adapters for EP_SIGNAL encode/decode interop."""

from __future__ import annotations

from protocol.EP_SIGNAL import reference_implementation as epi


def to_ep_signal(data_bin: str) -> str:
    """Convert a non-empty binary string to EP_SIGNAL format."""
    if not data_bin or not all(c in "01" for c in data_bin):
        raise ValueError("data_bin must be a non-empty binary string")
    return epi.encode(data_bin, fmt="BIN")


def from_ep_signal(signal: str) -> str:
    """Decode EP_SIGNAL format back into a binary string."""
    return epi.decode(signal)


def interop_with_w3lgu(w3lgu_data: bytes) -> str:
    """Encode W3Lgu bytes as EP_SIGNAL via their binary representation."""
    binstr = "".join(f"{byte:08b}" for byte in w3lgu_data)
    return to_ep_signal(binstr)


def interop_with_mpcp(mp_data: str) -> str:
    """Encode an MPCP binary string as EP_SIGNAL."""
    return to_ep_signal(mp_data)
