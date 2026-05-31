"""W3-API → EP_SIGNAL gateway adapter.

This adapter creates a compact EP_SIGNAL preview from the W3Lgu text. It does
not persist or overwrite EP_SIGNAL truth.
"""

from __future__ import annotations

from protocol.EP_SIGNAL.ep_signal_adapter import to_ep_signal


def build_ep_signal_preview(w3lgu_text: str) -> dict[str, object]:
    """Encode a small binary fingerprint preview for traceability only."""

    digest_bits = "".join(f"{byte:08b}" for byte in w3lgu_text.encode("utf-8")[:8])
    ep_signal = to_ep_signal(digest_bits or "0")
    return {
        "mode": "preview_only",
        "mutated": False,
        "format": "BIN",
        "ep_signal": ep_signal,
    }
