"""
PSP2 MFC Logic — PX stamp generation + Node registry

PSP2 ไม่ทำ routing, ไม่ infer, ไม่ validate content
หน้าที่: generate PX stamp + resolve node address สำหรับ forward
"""

from __future__ import annotations

from hashlib import sha1
from typing import Any, Dict

# ------------------------------------------------------------------
# Node Registry
# แต่ละปลายทางมี node address ของตัวเอง
# ni: = node in, no: = node out (เผื่ออนาคต)
# ------------------------------------------------------------------

NODE_REGISTRY: Dict[str, str] = {
    "REDR": "ni:redr",
    "DTML": "ni:dtml",
    "LRC2": "ni:lrc2",
    "MNPS": "ni:mnps",
    "TL-S": "ni:tls",
}

# Cross-system prefix สำหรับ WHUB อนาคต
CROSS_PREFIX = "xs:"


def register_node(target: str, address: str) -> None:
    """ลงทะเบียน node ใหม่ (สำหรับขยายระบบ หรือ cross-system)"""
    NODE_REGISTRY[target.upper().strip()] = address


# ------------------------------------------------------------------
# PX Stamp
# รูปแบบ: LN{room}'{seq:04d}
#    เช่น  LNCU'0001, LNCA'0042
# สำหรับ cross-system: {system_id}/LN{room}'{seq:04d}
# ------------------------------------------------------------------

ROOM_ORDER = ["CA", "CU", "RE", "SI", "AP", "EV"]


def generate_px_stamp(package: Dict[str, Any], system_id: str = "") -> str:
    """สร้าง PX stamp แบบกำหนดเอง รองรับ cross-series"""
    raw = package.get("package_id") or package.get("_px") or str(package)
    digest = sha1(raw.encode("utf-8")).hexdigest()
    seq = int(digest[:4], 16) % 9999 + 1
    room = _resolve_room(package)
    px = f"LN{room}'{seq:04d}"
    if system_id:
        px = f"{system_id}/{px}"
    return f"PX:{px}"


def _resolve_room(package: Dict[str, Any]) -> str:
    room = package.get("_room", "CU").upper().strip()
    if room in ROOM_ORDER:
        return room
    return "CU"


# ------------------------------------------------------------------
# Node resolution
# ------------------------------------------------------------------

def resolve_node(target: str) -> str:
    """แปลงชื่อปลายทาง -> node address"""
    t = target.upper().strip()
    node = NODE_REGISTRY.get(t)
    if node:
        return node
    return f"{CROSS_PREFIX}{t.lower()}"
