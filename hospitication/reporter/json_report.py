"""Deterministic JSON report rendering."""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any

from hospitication.core.types import HealthReport
from hospitication.signal.envelopes import signal_to_dict


def report_to_dict(report: HealthReport) -> dict[str, Any]:
    return {
        "generated_at": report.generated_at,
        "repo_root": report.repo_root,
        "summary": report.summary,
        "overall_score": report.overall_score,
        "metrics": [asdict(metric) for metric in sorted(report.metrics, key=lambda item: item.name)],
        "signals": [signal_to_dict(signal) for signal in sorted(report.signals, key=lambda item: item.signal_id)],
        "proposals": [asdict(proposal) for proposal in sorted(report.proposals, key=lambda item: item.proposal_id)],
    }


def render_json(report: HealthReport) -> str:
    return json.dumps(report_to_dict(report), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
