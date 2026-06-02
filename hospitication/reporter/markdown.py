"""Deterministic markdown report rendering."""

from __future__ import annotations

from hospitication.core.types import HealthReport


def render_markdown(report: HealthReport) -> str:
    lines: list[str] = [
        "# Hospitication Health Report",
        "",
        f"- Generated at: `{report.generated_at}`",
        f"- Repository: `{report.repo_root}`",
        f"- Overall pressure score: `{report.overall_score:.4f}`",
        f"- Summary: {report.summary}",
        "",
        "## Metrics",
        "",
        "| Metric | Score | Summary |",
        "| --- | ---: | --- |",
    ]
    for metric in sorted(report.metrics, key=lambda item: item.name):
        lines.append(f"| `{metric.name}` | `{metric.score:.4f}` | {metric.summary} |")

    lines.extend(["", "## Signals", ""])
    if report.signals:
        lines.append("| Signal | Type | Pressure | Confidence | Node |")
        lines.append("| --- | --- | --- | ---: | --- |")
        for signal in sorted(report.signals, key=lambda item: item.signal_id):
            node = f"({signal.origin_node.x},{signal.origin_node.y})"
            lines.append(
                f"| `{signal.signal_id}` | `{signal.detector_type}` | `{signal.pressure}` | "
                f"`{signal.confidence:.4f}` | `{node}` |"
            )
    else:
        lines.append("No signals emitted above threshold.")

    lines.extend(["", "## Recovery Proposals", ""])
    if report.proposals:
        for proposal in sorted(report.proposals, key=lambda item: item.proposal_id):
            lines.extend(
                [
                    f"### {proposal.title}",
                    "",
                    f"- ID: `{proposal.proposal_id}`",
                    f"- Status: `{proposal.status}`",
                    f"- Destructive: `{proposal.destructive}`",
                    f"- Rationale: {proposal.rationale}",
                    "- Actions:",
                ]
            )
            for action in proposal.actions:
                lines.append(f"  - {action}")
            if proposal.target_paths:
                lines.append("- Target paths:")
                for path in proposal.target_paths:
                    lines.append(f"  - `{path}`")
            lines.append("")
    else:
        lines.append("No recovery proposals required. Recovery layer did not mutate truth.")

    lines.append("_Hospitication observes, detects, emits, evaluates, and proposes; it does not mutate truth._")
    return "\n".join(lines).rstrip() + "\n"
