#!/usr/bin/env python3
"""Small Termux-friendly helper for the W3-API cross gateway."""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from typing import Any

API_URL = "http://127.0.0.1:8000/w3/cross"
HEALTH_URL = "http://127.0.0.1:8000/health"


def post_json(url: str, payload: dict[str, Any]) -> dict[str, Any]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as res:
        return json.loads(res.read().decode("utf-8"))


def get_json(url: str) -> dict[str, Any]:
    with urllib.request.urlopen(url, timeout=5) as res:
        return json.loads(res.read().decode("utf-8"))


def _print_json(payload: Any) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def pretty(result: dict[str, Any], *, intent: str, target: str, focus: str) -> None:
    signal = result.get("signal", {}) or {}
    w3db = signal.get("w3db", {}) or {}
    px = w3db.get("px", {}) or {}
    ep_signal = signal.get("ep_signal", {}) or {}

    print("\n=== W3 API RESULT ===")
    print("id      :", result.get("id"))
    print("status  :", result.get("status"))
    print("intent  :", intent)
    print("target  :", signal.get("target", target))
    print("focus   :", focus)
    print("mode    :", signal.get("mode", "cross"))

    print("\n=== W3LGU ===")
    print(result.get("w3lgu", "-"))

    print("\n=== W3DB PLAN ===")
    print("mode :", w3db.get("mode"))
    print("xiz  :", w3db.get("xiz_hint"))
    print("tuf  :", w3db.get("tuf_hint"))
    print("px   :", px.get("px_id") or px.get("id") or px.get("position") or "-")

    print("\n=== SIGNAL ===")
    print("type      :", signal.get("type"))
    print("traceable :", signal.get("traceable"))
    print("mutated   :", signal.get("mutated"))
    print("ep_mode   :", ep_signal.get("mode"))
    print("ep_format :", ep_signal.get("format"))
    print("ep_signal :", ep_signal.get("ep_signal"))


def usage() -> None:
    print(
        """
W3 API helper

Usage:
  python tools/w3api.py health
  python tools/w3api.py review REDR memory
  python tools/w3api.py review DTML law
  python tools/w3api.py review W3 system
  python tools/w3api.py design W3 general

Format:
  python tools/w3api.py <intent> <target> <focus> [data...]

Server:
  python -m uvicorn w3_api.main:app --host 127.0.0.1 --port 8000
"""
    )


def _print_http_error(prefix: str, err: urllib.error.HTTPError) -> None:
    print(prefix)
    try:
        body = err.read().decode("utf-8")
    except Exception:
        body = ""
    print("status:", err.code)
    if body:
        print("body:", body)


def main() -> int:
    if len(sys.argv) == 1 or sys.argv[1] in ("help", "-h", "--help"):
        usage()
        return 0

    if sys.argv[1] == "health":
        try:
            _print_json(get_json(HEALTH_URL))
            return 0
        except urllib.error.HTTPError as err:
            _print_http_error("ERROR: health endpoint failed", err)
            return 1
        except Exception as exc:
            print("ERROR: server offline or health failed:", exc)
            print("Run this first:")
            print("  python -m uvicorn w3_api.main:app --host 127.0.0.1 --port 8000")
            return 1

    intent = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) >= 3 else "W3"
    focus = sys.argv[3] if len(sys.argv) >= 4 else "general"
    data = " ".join(sys.argv[4:])

    payload = {
        "source": "BBX19",
        "intent": intent,
        "target": target,
        "mode": "cross",
        "payload": {
            "focus": focus,
            "data": data,
        },
    }

    try:
        result = post_json(API_URL, payload)
        pretty(result, intent=intent, target=target, focus=focus)
        return 0
    except urllib.error.HTTPError as err:
        _print_http_error("ERROR: API request failed", err)
        return 1
    except urllib.error.URLError as err:
        print("ERROR: API server not running?")
        print("Run this first:")
        print("  python -m uvicorn w3_api.main:app --host 127.0.0.1 --port 8000")
        print("detail:", err)
        return 1
    except Exception as exc:
        print("ERROR:", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
