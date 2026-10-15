"""Regression checks for evidence, uncertainty, and durable defect identity."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from iget.structure_review import inspect_structure, reconcile_findings


def test_static_checks_have_proof_without_claiming_runtime_success():
    with TemporaryDirectory() as folder:
        root = Path(folder)
        file = root / 'ok.py'
        file.write_text('def work():\n    return 1\nwork()\n')
        original = file.read_bytes()
        result = inspect_structure(root, ['ok.py', 'ok.py'])
        assert file.read_bytes() == original
        assert not result['findings']
        assert result['checks'][1]['state'] == 'UNVERIFIED'
        assert result['signal']['color'] == 'yellow'
        assert result['evidence'][0]['sha256']
        assert result['proof']['trace'][-1]['semantic_tag'] == 'iget:unknown'
        assert 'work' in result['call_names']


def test_broken_json_is_observed_defect_and_repair_is_rechecked():
    with TemporaryDirectory() as folder:
        file = Path(folder) / 'data.json'
        file.write_text('{broken')
        first = inspect_structure(folder, ['data.json'])
        ledger = reconcile_findings([], first['findings'], first['checked_paths'], 'first')
        assert ledger[0]['status'] == 'OPEN'
        second = inspect_structure(folder, ['data.json'])
        again = reconcile_findings(ledger, second['findings'], second['checked_paths'], 'second')
        assert len(again) == 1 and again[0]['occurrences'] == 2
        assert ledger[0]['finding_id'] == again[0]['finding_id']
        file.write_text('{}')
        fixed = inspect_structure(folder, ['data.json'])
        resolved = reconcile_findings(again, fixed['findings'], fixed['checked_paths'], 'third')
        assert resolved[0]['status'] == 'RESOLVED'


def test_uninspected_old_defect_does_not_silently_resolve():
    old = [{'kind': 'missing_path', 'path': 'old.py'}]
    ledger = reconcile_findings(old, [], ['other.py'], 'today')
    assert ledger[0]['status'] == 'NOT_RECHECKED'


def test_old_synthetic_finding_migrates_out_of_defect_list():
    assert reconcile_findings([{'kind': 'circuit_verification_required', 'path': 'core'}], [], [], 'now') == []
