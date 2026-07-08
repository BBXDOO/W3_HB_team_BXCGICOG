from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from argparse import Namespace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / "tools/w3api.py"


def load_tool():
    spec = importlib.util.spec_from_file_location("w3api_tool", TOOL_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_w3api_tool_builds_cross_payload_from_cli_args():
    tool = load_tool()
    args = Namespace(
        source="termux",
        intent="review",
        target="W3",
        mode="cross",
        focus="system",
        contract="observe_only",
        payload_json=json.dumps({"extra": "ok"}),
    )

    payload = tool.build_payload(args)

    assert payload["source"] == "termux"
    assert payload["intent"] == "review"
    assert payload["target"] == "W3"
    assert payload["mode"] == "cross"
    assert payload["payload"] == {
        "extra": "ok",
        "focus": "system",
        "contract": "observe_only",
    }


def test_w3api_tool_render_markdown_preserves_gateway_boundaries():
    tool = load_tool()
    markdown = tool.render_markdown(
        {
            "id": "demo",
            "status": "accepted",
            "w3lgu": "MEM:SOURCE:termux",
            "signal": {
                "mutated": False,
                "w3db": {"mode": "append_plan_only"},
                "ep_signal": {"mode": "preview_only"},
            },
        }
    )

    assert "Mutated: `false`" in markdown
    assert "W3DB mode: `append_plan_only`" in markdown
    assert "EP_SIGNAL mode: `preview_only`" in markdown
    assert "gateway-only" in markdown


def test_w3api_write_md_uses_build_payload_and_render_markdown(tmp_path, monkeypatch):
    tool = load_tool()
    out = tmp_path / "out.md"
    captured = {}

    def fake_post_json(url, payload):
        captured["payload"] = payload
        return {
            "id": "demo",
            "status": "accepted",
            "w3lgu": "ok",
            "signal": {"mutated": False, "w3db": {"mode": "append_plan_only"}, "ep_signal": {"mode": "preview_only"}},
        }

    monkeypatch.setattr(tool, "post_json", fake_post_json)
    monkeypatch.setattr(sys, "argv", [
        "tools/w3api.py",
        "--source", "termux",
        "--intent", "review",
        "--target", "W3",
        "--mode", "cross",
        "--write-md", str(out),
    ])

    assert tool.main() == 0
    assert captured["payload"]["source"] == "termux"
    assert captured["payload"]["intent"] == "review"
    assert out.exists()
    assert "# W3-API Cross Gateway Result" in out.read_text(encoding="utf-8")


def test_w3api_tool_help_is_callable():
    result = subprocess.run(
        [sys.executable, "tools/w3api.py", "--help"],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0
    assert "--write-md" in result.stdout
    assert "--health" in result.stdout
