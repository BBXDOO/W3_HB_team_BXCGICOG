"""
Tests for iget/scorer.py — IGET v9 Scoring Engine
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from iget.scorer import classify_files, compute_score, detect_mode, get_state


# ──────────────────────────────────────────────────────────────
# classify_files
# ──────────────────────────────────────────────────────────────

class TestClassifyFiles:
    def test_code_file_detected(self):
        files = [{"filename": "src/app.py", "changes": 10}]
        c = classify_files(files)
        assert len(c["code"]) == 1

    def test_doc_file_detected(self):
        files = [{"filename": "README.md", "changes": 5}]
        c = classify_files(files)
        assert len(c["doc"]) == 1

    def test_test_file_detected_by_path(self):
        files = [{"filename": "tests/test_app.py", "changes": 20}]
        c = classify_files(files)
        assert len(c["test"]) == 1

    def test_test_file_detected_by_suffix(self):
        files = [{"filename": "app_test.go", "changes": 10}]
        c = classify_files(files)
        assert len(c["test"]) == 1

    def test_spec_file_detected(self):
        files = [{"filename": "src/__tests__/app.spec.js", "changes": 15}]
        c = classify_files(files)
        assert len(c["test"]) == 1

    def test_risky_file_detected(self):
        files = [{"filename": "config/credentials.yml", "changes": 5}]
        c = classify_files(files)
        assert len(c["risky"]) == 1

    def test_risky_doc_not_flagged(self):
        # A markdown file mentioning "token" in a docs folder
        files = [{"filename": "docs/token-guide.md", "changes": 5}]
        c = classify_files(files)
        assert len(c["risky"]) == 0

    def test_workflow_file_detected(self):
        files = [{"filename": ".github/workflows/ci.yml", "changes": 10}]
        c = classify_files(files)
        assert len(c["workflow"]) == 1

    def test_multiple_categories(self):
        files = [
            {"filename": "src/app.py", "changes": 50},
            {"filename": "README.md", "changes": 10},
            {"filename": "tests/test_app.py", "changes": 30},
        ]
        c = classify_files(files)
        assert len(c["code"]) == 1  # only src/app.py; tests/test_app.py is in 'test'
        assert len(c["doc"]) == 1
        assert len(c["test"]) == 1


# ──────────────────────────────────────────────────────────────
# detect_mode
# ──────────────────────────────────────────────────────────────

class TestDetectMode:
    def test_docs_only(self):
        files = [{"filename": "README.md", "changes": 10}]
        c = classify_files(files)
        assert detect_mode(files, c) == "docs_only"

    def test_code_mode(self):
        files = [{"filename": "src/app.py", "changes": 50}]
        c = classify_files(files)
        assert detect_mode(files, c) == "code"

    def test_mixed_mode(self):
        files = [
            {"filename": "src/app.py", "changes": 50},
            {"filename": "README.md", "changes": 10},
        ]
        c = classify_files(files)
        assert detect_mode(files, c) == "mixed"

    def test_empty_pr(self):
        files = []
        c = classify_files(files)
        assert detect_mode(files, c) == "empty"


# ──────────────────────────────────────────────────────────────
# compute_score
# ──────────────────────────────────────────────────────────────

class TestComputeScore:
    def test_perfect_small_pr_with_tests(self):
        files = [
            {"filename": "src/auth.py", "changes": 30},
            {"filename": "tests/test_auth.py", "changes": 20},
        ]
        c = classify_files(files)
        mode = detect_mode(files, c)
        score, issues = compute_score(files, c, mode)
        # Should score high: small PR + has tests
        assert score >= 85

    def test_code_without_tests_penalised(self):
        files = [
            {"filename": "src/app.py", "changes": 60},
            {"filename": "src/utils.py", "changes": 40},
        ]
        c = classify_files(files)
        mode = detect_mode(files, c)
        score, issues = compute_score(files, c, mode)
        assert any("test" in i.lower() for i in issues)
        assert score < 100

    def test_risky_file_deduction(self):
        files = [{"filename": "config/credentials.yml", "changes": 5}]
        c = classify_files(files)
        mode = detect_mode(files, c)
        score, issues = compute_score(files, c, mode)
        assert score <= 70
        assert any("เสี่ยง" in i for i in issues)

    def test_docs_only_bonus(self):
        files = [
            {"filename": "README.md", "changes": 20},
            {"filename": "docs/guide.md", "changes": 10},
        ]
        c = classify_files(files)
        mode = detect_mode(files, c)
        score, issues = compute_score(files, c, mode)
        assert score >= 85
        assert any("Documentation" in i for i in issues)

    def test_very_large_pr_penalised(self):
        files = [{"filename": f"src/mod_{i}.py", "changes": 20} for i in range(20)]
        c = classify_files(files)
        mode = detect_mode(files, c)
        score, issues = compute_score(files, c, mode)
        assert score < 85
        assert any("PR ใหญ่" in i for i in issues)

    def test_score_clamped_0_to_100(self):
        # Extremely risky PR
        files = [
            {"filename": f"secret_key_{i}.py", "changes": 500} for i in range(30)
        ]
        c = classify_files(files)
        mode = detect_mode(files, c)
        score, _ = compute_score(files, c, mode)
        assert 0 <= score <= 100

    def test_small_pr_safety_bonus(self):
        files = [{"filename": "src/fix.py", "changes": 5}]
        c = classify_files(files)
        # No tests — would normally penalise, but small PR bonus offsets some
        mode = detect_mode(files, c)
        score, _ = compute_score(files, c, mode)
        # Should not go to red just for one tiny file
        assert score >= 60

    def test_workflow_file_penalised(self):
        files = [{"filename": ".github/workflows/deploy.yml", "changes": 30}]
        c = classify_files(files)
        mode = detect_mode(files, c)
        score, issues = compute_score(files, c, mode)
        assert any("workflow" in i.lower() for i in issues)


# ──────────────────────────────────────────────────────────────
# get_state
# ──────────────────────────────────────────────────────────────

class TestGetState:
    def test_green_at_threshold(self):
        assert get_state(85) == "green"
        assert get_state(100) == "green"

    def test_yellow_at_threshold(self):
        assert get_state(60) == "yellow"
        assert get_state(84) == "yellow"

    def test_red_below_threshold(self):
        assert get_state(0) == "red"
        assert get_state(59) == "red"
