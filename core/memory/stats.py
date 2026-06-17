"""Lightweight memory statistics for LRC2/runtime agents.

The module reads the shared JSON memory bus and returns a stable dictionary shape
used by runtime agents. It is read-only: no source truth or environment mutation.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any, Iterable

from core.memory.memory_bus import load_store, runtime_info


_FAILURE_MARKERS = {"fail", "failed", "failure", "error", "red", "stop", "block", "critical"}
_SUCCESS_MARKERS = {"success", "ok", "done", "ready", "green", "completed", "stable"}


def _text_parts(row: dict[str, Any]) -> list[str]:
    tags = row.get("tags") or []
    if not isinstance(tags, list):
        tags = [str(tags)]
    return [
        str(row.get("type", "")),
        str(row.get("source", "")),
        str(row.get("topic", "")),
        str(row.get("content", "")),
        " ".join(str(tag) for tag in tags),
    ]


def _matches_target(row: dict[str, Any], target: str) -> bool:
    target_lower = target.lower()
    if target_lower in {"", "w3", "system", "all", "*"}:
        return True
    return target_lower in " ".join(_text_parts(row)).lower()


def _markers(row: dict[str, Any]) -> set[str]:
    tokens: set[str] = set()
    for part in _text_parts(row):
        normalized = part.replace("_", " ").replace("-", " ").lower()
        tokens.update(token.strip() for token in normalized.split() if token.strip())
    return tokens


def _is_failed(row: dict[str, Any]) -> bool:
    return bool(_markers(row) & _FAILURE_MARKERS)


def _is_success(row: dict[str, Any]) -> bool:
    row_markers = _markers(row)
    if row_markers & _FAILURE_MARKERS:
        return False
    if row_markers & _SUCCESS_MARKERS:
        return True
    return bool(row_markers)


def _parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _top(counter: Counter[str], limit: int = 5) -> list[str]:
    return [key for key, _ in counter.most_common(limit)]


def _confidence(rows: Iterable[dict[str, Any]], total: int, failed: int) -> float:
    rows = list(rows)
    if total == 0:
        return 0.0
    scores = []
    for row in rows:
        score = row.get("score", 1)
        try:
            scores.append(float(score))
        except (TypeError, ValueError):
            scores.append(1.0)
    avg_score = sum(scores) / max(len(scores), 1)
    normalized_score = max(0.0, min(avg_score / 5.0, 1.0))
    failure_penalty = failed / total
    return round(max(0.0, normalized_score * (1.0 - failure_penalty)), 3)


def _health(total: int, failed: int) -> str:
    if total == 0:
        return "UNKNOWN"
    ratio = failed / total
    if ratio == 0:
        return "HEALTHY"
    if ratio < 0.3:
        return "WARNING"
    return "CRITICAL"


def memory_stats(target: str = "W3") -> dict[str, Any]:
    """Return stable memory statistics for a target/module name.

    The shape is intentionally broad because LRC2Agent formats several fields
    for reports. Missing memory returns zero/UNKNOWN values instead of failing.
    """
    target_text = str(target or "W3").strip()
    db = load_store()
    records = [row for row in db.get("records", []) if isinstance(row, dict)]
    rows = [row for row in records if _matches_target(row, target_text)]

    total = len(rows)
    failed = sum(1 for row in rows if _is_failed(row))
    success = sum(1 for row in rows if _is_success(row))

    sources = Counter(str(row.get("source", "unknown")) for row in rows)
    patterns = Counter(str(row.get("topic", row.get("type", "unknown"))) for row in rows)
    tags: Counter[str] = Counter()
    times = []
    for row in rows:
        for tag in row.get("tags") or []:
            tags[str(tag)] += 1
        parsed = _parse_time(row.get("timestamp"))
        if parsed is not None:
            times.append(parsed)

    first_seen = min(times).isoformat() if times else None
    last_seen_dt = max(times) if times else None
    last_seen = last_seen_dt.isoformat() if last_seen_dt else None
    age_seconds = None
    if last_seen_dt:
        age_seconds = int((datetime.now(timezone.utc) - last_seen_dt).total_seconds())

    return {
        "target": target_text,
        "total": total,
        "success": success,
        "failed": failed,
        "runtime": runtime_info().get("runtime", {}),
        "top_sources": _top(sources),
        "top_patterns": _top(patterns),
        "top_tags": _top(tags),
        "confidence": _confidence(rows, total, failed),
        "health": _health(total, failed),
        "trend": "NO_DATA" if total == 0 else ("NEEDS_REVIEW" if failed else "STABLE"),
        "first_seen": first_seen,
        "last_seen": last_seen,
        "age_seconds": age_seconds,
    }
