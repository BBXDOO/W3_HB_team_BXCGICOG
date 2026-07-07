"""FastAPI app for the W3 cross gateway."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from w3_api.router import router

app = FastAPI(
    title="W3 API",
    version="0.1.0",
)

# ------------------------------------------------------------------
# CORS (สำหรับ PWA / Browser)
# ------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1",
        "http://localhost",
        "https://127.0.0.1",
        "https://localhost",
        # เพิ่มโดเมนจริงของ W3 หากมี
        # "https://w3.yourdomain.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


def service_status():
    return {
        "ok": True,
        "status": "online",
        "service": "W3-API",
        "version": "0.1.0",
    }


app.add_api_route(
    "/health",
    service_status,
    methods=["GET"],
)
