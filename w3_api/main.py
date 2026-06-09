"""FastAPI app for the W3 cross gateway."""

from __future__ import annotations

from fastapi import FastAPI

from w3_api.router import router

app = FastAPI(title="W3 API", version="0.1.0")
app.include_router(router)
