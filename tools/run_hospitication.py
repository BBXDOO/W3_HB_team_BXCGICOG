#!/usr/bin/env python3
"""Read-only Hospitication runner for check/evaluation use.

The runner observes repository health and prints a concise report. It never
repairs, deletes, rewrites, or mutates repository truth.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from hospitication.cli import build_report  # noqa: E402
from hospitication.core.config import HospiticationConfig  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="run_hospitication",
        description="Run a read-only Hospitication health check and print a concise summary.",
    )
    parser.add_argument("--repo", default=".", help="Repository root to observe")
    parser.add_argument(
        "--timestamp",
        default=HospiticationConfig().deterministic_timestamp,
        help="Deterministic timestamp for reproducible reports",
    )
    args = parser.parse_args(argv)

    try:
        report = build_report(
            args.repo,
            HospiticationConfig(deterministic_timestamp=args.timestamp),
        )
    except Exception as exc:  # Runner failure only; Hospitication remains non-mutating.
        print("status:runner_failed")
        print("mutated:false")
        print("observation:not repair")
        print(f"error:{type(exc).__name__}: {exc}")
        return 1

    warnings = [
        metric for metric in sorted(report.metrics, key=lambda item: item.score, reverse=True)
        if metric.score >= 0.5
    ]
    recommendations = tuple(report.proposals[:3])

    print("status:completed")
    print("mutated:false")
    print("observation:not repair")
    print(f"repo:{report.repo_root}")
    print(f"checked_areas:files={len(report.metrics)} metrics, signals={len(report.signals)}, proposals={len(report.proposals)}")
    print(f"overall_pressure:{report.overall_score:.4f}")
    print(f"summary:{report.summary}")
    print("warnings_risks:")
    if warnings:
        for metric in warnings[:5]:
            print(f"- {metric.name}:{metric.score:.4f} {metric.summary}")
    else:
        print("- none above warning threshold")
    print("recommendations:")
    if recommendations:
        for proposal in recommendations:
            print(f"- {proposal.title} ({proposal.status}, destructive:{proposal.destructive})")
    else:
        print("- continue observation; no recovery proposal required")
    print("boundary:Hospitication observes/evaluates/proposes only; no auto-repair")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
