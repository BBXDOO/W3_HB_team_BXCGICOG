"""Packet-safe encoding for externally supplied W3Lgu values."""

from __future__ import annotations

from urllib.parse import quote, unquote


def encode_w3lgu_value(value: object) -> str:
    """Percent-encode a value so it cannot introduce W3Lgu fields or lines."""

    normalized = " ".join(
        str(value).replace("\n", " ").replace("\r", " ").split()
    )
    return quote(normalized, safe="-._~")


def decode_w3lgu_value(value: str) -> str:
    """Decode a value previously produced by :func:`encode_w3lgu_value`."""

    return unquote(value)
