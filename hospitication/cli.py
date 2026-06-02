"""Command-line entrypoint for Hospitication."""

from __future__ import annotations

import argparse
from pathlib import Path

from hospitication.core.config import HospiticationConfig
from hospitication.core.registry import default_registry
from hospitication.core.types import HealthReport
from hospitication.recovery.proposals import propose_recovery
from hospitication.reporter.json_report import render_json
from hospitication.reporter.markdown import render_markdown
from hospitication.signal.detector import detect_signals
from hospitication.signal.emitter import emit_signals
from hospitication.signal.observer import observe_repository


def build_report(repo_root: str | Path, config: HospiticationConfig | None = None) -> HealthReport:
    cfg = config or HospiticationConfig()
    snapshot = observe_repository(repo_root, cfg)
    registry = default_registry()
    metrics = tuple(analyzer(snapshot) for analyzer in registry.analyzers())
    detections = detect_signals(metrics)
    signals = emit_signals(detections, cfg)
    proposals = propose_recovery(metrics, signals)
    summary = _summary(metrics, signals, proposals)
    return HealthReport(
        generated_at=cfg.deterministic_timestamp,
        repo_root=snapshot.repo_root,
        metrics=metrics,
        signals=signals,
        proposals=proposals,
        summary=summary,
    )


def render_report(report: HealthReport, output_format: str) -> str:
    if output_format == "json":
        return render_json(report)
    if output_format == "markdown":
        return render_markdown(report)
    raise ValueError(f"Unsupported report format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="hospitication",
        description="Observe W3 structural health and propose non-mutating recovery.",
    )
    parser.add_argument("--repo", default=".", help="Repository root to observe")
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Report format",
    )
    parser.add_argument("--output", help="Optional output file. Defaults to stdout.")
    parser.add_argument(
        "--timestamp",
        default=None,
        help="Deterministic report timestamp. Defaults to config timestamp.",
    )
    args = parser.parse_args(argv)

    config = HospiticationConfig(
        deterministic_timestamp=args.timestamp or HospiticationConfig().deterministic_timestamp
    )
    report = build_report(args.repo, config)
    rendered = render_report(report, args.format)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


def _summary(metrics, signals, proposals) -> str:
    if not metrics:
        return "No metrics produced."
    highest = max(metrics, key=lambda metric: (metric.score, metric.name))
    return (
        f"Highest pressure: {highest.name}={highest.score:.4f}; "
        f"signals={len(signals)}; proposals={len(proposals)}."
    )


if __name__ == "__main__":
    raise SystemExit(main())
