"""W3-API cross gateway package.

The FastAPI application is loaded lazily so adapter modules can be imported in
lightweight protocol tests without requiring gateway runtime dependencies first.
"""

__all__ = ["app"]


def __getattr__(name: str):
    if name == "app":
        from w3_api.main import app

        return app
    raise AttributeError(f"module 'w3_api' has no attribute {name!r}")
