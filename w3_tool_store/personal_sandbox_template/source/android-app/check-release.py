"""Fail an APK build when its bundled manual/version is absent or inconsistent."""
import hashlib
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parent
assets = root / 'app/src/main/assets/www'
info = json.loads((assets / 'release-info.json').read_text())
manual = (assets / 'user-guide.md').read_bytes()
gradle = (root / 'app/build.gradle').read_text()
assert info['schema'] == 'w3.sandbox.manual-release.v1', 'unknown manual manifest'
assert info['versionCode'] == int(re.search(r'versionCode (\d+)', gradle)[1]), 'manual and APK version differ'
assert info['versionName'] == re.search(r"versionName '([^']+)'", gradle)[1], 'manual version name differs'
assert info['manualSha256'] == hashlib.sha256(manual).hexdigest(), 'manual checksum differs'
assert f"<!-- reviewed-version: {info['versionCode']} -->" in manual.decode(), 'manual not reviewed for this version'
assert f"<!-- manual-version: {info['versionCode']} -->" in manual.decode(), 'wrong guide version'
for menu in info['menus']:
    assert f'<!-- menu: {menu} -->' in manual.decode(), f'missing menu {menu}'
# Check that the current web bundle actually embeds the same guide and version.
bundles = '\n'.join(p.read_text() for p in (assets / 'assets').glob('*.js'))
assert f"manual-version: {info['versionCode']}" in bundles, 'guide is not in the application bundle'
assert info['manualSha256'] and info['sourceSha256'], 'review fingerprint missing'
print(f"APK manual v{info['versionCode']}: manifest, checksum, sections and bundled guide passed")
