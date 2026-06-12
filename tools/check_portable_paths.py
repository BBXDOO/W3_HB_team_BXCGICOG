#!/usr/bin/env python3
"""Reject Git paths that cannot be checked out reliably on Windows.

Run from any directory inside the repository. The check reads Git's tracked path
list rather than the current filesystem so trailing spaces and other unusual
names cannot be hidden by platform normalization.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import PurePosixPath

FORBIDDEN = set('<>:"\\|?*')
RESERVED = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}


def tracked_paths() -> list[str]:
    output = subprocess.check_output(
        ["git", "ls-files", "-z"],
        stderr=subprocess.DEVNULL,
    )
    return [item.decode("utf-8", "surrogateescape") for item in output.split(b"\0") if item]


def path_problems(path: str) -> list[str]:
    problems: list[str] = []
    for component in PurePosixPath(path).parts:
        if component.endswith((" ", ".")):
            problems.append(f"component ends with a space or period: {component!r}")
        illegal = sorted(FORBIDDEN.intersection(component))
        if illegal:
            problems.append(f"component contains Windows-reserved characters {illegal}: {component!r}")
        if any(ord(character) < 32 for character in component):
            problems.append(f"component contains a control character: {component!r}")
        stem = component.split(".", 1)[0].upper()
        if stem in RESERVED:
            problems.append(f"component uses a Windows device name: {component!r}")
    return problems


def case_collisions(paths: list[str]) -> list[str]:
    groups: dict[str, list[str]] = {}
    for path in paths:
        groups.setdefault(path.casefold(), []).append(path)
    return [
        "case-insensitive collision: " + ", ".join(repr(path) for path in values)
        for values in groups.values()
        if len(values) > 1
    ]


def main() -> int:
    try:
        paths = tracked_paths()
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: cannot read tracked Git paths: {exc}", file=sys.stderr)
        return 2

    failures: list[str] = []
    for path in paths:
        failures.extend(f"{path!r}: {problem}" for problem in path_problems(path))
    failures.extend(case_collisions(paths))

    if failures:
        print("Windows-incompatible tracked paths detected:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Portable path check passed for {len(paths)} tracked paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
