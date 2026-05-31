from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from hospitication.core.config import HospiticationConfig
from hospitication.core.types import NodeRef, SignalEnvelope
from hospitication.recovery.proposals import propose_recovery
from hospitication.reporter.json_report import render_json
from hospitication.reporter.markdown import render_markdown
from hospitication.signal.detector import detect_signals
from hospitication.signal.emitter import emit_signals
from hospitication.signal.observer import observe_repository
from hospitication.cli import build_report


def make_repo(tmp_path):
    (tmp_path / "core" / "memory").mkdir(parents=True)
    (tmp_path / "core" / "governance").mkdir(parents=True)
    (tmp_path / "tests").mkdir()
    (tmp_path / "core" / "memory" / "memory_bus.py").write_text(
        "import json\nimport pathlib\n# replay governance memory signal\n",
        encoding="utf-8",
    )
    (tmp_path / "core" / "governance" / "README.md").write_text(
        "governance replay recovery signal truth mpcp\n",
        encoding="utf-8",
    )
    (tmp_path / "tests" / "test_memory.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")
    return tmp_path


def test_observer_is_read_only_and_deterministic(tmp_path):
    repo = make_repo(tmp_path)
    before = sorted(path.relative_to(repo).as_posix() for path in repo.rglob("*") if path.is_file())

    first = observe_repository(repo)
    second = observe_repository(repo)

    after = sorted(path.relative_to(repo).as_posix() for path in repo.rglob("*") if path.is_file())
    assert before == after
    assert first == second
    assert tuple(file.path for file in first.files) == tuple(sorted(file.path for file in first.files))


def test_signal_envelope_and_node_are_immutable():
    envelope = SignalEnvelope(
        signal_id="sig_test",
        timestamp="1970-01-01T00:00:00Z",
        origin_node=NodeRef(1, 2),
        detector_type="drift",
        pressure="informational_drift",
        confidence=0.25,
    )

    with pytest.raises(FrozenInstanceError):
        envelope.signal_id = "sig_mutated"

    assert envelope.to_shadow()["origin_node"] == (1, 2)


def test_report_pipeline_emits_deterministic_json_and_markdown(tmp_path):
    repo = make_repo(tmp_path)
    config = HospiticationConfig(deterministic_timestamp="2026-05-28T00:00:00Z")

    first = build_report(repo, config)
    second = build_report(repo, config)

    assert render_json(first) == render_json(second)
    markdown = render_markdown(first)
    assert "# Hospitication Health Report" in markdown
    assert "Recovery Proposals" in markdown
    assert first.generated_at == second.generated_at == "2026-05-28T00:00:00Z"


def test_detector_and_recovery_boundaries_do_not_diagnose_or_mutate(tmp_path):
    repo = make_repo(tmp_path)
    report = build_report(repo)
    detections = detect_signals(report.metrics)
    signals = emit_signals(detections)
    proposals = propose_recovery(report.metrics, signals)

    for detection in detections:
        assert "recommendation" not in detection.evidence
        assert "cause" not in detection.evidence

    for proposal in proposals:
        assert proposal.status == "proposed"
        assert proposal.destructive is False
