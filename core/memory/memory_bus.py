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

import os
import json
import tempfile
import threading

from pathlib import Path
from datetime import datetime


# =========================================================
# Runtime Path Resolution
# =========================================================

ROOT_DIR = Path(__file__).resolve().parents[2]

DEFAULT_MEMORY_FILE = (
    ROOT_DIR / "core" / "memory" / "memory_store.json"
)

MEMORY_FILE = Path(
    os.environ.get("W3_MEMORY_FILE", DEFAULT_MEMORY_FILE)
).expanduser().resolve()


# =========================================================
# Thread Lock
# =========================================================

_lock = threading.RLock()


# =========================================================
# Exceptions
# =========================================================

class MemoryError(Exception):
    pass


# =========================================================
# Helpers
# =========================================================

def now():
    return datetime.utcnow().isoformat() + "Z"


def _ensure_store():
    """
    Create memory store if not exists.
    """

    if not MEMORY_FILE.exists():

        MEMORY_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

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


def _atomic_write(data):
    """
    Prevent corrupted JSON during crash/interruption.
    Mobile-safe.
    """

    MEMORY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with tempfile.NamedTemporaryFile(
        "w",
        delete=False,
        encoding="utf-8",
        dir=MEMORY_FILE.parent
    ) as tmp:

        json.dump(
            data,
            tmp,
            indent=2,
            ensure_ascii=False
        )

        tmp_path = Path(tmp.name)

    tmp_path.replace(MEMORY_FILE)


# =========================================================
# Store Operations
# =========================================================

def load_store():

    with _lock:

        _ensure_store()

        try:

            with open(
                MEMORY_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        except json.JSONDecodeError as e:
            raise MemoryError(
                f"Corrupted memory store: {e}"
            )


def save_store(data):

    with _lock:
        _atomic_write(data)


# =========================================================
# Memory APIs
# =========================================================

def add_memory(
    source,
    topic,
    content,
    tags=None,
    score=1
):
    """
    Example:
    add_memory(
        "ChatGPT",
        "router",
        "design complete",
        ["core", "router"]
    )
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

    keyword = keyword.lower()

    results = []

    for row in db["records"]:

        text = json.dumps(
            row,
            ensure_ascii=False
        ).lower()

        if keyword in text:
            results.append(row)

    return results


def memory_by_source(source):

    db = load_store()

    return [
        x for x in db["records"]
        if x["source"] == source
    ]


def top_memory(limit=10):

    db = load_store()

    rows = sorted(
        db["records"],
        key=lambda x: x["score"],
        reverse=True
    )

    return rows[:limit]


# =========================================================
# Runtime Info
# =========================================================

def runtime_info():

    return {
        "memory_file": str(MEMORY_FILE),
        "exists": MEMORY_FILE.exists(),
        "record_count": len(load_store()["records"])
    }


# =========================================================
# Test
# =========================================================

if __name__ == "__main__":

    add_memory(
        source="ChatGPT",
        topic="router",
        content="W3 module router initialized",
        tags=["core", "router"],
        score=5
    )

    print(json.dumps(
        get_memory(),
        indent=2,
        ensure_ascii=False
    ))

    print(json.dumps(
        runtime_info(),
        indent=2,
        ensure_ascii=False
    ))
