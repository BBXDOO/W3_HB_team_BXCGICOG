from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_hospitication_runner_is_callable_and_read_only():
    result = subprocess.run(
        [
            sys.executable,
            "tools/run_hospitication.py",
            "--repo",
            ".",
            "--timestamp",
            "2026-06-01T00:00:00Z",
        ],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0
    assert "status:completed" in result.stdout
    assert "mutated:false" in result.stdout
    assert "observation:not repair" in result.stdout
    assert "warnings_risks:" in result.stdout
    assert "recommendations:" in result.stdout
    assert "no auto-repair" in result.stdout
