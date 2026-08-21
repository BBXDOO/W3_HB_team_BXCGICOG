"""Append-only lifecycle evidence for LRC2.

Each record includes the previous record hash.  This does not make the file
physically immutable, but it makes historical rewriting detectable while
keeping the format portable JSONL.
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_LOG_PATH = REPO_ROOT / "modules" / "LRC2" / "memory" / "lifecycle.jsonl"


def _canonical(value: Dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)


def _last_hash(path: Path) -> str:
    if not path.exists():
        return "GENESIS"
    last = ""
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                last = line
    if not last:
        return "GENESIS"
    try:
        return str(json.loads(last).get("record_hash") or "GENESIS")
    except (json.JSONDecodeError, AttributeError):
        return "UNVERIFIED_PREVIOUS_RECORD"


def append_lifecycle_record(
    event: Dict[str, Any], path: str | os.PathLike[str] | None = None
) -> Dict[str, Any]:
    """Append one evidence record without updating existing records."""
    target = Path(path) if path is not None else Path(os.environ.get("W3_LRC2_LOG_PATH", DEFAULT_LOG_PATH))
    target = target.expanduser().resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    previous_hash = _last_hash(target)
    body = {
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "previous_hash": previous_hash,
        "event": event,
    }
    record_hash = hashlib.sha256(_canonical(body).encode("utf-8")).hexdigest()
    record = {**body, "record_hash": record_hash}
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True, default=str) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    return {**record, "path": str(target)}


__all__ = ["append_lifecycle_record", "DEFAULT_LOG_PATH"]
