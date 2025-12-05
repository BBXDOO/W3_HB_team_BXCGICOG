#!/usr/bin/env python3
"""
Runtime Log Validation Script for W3 Hybrid Engine
===================================================

This script validates the runtime log file (logs/engine/runtime.log)
by parsing each line as JSON and verifying that required fields exist.

Required fields (per event):
- event_id
- event_type
- timestamp
- level
- source
- message
"""

import json
import sys
from pathlib import Path
from typing import List, Tuple

# Required fields for each log event
REQUIRED_FIELDS = [
    "event_id",
    "event_type",
    "timestamp",
    "level",
    "source",
    "message",
]


def validate_log_entry(entry: dict, line_number: int) -> List[str]:
    """
    Validate a single log entry.

    Returns a list of error messages (empty if valid).
    """
    errors = []
    for field in REQUIRED_FIELDS:
        if field not in entry:
            errors.append(f"Line {line_number}: Missing required field '{field}'")
    return errors


def validate_runtime_log(log_path: str) -> Tuple[int, int, List[str]]:
    """
    Validate the runtime log file.

    Returns:
        - total_lines: Number of lines processed
        - valid_lines: Number of valid lines
        - errors: List of error messages
    """
    errors = []
    total_lines = 0
    valid_lines = 0

    try:
        with open(log_path, "r", encoding="utf-8") as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue  # Skip empty lines

                total_lines += 1

                try:
                    entry = json.loads(line)
                except json.JSONDecodeError as e:
                    errors.append(f"Line {line_number}: Invalid JSON - {e}")
                    continue

                entry_errors = validate_log_entry(entry, line_number)
                if entry_errors:
                    errors.extend(entry_errors)
                else:
                    valid_lines += 1

    except FileNotFoundError:
        errors.append(f"Log file not found: {log_path}")
    except Exception as e:
        errors.append(f"Error reading log file: {e}")

    return total_lines, valid_lines, errors


def main() -> int:
    """Main entry point for the validation script."""
    # Get the repository root directory
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    log_path = repo_root / "logs" / "engine" / "runtime.log"

    print("=" * 60)
    print("W3 Runtime Log Validation")
    print("=" * 60)
    print()
    print(f"Log file: {log_path}")
    print()

    if not log_path.exists():
        print("Log file does not exist yet. Validation skipped.")
        print("Run the W3 engine to generate log entries.")
        return 0

    total_lines, valid_lines, errors = validate_runtime_log(str(log_path))

    print(f"Total entries: {total_lines}")
    print(f"Valid entries: {valid_lines}")
    print()

    if errors:
        print("VALIDATION FAILED")
        print("-" * 40)
        for error in errors:
            print(f"  ❌ {error}")
        print()
        print(f"Total errors: {len(errors)}")
        return 1
    else:
        print("✅ VALIDATION PASSED")
        print("-" * 40)
        print("All log entries comply with the runtime log schema.")
        print()
        print("Validated fields:")
        for field in REQUIRED_FIELDS:
            print(f"  • {field}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
