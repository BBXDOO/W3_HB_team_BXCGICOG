"""FastAPI app for the W3 cross gateway."""

from __future__ import annotations

from fastapi import FastAPI

from w3_api.router import health_payload, router

app = FastAPI(title="W3 API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, object]:
    """Root gateway health check for local/Termux smoke tests."""

    return health_payload()


app.include_router(router)
