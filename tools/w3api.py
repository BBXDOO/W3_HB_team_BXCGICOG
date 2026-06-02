#!/usr/bin/env python3
import json
import sys
import urllib.request
import urllib.error

API_URL = "http://127.0.0.1:8000/w3/cross"
HEALTH_URL = "http://127.0.0.1:8000/health"


def post_json(url, payload):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=10) as res:
        return json.loads(res.read().decode("utf-8"))


def get_json(url):
    with urllib.request.urlopen(url, timeout=5) as res:
        return json.loads(res.read().decode("utf-8"))


def pick(text, key):
    marker = key + "="
    if marker not in text:
        return "-"
    part = text.split(marker, 1)[1]
    return part.split(" ", 1)[0].split("|", 1)[0]


def pretty(result):
    print("\n=== W3 API RESULT ===")
    print("id      :", result.get("id"))
    print("status  :", result.get("status"))

    runtime = result.get("runtime", {})
    print("module  :", runtime.get("module"))
    print("task    :", runtime.get("task"))

    output = runtime.get("output", "")
    print("\n=== SUMMARY ===")
    print("target     :", pick(output, "target:").replace(":", "") if "target:" in output else pick(output, "target"))
    print("focus      :", pick(output, "focus:").replace(":", "") if "focus:" in output else pick(output, "focus"))
    print("health     :", pick(output, "health"))
    print("confidence :", pick(output, "confidence"))
    print("trend      :", pick(output, "trend"))
    print("memory     :", pick(output, "total"))

    print("\n=== RAW OUTPUT ===")
    print(output)

    signal = result.get("signal", {})
    print("\n=== SIGNAL ===")
    print("type      :", signal.get("type"))
    print("traceable :", signal.get("traceable"))
    print("mutated   :", signal.get("mutated"))
    print("cross     :", signal.get("cross"))


def usage():
    print("""
W3 API helper

Usage:
  python tools/w3api.py health
  python tools/w3api.py review REDR memory
  python tools/w3api.py review DTML law
  python tools/w3api.py review W3 system
  python tools/w3api.py design W3 general

Format:
  python tools/w3api.py <intent> <target> <focus>

Examples:
  python tools/w3api.py review REDR memory
  python tools/w3api.py review W3 system
""")


def main():
    if len(sys.argv) == 1:
        usage()
        return

    if sys.argv[1] in ("help", "-h", "--help"):
        usage()
        return

    if sys.argv[1] == "health":
        try:
            print(json.dumps(get_json(HEALTH_URL), indent=2, ensure_ascii=False))
        except Exception as e:
            print("ERROR: server offline or health failed:", e)
        return

    intent = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) >= 3 else "W3"
    focus = sys.argv[3] if len(sys.argv) >= 4 else "general"

    payload = {
        "source": "BBX19",
        "intent": intent,
        "target": target,
        "focus": focus,
        "mode": "cross",
    }

    try:
        result = post_json(API_URL, payload)
        pretty(result)
    except urllib.error.URLError as e:
        print("ERROR: API server not running?")
        print("Run this first:")
        print("  python W3_API_SERVER_SIMPLE.py")
        print("detail:", e)
    except Exception as e:
        print("ERROR:", e)


if __name__ == "__main__":
    main()
