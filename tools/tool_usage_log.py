"""Minimal append-only usage log for root-level W3 tools.

This helper records only:
- who called the tool
- which tool was called
- why it was called
- when it was used

It does not grant permission to use a tool and does not execute tools itself.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parent / "tool_usage.log"


def log_tool_usage(*, caller: str, tool: str, purpose: str) -> dict[str, str]:
    """Append one tool-usage record and return the recorded entry."""
    entry = {
        "who": str(caller),
        "tool": str(tool),
        "purpose": str(purpose),
        "used_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }

    with LOG_PATH.open("a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(entry, ensure_ascii=False) + "\n")

    return entry
