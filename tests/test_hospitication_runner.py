from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from hospitication.signal import observer
from tools import run_hospitication as runner

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
    assert "coverage:complete_within_declared_scope" in result.stdout
    assert "unreadable_files:0" in result.stdout
    assert "unreadable_directories:0" in result.stdout


@pytest.mark.parametrize('failure', ('file', 'directory', 'both'))
def test_runner_exposes_partial_coverage_even_without_pressure_warnings(tmp_path, monkeypatch, capsys, failure):
    (tmp_path / 'ok.md').write_text('hello\n', encoding='utf-8')
    blocked = tmp_path / 'blocked.py'
    blocked.write_text('import os\n', encoding='utf-8')
    original_open = Path.open

    def limited_open(path, *args, **kwargs):
        if path == blocked and failure in ('file', 'both'):
            raise PermissionError('simulated unreadable file')
        return original_open(path, *args, **kwargs)

    def limited_walk(root, *, followlinks, onerror):
        if failure in ('directory', 'both'):
            onerror(PermissionError('simulated unreadable subtree'))
        yield str(root), [], ['ok.md', 'blocked.py']

    monkeypatch.setattr(Path, 'open', limited_open)
    monkeypatch.setattr(observer.os, 'walk', limited_walk)
    assert runner.main(['--repo', str(tmp_path)]) == 0
    output = capsys.readouterr().out
    assert 'status:completed' in output  # command completion is separate from coverage
    assert 'coverage:partial' in output
    assert f"unreadable_files:{int(failure in ('file', 'both'))}" in output
    assert f"unreadable_directories:{int(failure in ('directory', 'both'))}" in output
    assert 'skipped_entries:' in output
    assert 'incomplete_coverage:' in output
    assert 'none above warning threshold' not in output
