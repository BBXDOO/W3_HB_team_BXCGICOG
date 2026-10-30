#!/usr/bin/env python3
"""Publish a signed, immutable translator release after CI verification."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--check-only", action="store_true", help="Verify signed APK without publishing")
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
apk = root / "app/build/outputs/apk/release/app-release.apk"
sdk = Path(os.environ["ANDROID_HOME"])
signer = sdk / "build-tools/35.0.0/apksigner"
analyzer = sdk / "cmdline-tools/latest/bin/apkanalyzer"
expected = (root / "signing-certificate-sha256.txt").read_text().strip().lower()
verified = subprocess.check_output([str(signer), "verify", "--print-certs", str(apk)], text=True)
certs = re.findall(r"Signer #\d+ certificate SHA-256 digest: ([0-9a-fA-F]{64})", verified)
if len(certs) != 1 or certs[0].lower() != expected:
    raise SystemExit("APK signing certificate differs from the installed app; publication blocked")
package = subprocess.check_output([str(analyzer), "manifest", "application-id", str(apk)], text=True).strip()
version = int(subprocess.check_output([str(analyzer), "manifest", "version-code", str(apk)], text=True).strip())
if package != "org.w3.translate.preview" or version < 3:
    raise SystemExit("Unexpected APK identity/version")
repo = os.environ["GITHUB_REPOSITORY"]
if repo != "BBXDOO/W3_HB_team_BXCGICOG":
    raise SystemExit("Unexpected release repository")
tag = f"screen-translator-v{version}"
if args.check_only:
    print(json.dumps({"status":"PASSED", "package":package, "version":version, "certificate_matches":True, "sha256":hashlib.sha256(apk.read_bytes()).hexdigest(), "bytes":apk.stat().st_size}))
    raise SystemExit(0)
# Never replace an already published release or its APK.
existing = subprocess.run(["gh", "release", "view", tag, "--repo", repo, "--json", "url"], capture_output=True, text=True)
if existing.returncode == 0:
    print("Release already exists; leaving its published files unchanged")
    raise SystemExit(0)
output = root / "app/build/update-channel"
output.mkdir(parents=True, exist_ok=True)
asset = output / f"W3-Screen-Translator-v{version}.apk"
shutil.copyfile(apk, asset)
sha = hashlib.sha256(asset.read_bytes()).hexdigest()
(output / "SHA256SUMS").write_text(f"{sha}  {asset.name}\n")
notes = output / "notes.txt"
notes.write_text(f"W3 แปลหน้าจอ รุ่นอัปเดต {version}\n\nติดตั้งอัปเดตผ่านปุ่มอัปเดตแอปในหน้าหลัก รองรับ package และกุญแจลงนามเดิม\n\nSHA-256: {sha}\n", encoding="utf-8")
subprocess.run(["gh", "release", "create", tag, str(asset), str(output / "SHA256SUMS"), "--repo", repo,
                "--target", os.environ["GITHUB_SHA"], "--prerelease", "--title", f"W3 Screen Translator v{version}", "--notes-file", str(notes)], check=True)
# Verify GitHub provides the digest that the Android client requires.
release = json.loads(subprocess.check_output(["gh", "api", f"repos/{repo}/releases/tags/{tag}"], text=True))
match = next((a for a in release.get("assets", []) if a.get("name") == asset.name), None)
if not match or match.get("digest", "").lower() != "sha256:" + sha:
    raise SystemExit("Release uploaded, but GitHub asset digest is missing/mismatched; check release before distributing")
with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as out:
    out.write("Published update: " + release["html_url"] + "\n")
