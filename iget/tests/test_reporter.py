"""
Tests for iget/reporter.py — IGET v9 Reporter
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from iget.reporter import (
    build_flow,
    build_comment,
    build_inline_comments,
    build_recommendations,
    build_summary_lines,
)
from iget.scorer import classify_files, compute_score, detect_mode, get_state
from iget.config import COMMENT_MARKER, VERSION


class TestBuildFlow:
    def test_green_flow(self):
        flow = build_flow("green")
        assert len(flow) == 6
        assert all(icon in ("🟩", "🟨", "🟥") for icon in flow)

    def test_red_flow_contains_red_icon(self):
        flow = build_flow("red")
        assert "🟥" in flow

    def test_yellow_flow_contains_yellow_icon(self):
        flow = build_flow("yellow")
        assert "🟨" in flow


class TestBuildComment:
    def _make_comment(self, score=90, state="green"):
        issues = []
        summary_lines = ["- ไฟล์ที่เปลี่ยน: 2"]
        recommend = ["สามารถ merge ได้"]
        return build_comment(score, state, issues, summary_lines, recommend)

    def test_comment_contains_version(self):
        body = self._make_comment()
        assert VERSION == "9.0"
        assert f"v{VERSION}" in body
        assert body.startswith(COMMENT_MARKER)

    def test_comment_contains_score(self):
        body = self._make_comment(score=77)
        assert "77%" in body

    def test_comment_contains_sections(self):
        body = self._make_comment()
        assert "FLOW" in body
        assert "SUMMARY" in body
        assert "RISK" in body
        assert "IMPACT" in body
        assert "RECOMMEND" in body

    def test_no_risk_message_when_no_issues(self):
        body = self._make_comment(score=95, state="green")
        assert "ไม่พบความเสี่ยง" in body


class TestBuildInlineComments:
    def test_no_inline_for_docs_only(self):
        files = [{"filename": "README.md", "changes": 50}]
        c = classify_files(files)
        comments = build_inline_comments(files, c, "docs_only")
        assert len(comments) == 0

    def test_large_file_gets_inline_comment(self):
        files = [{"filename": "src/big.py", "changes": 300}]
        c = classify_files(files)
        comments = build_inline_comments(files, c, "code")
        # Should have comment about large file
        assert any("จำนวนมาก" in cm["body"] for cm in comments)

    def test_inline_capped_at_max(self):
        files = [{"filename": f"src/big_{i}.py", "changes": 300} for i in range(20)]
        c = classify_files(files)
        comments = build_inline_comments(files, c, "code")
        assert len(comments) <= 5


class TestBuildRecommendations:
    def test_docs_only_recommend(self):
        files = [{"filename": "README.md", "changes": 10}]
        c = classify_files(files)
        recs = build_recommendations(files, c, "docs_only", 10)
        assert any("สะกด" in r or "เนื้อหา" in r for r in recs)

    def test_no_test_recommend(self):
        files = [{"filename": "src/app.py", "changes": 50}]
        c = classify_files(files)
        recs = build_recommendations(files, c, "code", 50)
        assert any("test" in r.lower() for r in recs)

    def test_clean_pr_recommend(self):
        files = [
            {"filename": "src/app.py", "changes": 10},
            {"filename": "tests/test_app.py", "changes": 10},
        ]
        c = classify_files(files)
        recs = build_recommendations(files, c, "code", 20)
        assert any("merge" in r.lower() for r in recs)


class TestBuildSummaryLines:
    def test_summary_includes_counts(self):
        files = [
            {"filename": "src/app.py", "changes": 20},
            {"filename": "README.md", "changes": 5},
        ]
        c = classify_files(files)
        lines = build_summary_lines(files, c, "mixed")
        joined = "\n".join(lines)
        assert "2" in joined  # total files
        assert "25" in joined  # total changes
