"""FastAPI app for the W3 cross gateway."""

from __future__ import annotations

from fastapi import FastAPI

from w3_api.router import router

app = FastAPI(title="W3 API", version="0.1.0")
app.include_router(router)


def service_status():
    return {"ok": True, "status": "online", "service": "W3-API", "version": "0.1.0"}


app.add_api_route("/health", service_status, methods=["GET"])
