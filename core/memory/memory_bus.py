"""
W3 Shared Memory Core
Path: core/memory/memory_bus.py

Purpose:
- Shared memory between AI modules
- Persistent lightweight JSON backend
- Crash-safe runtime memory
- Multi-runtime compatible
- Thread-safe operations
- W3 orchestration support

Author: BBX19 / W3
"""

import os
import json
import uuid
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
    os.environ.get(
        "W3_MEMORY_FILE",
        DEFAULT_MEMORY_FILE
    )
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
# Time Helpers
# =========================================================

def now():
    return datetime.utcnow().isoformat() + "Z"


# =========================================================
# Store Initialization
# =========================================================

def _default_store():

    return {
        "version": "2.0",
        "created": now(),

        "runtime": {
            "engine": "W3_HB_Runtime",
            "memory_format": "LRC2",
            "write_mode": "atomic",
            "storage": "json"
        },

        "records": []
    }


def _ensure_store():

    if not MEMORY_FILE.exists():

        MEMORY_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        _atomic_write(_default_store())


# =========================================================
# Atomic JSON Write
# =========================================================

def _atomic_write(data):

    MEMORY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with tempfile.NamedTemporaryFile(
        mode="w",
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

        tmp.flush()
        os.fsync(tmp.fileno())

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

                db = json.load(f)

        except json.JSONDecodeError as e:

            raise MemoryError(
                f"Corrupted memory store: {e}"
            )

        # Auto schema patch
        if "runtime" not in db:
            db["runtime"] = {
                "engine": "W3_HB_Runtime",
                "memory_format": "LRC2",
                "write_mode": "atomic",
                "storage": "json"
            }

        if "records" not in db:
            db["records"] = []

        return db


def save_store(data):

    with _lock:
        _atomic_write(data)


# =========================================================
# Record Helpers
# =========================================================

def _build_record(
    source,
    topic,
    content,
    tags=None,
    score=1,
    record_type="memory"
):

    return {
        "id": str(uuid.uuid4()),
        "timestamp": now(),

        "type": record_type,

        "source": source,
        "topic": topic,
        "content": content,

        "tags": tags or [],

        "score": score
    }


# =========================================================
# Memory APIs
# =========================================================

def add_memory(
    source,
    topic,
    content,
    tags=None,
    score=1,
    record_type="memory"
):

    with _lock:

        db = load_store()

        record = _build_record(
            source=source,
            topic=topic,
            content=content,
            tags=tags,
            score=score,
            record_type=record_type
        )

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

        searchable = (
            f"{row.get('type', '')} "
            f"{row.get('source', '')} "
            f"{row.get('topic', '')} "
            f"{row.get('content', '')} "
            f"{' '.join(row.get('tags', []))}"
        ).lower()

        if keyword in searchable:
            results.append(row)

    return results


def memory_by_source(source):

    db = load_store()

    return [
        row for row in db["records"]
        if row.get("source") == source
    ]


def memory_by_type(record_type):

    db = load_store()

    return [
        row for row in db["records"]
        if row.get("type") == record_type
    ]


def top_memory(limit=10):

    db = load_store()

    rows = sorted(
        db["records"],
        key=lambda x: x.get("score", 0),
        reverse=True
    )

    return rows[:limit]


def runtime_info():

    db = load_store()

    return {
        "memory_file": str(MEMORY_FILE),
        "exists": MEMORY_FILE.exists(),
        "records": len(db["records"]),
        "runtime": db.get("runtime", {})
    }


# =========================================================
# Migration
# =========================================================

def migrate_legacy_ids():

    with _lock:

        db = load_store()

        changed = False

        for row in db["records"]:

            if not isinstance(
                row.get("id"),
                str
            ):

                row["id"] = str(uuid.uuid4())
                changed = True

        if changed:

            db["version"] = "2.0"

            save_store(db)

        return changed


# =========================================================
# Test Runtime
# =========================================================

if __name__ == "__main__":

    migrate_legacy_ids()

    add_memory(
        source="ChatGPT",
        topic="runtime",
        content="W3 runtime initialized",
        tags=["runtime", "boot"],
        score=5,
        record_type="system"
    )

    print(
        json.dumps(
            runtime_info(),
            indent=2,
            ensure_ascii=False
        )
    )

    print(
        json.dumps(
            get_memory(),
            indent=2,
            ensure_ascii=False
        )
    )
