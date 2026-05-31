from __future__ import annotations

import json
import subprocess
import sys


def test_cli_json_stdout(tmp_path):
    (tmp_path / "README.md").write_text("memory replay governance signal recovery\n", encoding="utf-8")
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "hospitication.cli",
            "--repo",
            str(tmp_path),
            "--format",
            "json",
            "--timestamp",
            "2026-05-28T00:00:00Z",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(completed.stdout)
    assert payload["generated_at"] == "2026-05-28T00:00:00Z"
    assert payload["metrics"]
    assert payload["repo_root"] == str(tmp_path.resolve())


def test_cli_output_file(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "module.py").write_text("import json\n", encoding="utf-8")
    output = tmp_path / "report.md"

    subprocess.run(
        [
            sys.executable,
            "-m",
            "hospitication.cli",
            "--repo",
            str(repo),
            "--format",
            "markdown",
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert output.exists()
    assert output.read_text(encoding="utf-8").startswith("# Hospitication Health Report")
