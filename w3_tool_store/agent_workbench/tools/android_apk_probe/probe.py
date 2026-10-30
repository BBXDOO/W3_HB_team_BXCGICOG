#!/usr/bin/env python3
"""Inspect an actual APK; never claim a device/runtime test."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("apk", type=Path)
    parser.add_argument("--sdk", type=Path, default=os.environ.get("ANDROID_HOME"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    apk = args.apk.resolve(strict=True)
    if args.sdk is None:
        parser.error("set ANDROID_HOME or --sdk")
    sdk = Path(args.sdk)
    tools = sorted((sdk / "build-tools").glob("*/apksigner"))
    if not tools:
        parser.error("Android SDK build-tools/apksigner is required")
    signer = tools[-1]
    analyzer = sdk / "cmdline-tools/latest/bin/apkanalyzer"
    checks = {}
    commands = {
        "signature": [str(signer), "verify", "--verbose", "--print-certs", str(apk)],
        "application_id": [str(analyzer), "manifest", "application-id", str(apk)],
        "permissions": [str(analyzer), "manifest", "permissions", str(apk)],
        "manifest": [str(analyzer), "manifest", "print", str(apk)],
    }
    for name, command in commands.items():
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=90, check=False)
            checks[name] = {"ok": result.returncode == 0, "exit_code": result.returncode,
                            "stdout": result.stdout.strip(), "stderr": result.stderr.strip()}
        except (OSError, subprocess.TimeoutExpired) as exc:
            checks[name] = {"ok": False, "error": str(exc)}
    report = {"status": "PASSED" if all(c["ok"] for c in checks.values()) else "FAILED",
              "scope": "APK signature and static manifest only; no device/OCR/translation test",
              "apk": apk.name, "bytes": apk.stat().st_size,
              "sha256": hashlib.sha256(apk.read_bytes()).hexdigest(), "checks": checks}
    content = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content + "\n", encoding="utf-8")
    print(content)
    return 0 if report["status"] == "PASSED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
