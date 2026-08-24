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
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Union

MAIN_LOG_DIR = os.path.join("knowledge", "cast")
MAIN_LOG_PATH = os.path.join(MAIN_LOG_DIR, "main_activity_log.jsonl")
_WRITE_LOCK = threading.RLock()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _resolve_path(path: Optional[Union[str, os.PathLike]] = None) -> Path:
    configured = path or os.environ.get("W3_CAST_ACTIVITY_LOG") or MAIN_LOG_PATH
    return Path(configured).expanduser().resolve()


def _append(
    record: Dict[str, Any],
    path: Optional[Union[str, os.PathLike]] = None,
) -> str:
    """Append one durable JSONL record and return the actual path used."""
    target = _resolve_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
    with _WRITE_LOCK:
        with target.open("a", encoding="utf-8") as fh:
            fh.write(encoded)
            fh.flush()
            os.fsync(fh.fileno())
    return str(target)


def log_assignment(
    module: str,
    task: str,
    assigned_by: str = "unknown",
    note: str = "",
    path: Optional[Union[str, os.PathLike]] = None,
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
    record["log_path"] = str(_resolve_path(path))
    _append(record, record["log_path"])
    return record


def log_subsystem_report(
    subsystem: str,
    reported: bool,
    channel: str = "",
    summary: str = "",
    path: Optional[Union[str, os.PathLike]] = None,
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
    record["log_path"] = str(_resolve_path(path))
    _append(record, record["log_path"])
    return record


def read_recent(
    limit: int = 20,
    path: Optional[Union[str, os.PathLike]] = None,
) -> list:
    """อ่าน record ล่าสุด n รายการ (สำหรับ OWNER หรือโมดูลอื่นดึงย้อนหลัง)"""
    target = _resolve_path(path)
    if not target.exists():
        return []
    with target.open("r", encoding="utf-8") as fh:
        lines = [line for line in fh if line.strip()]
    requested = max(0, int(limit))
    if requested == 0:
        return []
    records = []
    for line in lines[-requested:]:
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(record, dict):
            records.append(record)
    return records


def summarize_subsystem_health(
    path: Optional[Union[str, os.PathLike]] = None,
) -> Dict[str, Any]:
    """สรุปว่า subsystem ไหนรายงานล่าสุดเมื่อไหร่ / เงียบไปหรือยัง

    ใช้ดูภาพรวมเร็วๆ ว่า subsystem ไหนควรถูกตรวจสอบ
    """
    target = _resolve_path(path)
    if not target.exists():
        return {"subsystems": {}, "checked_at": _now()}

    subsystems: Dict[str, Dict[str, Any]] = {}
    malformed_records = 0
    with target.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                malformed_records += 1
                continue
            if not isinstance(record, dict):
                malformed_records += 1
                continue
            if record.get("type") != "subsystem_report":
                continue
            name = str(record.get("subsystem") or "unknown")
            entry = subsystems.setdefault(
                name, {"last_seen": None, "last_reported": None, "total_reports": 0}
            )
            entry["last_seen"] = record.get("timestamp")
            entry["last_reported"] = bool(record.get("reported"))
            if record.get("reported") is True:
                entry["total_reports"] += 1

    return {
        "subsystems": subsystems,
        "checked_at": _now(),
        "malformed_records": malformed_records,
        "log_path": str(target),
    }


__all__ = [
    "log_assignment",
    "log_subsystem_report",
    "read_recent",
    "summarize_subsystem_health",
]
