"""Cast main-activity log.

บันทึกภาพรวมระดับ MAIN ของ W3 เท่านั้น:
  - ใครรับงานอะไร (module -> task assignment)
  - subsystem แต่ละตัวรายงานสถานะเข้ามาไหม / มายังไง

ไม่บันทึกรายละเอียดภายในของ subsystem ใดๆ (เช่น W3Lgu: REDR/PSP2/
DTML/LRC2) — ของพวกนั้นมี memory ของตัวเองอยู่แล้ว และตามที่ BBX19
ระบุ อาจไม่ต้องเผยแพร่ออกไปด้วย

ไฟล์นี้เขียนเฉพาะ knowledge/cast/main_activity_log.jsonl
เป็น append-only เหมือน LRC2 (ห้ามแก้ของเก่า เขียนบรรทัดใหม่เท่านั้น)
"""

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

MAIN_LOG_DIR = os.path.join("knowledge", "cast")
MAIN_LOG_PATH = os.path.join(MAIN_LOG_DIR, "main_activity_log.jsonl")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _append(record: Dict[str, Any], path: str = MAIN_LOG_PATH) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def log_assignment(
    module: str,
    task: str,
    assigned_by: str = "unknown",
    note: str = "",
) -> Dict[str, Any]:
    """บันทึกว่า "ใครรับงานอะไร" ระดับ main

    เรียกตอน W3 มอบหมายงานให้โมดูลใดๆ (ไม่ใช่ตอนโมดูลนั้นทำงานเสร็จ
    — จุดนั้นเป็นหน้าที่ log_subsystem_report แทน)
    """
    record = {
        "type": "assignment",
        "timestamp": _now(),
        "module": module,
        "task": task,
        "assigned_by": assigned_by,
        "note": note,
        "source": "Cast",
    }
    _append(record)
    return record


def log_subsystem_report(
    subsystem: str,
    reported: bool,
    channel: str = "",
    summary: str = "",
) -> Dict[str, Any]:
    """บันทึกว่า subsystem นี้ "รายงานสถานะเข้ามาไหม" และ "มายังไง"

    reported=False ก็ต้องบันทึกด้วย — เพื่อให้เห็นว่า subsystem ไหน
    เงียบ ไม่ใช่แค่บันทึกตอนมันรายงานมาเท่านั้น (ตรง LINE_B: ไม่ซ่อน
    ความจริงแม้ความจริงคือ "ไม่มีอะไรเกิดขึ้น")
    """
    record = {
        "type": "subsystem_report",
        "timestamp": _now(),
        "subsystem": subsystem,
        "reported": reported,
        "channel": channel or "unspecified",
        "summary": summary,
        "source": "Cast",
    }
    _append(record)
    return record


def read_recent(limit: int = 20, path: str = MAIN_LOG_PATH) -> list:
    """อ่าน record ล่าสุด n รายการ (สำหรับ OWNER หรือโมดูลอื่นดึงย้อนหลัง)"""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as fh:
        lines = [line for line in fh if line.strip()]
    records = [json.loads(line) for line in lines[-limit:]]
    return records


def summarize_subsystem_health(path: str = MAIN_LOG_PATH) -> Dict[str, Any]:
    """สรุปว่า subsystem ไหนรายงานล่าสุดเมื่อไหร่ / เงียบไปหรือยัง

    ใช้ดูภาพรวมเร็วๆ ว่า subsystem ไหนควรถูกตรวจสอบ
    """
    if not os.path.exists(path):
        return {"subsystems": {}, "checked_at": _now()}

    subsystems: Dict[str, Dict[str, Any]] = {}
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            if record.get("type") != "subsystem_report":
                continue
            name = record["subsystem"]
            entry = subsystems.setdefault(
                name, {"last_seen": None, "last_reported": None, "total_reports": 0}
            )
            entry["last_seen"] = record["timestamp"]
            entry["last_reported"] = record["reported"]
            if record["reported"]:
                entry["total_reports"] += 1

    return {"subsystems": subsystems, "checked_at": _now()}


__all__ = [
    "log_assignment",
    "log_subsystem_report",
    "read_recent",
    "summarize_subsystem_health",
]

