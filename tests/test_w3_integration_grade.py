from __future__ import annotations

import json
import subprocess
import sys

from core.semantic_router import interpret_hospitication_report
from hospitication.cli import build_report
from hospitication.core.config import HospiticationConfig
from hospitication.reporter.json_report import render_json
from hospitication.w3db_adapter import store_hospitication_report_to_w3db
from integrations.ep_signal_w3db import store_ep_signal_to_w3db
from protocol.EP_SIGNAL.ep_signal_adapter import from_ep_signal, to_ep_signal
from scripts.enforce_layer_separation import evaluate_paths, load_hospitication_signals
from src.w3db.store import W3DBStore


def test_ep_signal_to_w3db_flow_creates_trace_records():
    store = W3DBStore()
    ep_signal = to_ep_signal("0011010110111000")

    result = store_ep_signal_to_w3db(ep_signal, store=store)

    assert from_ep_signal(ep_signal) == "0011010110111000"
    assert store.read_xiz(result.xiz_id) is not None
    assert store.read_tuf(result.tuf_id) is not None
    assert store.read_fbd(result.fbd_id) is not None
    assert store.read_prx(result.prx_id) is not None
    assert result.output["xiz"] == result.xiz_id


def test_hospitication_report_signals_append_to_w3db(tmp_path):
    (tmp_path / "README.md").write_text("memory replay governance signal recovery\n", encoding="utf-8")
    report = build_report(
        tmp_path,
        HospiticationConfig(deterministic_timestamp="2026-05-29T00:00:00Z", emit_threshold=0.0),
    )
    store = W3DBStore()

    results = store_hospitication_report_to_w3db(report, store=store)

    assert len(results) == len(report.signals)
    assert len(store.list_xiz()) == len(report.signals)
    assert all(store.read_prx(result.prx_id) is not None for result in results)


def test_layer_enforcement_signal_bridge_downgrades_red_to_yellow(tmp_path):
    source = tmp_path / "core" / "bad.py"
    source.parent.mkdir()
    source.write_text("# execute recovery must not mutate truth\n", encoding="utf-8")

    without_signal = evaluate_paths((str(source),))
    with_signal = evaluate_paths((str(source),), hospitication_signals=({"signal_id": "sig"},))

    assert without_signal[0].severity == "RED"
    assert with_signal[0].severity == "YELLOW"
    assert with_signal[0].adjusted_by_signal is True
    assert "docs/standards/referencing_standard.md" in with_signal[0].references


def test_layer_cli_accepts_hospitication_signals(tmp_path):
    target = tmp_path / "core" / "bad.py"
    target.parent.mkdir()
    target.write_text("# overwrite truth\n", encoding="utf-8")
    signals = tmp_path / "signals.json"
    signals.write_text(json.dumps({"signals": [{"signal_id": "sig"}]}), encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/enforce_layer_separation.py",
            "--json",
            "--ci-mode",
            "--hospitication-signals",
            str(signals),
            str(target),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)

    assert payload["violations"][0]["severity"] == "YELLOW"
    assert load_hospitication_signals(str(signals))[0]["signal_id"] == "sig"


def test_semantic_router_interpret_hospitication_report_records_w3db():
    store = W3DBStore()

    agent = interpret_hospitication_report("hospitication-report.json", store=store)

    assert agent.module_name in {"Gemini", "Cast"}
    assert len(store.list_xiz()) == 1
    assert len(store.list_prx()) == 1
    assert store.list_tuf()[0].final in {"0", "0.5", "1"}


def test_hospitication_json_can_feed_layer_bridge(tmp_path):
    (tmp_path / "README.md").write_text("memory replay governance signal recovery\n", encoding="utf-8")
    report = build_report(tmp_path, HospiticationConfig(emit_threshold=0.0))
    report_file = tmp_path / "report.json"
    report_file.write_text(render_json(report), encoding="utf-8")

    signals = load_hospitication_signals(str(report_file))

    assert len(signals) == len(report.signals)
