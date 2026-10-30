#!/usr/bin/env python3
"""Restore one private signing JSON secret without exposing its contents."""
import base64
import json
import os
from pathlib import Path

raw = os.environ.get("INPUT_SIGNING_JSON", "")
if not raw:
    with open(os.environ["GITHUB_OUTPUT"], "a") as out:
        out.write("ready=false\n")
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as out:
        out.write("APK publishing skipped: configure W3_TRANSLATOR_SIGNING_JSON once. Build/test artifacts are separate.\n")
    raise SystemExit(0)
try:
    config = json.loads(raw)
    fields = {k: config[k] for k in ("keystore_base64", "store_password", "key_alias", "key_password")}
    if any(not isinstance(v, str) or not v or "\n" in v or "\r" in v for v in fields.values()):
        raise ValueError("Invalid signing configuration")
    # The complete JSON is masked by GitHub; also mask its individual values.
    for name in ("store_password", "key_alias", "key_password", "keystore_base64"):
        print("::add-mask::" + fields[name])
    keyfile = Path(os.environ["RUNNER_TEMP"]) / "w3-translator-signing.p12"
    keyfile.write_bytes(base64.b64decode(fields["keystore_base64"], validate=True))
    keyfile.chmod(0o600)
    with open(os.environ["GITHUB_ENV"], "a") as out:
        for name, value in {
            "W3_RELEASE_KEYSTORE_FILE": str(keyfile),
            "W3_RELEASE_STORE_PASSWORD": fields["store_password"],
            "W3_RELEASE_KEY_ALIAS": fields["key_alias"],
            "W3_RELEASE_KEY_PASSWORD": fields["key_password"],
        }.items():
            out.write(name + "=" + value + "\n")
    with open(os.environ["GITHUB_OUTPUT"], "a") as out:
        out.write("ready=true\n")
except Exception:
    raise SystemExit("Signing configuration is invalid; no secret values were logged")
