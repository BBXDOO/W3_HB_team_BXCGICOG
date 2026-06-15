"""Compatibility entrypoint for the canonical W3-API app.

This module keeps all common server entrypoints on the same FastAPI app object:

- ``uvicorn main:app``
- ``uvicorn w3_api.main:app``
- ``python main.py``

The canonical implementation stays in :mod:`w3_api.main` so the ``/health``,
``/w3/cross``, and ``/w3/cross/plan`` routes do not drift apart.
"""

from __future__ import annotations

from w3_api.main import app

HOST = "127.0.0.1"
PORT = 8000


def main() -> int:
    """Run the canonical W3-API app for local/Termux use."""

    try:
        import uvicorn
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "ERROR: uvicorn is required to run the W3-API server.\n"
            "Install dependencies with: python -m pip install -r requirements.txt"
        ) from exc

    uvicorn.run(app, host=HOST, port=PORT)
    return 0


__all__ = ["app", "main"]


if __name__ == "__main__":
    raise SystemExit(main())
