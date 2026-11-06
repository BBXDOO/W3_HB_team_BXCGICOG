from dataclasses import replace
import json
import subprocess
import sys

import pytest

from hospitication.analysis.dependency_fatigue import analyze_dependency_fatigue
from hospitication.cli import build_report
from hospitication.core.config import HospiticationConfig
from hospitication.core.types import MetricScore
from hospitication.reporter.json_report import render_json
from hospitication.signal.detector import detect_signals
from hospitication.signal.observer import observe_repository


def put(root, name, content):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return path


def test_binary_and_external_prototype_do_not_change_w3_metrics(tmp_path):
    put(tmp_path, 'core/module.py', b'import json\n')
    before = build_report(tmp_path)
    put(tmp_path, 'branding/image.jpg', b'\xff\xd8' + b'\n' * 600)
    put(tmp_path, 'fake.py', b'\x00' + b'\n' * 600)
    put(tmp_path, 'bad.md', b'\xff\xfe')
    put(tmp_path, 'w3_tool_store/xrea/huge.py', b'import json\n' * 600)
    after = build_report(tmp_path)
    assert after.metrics == before.metrics
    scope = after.observation_scope
    assert scope.observed_files == 1
    assert dict(scope.skipped_entries) == {
        'binary_files': 1, 'excluded_directories': 1,
        'non_utf8_files': 1, 'unsupported_files': 1,
    }
    included = build_report(tmp_path, HospiticationConfig(excluded_paths=()))
    assert included.observation_scope.observed_files == 2
    assert included.metrics != after.metrics


def test_scope_boundaries_are_exact_and_overrides_reach_analyzers(tmp_path):
    put(tmp_path, 'w3_tool_store/xrea/tool.py', b'import json\n')
    put(tmp_path, 'w3_tool_store/xrea_extra/tool.py', b'import pathlib\n')
    put(tmp_path, 'data.custom', b'hello\n')
    cfg = replace(HospiticationConfig(), config_extensions=('.custom',))
    report = build_report(tmp_path, cfg)
    metrics = {metric.name: metric for metric in report.metrics}
    assert metrics['cognitive_cost'].evidence['config_files'] == 1
    assert report.observation_scope.observed_files == 2
    assert report.observation_scope.config_extensions == ('.custom',)


def test_symlinks_are_not_observed_and_large_files_are_counted(tmp_path):
    root = tmp_path / 'repo'
    root.mkdir()
    outside = put(tmp_path, 'outside.py', b'import os\n')
    (root / 'link.py').symlink_to(outside)
    (root / 'linkdir').symlink_to(tmp_path, target_is_directory=True)
    put(root, 'too-large.md', b'a' * 11)
    put(root, 'ok.md', b'hello')
    snapshot = observe_repository(root, replace(HospiticationConfig(), max_file_bytes=10))
    assert [file.path for file in snapshot.files] == ['ok.md']
    assert dict(snapshot.scope.skipped_entries) == {
        'oversized_files': 1, 'symlink_directories': 1, 'symlink_files': 1,
    }


def test_missing_root_is_not_a_successful_empty_scan(tmp_path):
    with pytest.raises(ValueError, match='not a directory'):
        observe_repository(tmp_path / 'missing')
    result = subprocess.run([sys.executable, 'tools/run_hospitication.py', '--repo', str(tmp_path / 'missing')],
                            capture_output=True, text=True)
    assert result.returncode == 1
    assert 'status:runner_failed' in result.stdout


def test_non_python_code_cannot_dilute_python_import_metric(tmp_path):
    put(tmp_path, 'module.py', b'import json\n')
    before = analyze_dependency_fatigue(observe_repository(tmp_path))
    for index in range(12):
        put(tmp_path, f'source{index}.mjs', b'import fs from "node:fs";\n')
    after = analyze_dependency_fatigue(observe_repository(tmp_path))
    assert before.score == after.score
    assert after.evidence['code_files'] == 1
    assert after.evidence['unmeasured_code_files'] == 12


def test_single_snapshot_does_not_claim_temporal_oscillation():
    names = ('cognitive_cost', 'dependency_fatigue', 'recovery_resistance', 'replay_complexity', 'semantic_pressure')
    metrics = tuple(MetricScore(name=name, score=score, summary='fixture')
                    for name, score in zip(names, (1, 0, 1, 0, 1)))
    signals = detect_signals(metrics)
    assert signals
    assert all(signal.detector_type != 'oscillation' for signal in signals)


def test_semantic_and_replay_terms_reach_metric_evidence(tmp_path):
    put(tmp_path, 'README.md', b'truth signal recovery protocol outcome ledger event trace checkpoint\n')
    report = build_report(tmp_path)
    metrics = {metric.name: metric for metric in report.metrics}
    assert metrics['semantic_pressure'].evidence['semantic_marker_hits'] == 6
    assert metrics['replay_complexity'].evidence['replay_marker_hits'] == 5


def test_cli_scope_and_prototype_opt_in_are_explicit(tmp_path):
    put(tmp_path, 'module.py', b'import json\n')
    put(tmp_path, 'w3_tool_store/xrea/tool.py', b'import os\n')
    command = [sys.executable, '-m', 'hospitication.cli', '--repo', str(tmp_path), '--format', 'json']
    default = json.loads(subprocess.check_output(command, text=True))
    opted_in = json.loads(subprocess.check_output(command + ['--include-prototypes'], text=True))
    assert default['observation_scope']['observed_files'] == 1
    assert opted_in['observation_scope']['observed_files'] == 2
    assert default['observation_scope']['version'] == '0.2.0'
    assert 'single_snapshot' in default['measurement_basis']
    assert render_json(build_report(tmp_path)) == render_json(build_report(tmp_path))


@pytest.mark.parametrize('excluded', ('..', '/tmp', '.', 'a/../../b', 'a\\b'))
def test_invalid_exclusions_are_rejected(tmp_path, excluded):
    with pytest.raises(ValueError, match='repository-relative'):
        observe_repository(tmp_path, HospiticationConfig(excluded_paths=(excluded,)))


@pytest.mark.parametrize('limit', (0, -1, True))
def test_invalid_file_limits_are_rejected(tmp_path, limit):
    with pytest.raises(ValueError, match='positive integer'):
        observe_repository(tmp_path, HospiticationConfig(max_file_bytes=limit))
