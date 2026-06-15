from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class CrossRequest(BaseModel):
    source: str
    intent: str
    target: str
    mode: str
    payload: dict

@app.post("/w3/cross")
def w3_cross(req: CrossRequest):
    return {
        "ok": True,
        "message": "W3-API received",
        "px": req.payload.get("px"),
        "planner": "preview-only"
    }
