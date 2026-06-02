#!/usr/bin/env python3
"""Local W3-API client/wrapper for Termux and developer machines.

This client can call the gateway and optionally write a local Markdown copy of
that response. The API remains gateway-only; any file writing happens only in
this local wrapper when the user passes --write-md.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_SERVER = "http://127.0.0.1:8000"


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload = parse_payload_json(args.payload_json)
    if args.focus:
        payload["focus"] = args.focus
    if args.contract:
        payload["contract"] = args.contract
    return {
        "source": args.source,
        "intent": args.intent,
        "target": args.target,
        "mode": args.mode,
        "payload": payload,
    }


def parse_payload_json(raw: str | None) -> dict[str, Any]:
    if not raw:
        return {}
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError("--payload-json must decode to a JSON object")
    return parsed


def request_json(method: str, url: str, payload: dict[str, Any] | None = None, timeout: float = 10.0) -> dict[str, Any]:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(url, data=data, method=method)
    request.add_header("Content-Type", "application/json")
    with urlopen(request, timeout=timeout) as response:
        body = response.read().decode("utf-8")
    parsed = json.loads(body)
    if not isinstance(parsed, dict):
        raise ValueError("W3-API response was not a JSON object")
    return parsed


def render_markdown(response: dict[str, Any]) -> str:
    signal = response.get("signal", {}) if isinstance(response.get("signal"), dict) else {}
    w3db = signal.get("w3db", {}) if isinstance(signal.get("w3db"), dict) else {}
    ep_signal = signal.get("ep_signal", {}) if isinstance(signal.get("ep_signal"), dict) else {}
    lines = [
        "# W3-API Cross Result",
        "",
        f"- Status: `{response.get('status', 'unknown')}`",
        f"- ID: `{response.get('id', 'unknown')}`",
        f"- Mutated: `{str(signal.get('mutated', False)).lower()}`",
        f"- W3DB mode: `{w3db.get('mode', 'unknown')}`",
        f"- EP_SIGNAL mode: `{ep_signal.get('mode', 'unknown')}`",
        "",
        "## W3Lgu",
        "",
        "```text",
        str(response.get("w3lgu", "")),
        "```",
        "",
        "## Raw JSON",
        "",
        "```json",
        json.dumps(response, ensure_ascii=False, indent=2, sort_keys=True),
        "```",
        "",
        "_Written by local wrapper only; W3-API remained gateway-only._",
    ]
    return "\n".join(lines) + "\n"


def write_markdown(path: str, response: dict[str, Any]) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_markdown(response), encoding="utf-8")
    return output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="w3api",
        description="Call the W3-API gateway from a local shell. Does not make the server write truth.",
    )
    parser.add_argument("--server", default=DEFAULT_SERVER, help="W3-API base URL")
    parser.add_argument("--timeout", type=float, default=10.0, help="HTTP timeout in seconds")
    parser.add_argument("--health", action="store_true", help="Call GET /health instead of POST /w3/cross")
    parser.add_argument("--source", default="termux", help="Request source")
    parser.add_argument("--intent", default="review", help="Intent for /w3/cross")
    parser.add_argument("--target", default="W3", help="Target system")
    parser.add_argument("--mode", default="cross", help="Gateway mode")
    parser.add_argument("--focus", default=None, help="Convenience payload.focus value")
    parser.add_argument("--contract", default=None, help="Convenience payload.contract value")
    parser.add_argument("--payload-json", default=None, help="Extra JSON object for payload")
    parser.add_argument("--write-md", default=None, help="Optional local Markdown output path")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    base_url = args.server.rstrip("/")
    try:
        if args.health:
            response = request_json("GET", f"{base_url}/health", timeout=args.timeout)
        else:
            response = request_json("POST", f"{base_url}/w3/cross", build_payload(args), args.timeout)
        if args.write_md:
            written = write_markdown(args.write_md, response)
            print(f"wrote:{written}")
        print(json.dumps(response, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        print(f"w3api:error:{type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
