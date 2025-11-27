#!/usr/bin/env python3
"""
Validate YAML front-matter for required metadata fields in Markdown files.

Checks for:
- index-id (required for requirements)
- version-id (required for directives/decisions)
- approved-by (if present must be non-empty)
- reason (if approved-by present, reason required)

Exit non-zero on validation failures so Action fails.
"""

import sys
import argparse
import re
from pathlib import Path
import yaml

FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)

REQUIRED_FIELDS = {
    "BBX19/decisions": ["version-id", "approved-by", "reason"],
    "BBX19/directives": ["version-id"],
    "BBX19": ["index-id"],
}

def extract_front_matter(text):
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except Exception:
        return {}

def validate_file(path: Path):
    text = path.read_text(encoding="utf-8")
    fm = extract_front_matter(text)
    errors = []
    # Determine required fields by path
    pstr = str(path).replace("\\", "/")
    for key, fields in REQUIRED_FIELDS.items():
        if pstr.startswith(key):
            for f in fields:
                if f not in fm or fm.get(f) in (None, ""):
                    errors.append(f"Missing or empty '{f}' in {pstr}")
    # Additional rules
    if "approved-by" in fm and fm.get("approved-by"):
        if not fm.get("reason"):
            errors.append(f"'approved-by' present but missing 'reason' in {pstr}")
    return errors

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paths", nargs="+", required=True, help="Glob paths to check")
    args = ap.parse_args()
    all_errors = []
    for pattern in args.paths:
        for p in Path(".").glob(pattern):
            if p.is_file():
                errs = validate_file(p)
                if errs:
                    all_errors.extend(errs)
    if all_errors:
        print("Metadata validation failed:")
        for e in all_errors:
            print(" -", e)
        sys.exit(1)
    print("Metadata validation passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
