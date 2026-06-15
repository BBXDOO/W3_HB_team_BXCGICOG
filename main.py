"""Compatibility entrypoint for running the canonical W3-API app.

This keeps `uvicorn main:app` and `uvicorn w3_api.main:app` on the same
implementation so the `/w3/cross` contract and `/w3/cross/plan` route do not
drift apart.
"""

from w3_api.main import app

__all__ = ["app"]
