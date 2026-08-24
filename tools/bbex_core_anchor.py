#!/usr/bin/env python3
"""Capture a BBEX perception record without executing the requested action."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.runtime.agents.bbex_core import BBEXCore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Record BBEX intent, observations, and alignment signals without execution.",
    )
    parser.add_argument("intent", help="Intent or task to preserve")
    parser.add_argument("--outcome", help="Observable desired outcome")
    parser.add_argument("--source", default="BBX19")
    parser.add_argument("--target", default="W3")
    parser.add_argument("--constraint", action="append", default=[])
    parser.add_argument("--non-goal", action="append", default=[])
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--observation", action="append", default=[])
    parser.add_argument("--support-signal", action="append", default=[])
    parser.add_argument("--drift-signal", action="append", default=[])
    parser.add_argument(
        "--structural-option",
        action="append",
        default=[],
        help="Consultation option retained only when --source is BBX19",
    )
    parser.add_argument("--output", type=Path, help="Explicit Markdown output path")
    parser.add_argument("--json", action="store_true", help="Print the record as JSON")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    core = BBEXCore(REPO_ROOT)
    record = core.capture(
        args.intent,
        source=args.source,
        target=args.target,
        intent=args.intent,
        desired_outcome=args.outcome,
        constraints=args.constraint,
        non_goals=args.non_goal,
        evidence=args.evidence,
        observations=args.observation,
        support_signals=args.support_signal,
        drift_signals=args.drift_signal,
        structural_options=args.structural_option,
    )

    if args.output:
        saved = core.save(record, args.output)
        print(f"Saved: {saved}", file=sys.stderr)

    if args.json:
        print(json.dumps(record, ensure_ascii=False, indent=2))
    else:
        print(core.render_markdown(record))

    return 0 if record["state"] == "READY_FOR_ACTION" else 2


if __name__ == "__main__":
    raise SystemExit(main())
