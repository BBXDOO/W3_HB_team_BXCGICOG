"""
W3 Shared Memory Core
Path: core/memory/memory_bus.py

Purpose:
- Shared memory between AI modules
- Save / Load / Search context
- Persistent lightweight memory store
- Mobile friendly JSON backend

Author: BBX19 / W3
"""

import json
import threading
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent
MEMORY_FILE = BASE_DIR / "memory_store.json"

_lock = threading.RLock()


class MemoryError(Exception):
    pass


def now():
    return datetime.utcnow().isoformat() + "Z"


def _ensure_store():
    if not MEMORY_FILE.exists():
        MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "version": "1.0",
                    "created": now(),
                    "records": []
                },
                f,
                indent=2,
                ensure_ascii=False
            )


def load_store():
    with _lock:
        _ensure_store()
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)


def save_store(data):
    with _lock:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


def add_memory(source, topic, content, tags=None, score=1):
    """
    Example:
    add_memory("ChatGPT", "router", "design complete", ["core","router"])
    """
    with _lock:
        db = load_store()

        record = {
            "id": len(db["records"]) + 1,
            "timestamp": now(),
            "source": source,
            "topic": topic,
            "content": content,
            "tags": tags or [],
            "score": score
        }

        db["records"].append(record)
        save_store(db)

    return record


def get_memory(limit=10):
    db = load_store()
    return db["records"][-limit:]


def search_memory(keyword):
    db = load_store()

    results = []
    keyword = keyword.lower()

    for row in db["records"]:
        text = json.dumps(row, ensure_ascii=False).lower()
        if keyword in text:
            results.append(row)

    return results


def memory_by_source(source):
    db = load_store()
    return [x for x in db["records"] if x["source"] == source]


def top_memory(limit=10):
    db = load_store()
    rows = sorted(db["records"], key=lambda x: x["score"], reverse=True)
    return rows[:limit]


if __name__ == "__main__":
    add_memory(
        source="ChatGPT",
        topic="router",
        content="W3 module router initialized",
        tags=["core", "router"],
        score=5
    )

    print(json.dumps(get_memory(), indent=2, ensure_ascii=False))
