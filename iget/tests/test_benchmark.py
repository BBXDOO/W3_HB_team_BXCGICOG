"""
Tests for iget/benchmark.py — IGET v9 Benchmark Engine
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from iget.benchmark import run_benchmark, format_benchmark_report, BENCHMARK_PROFILES


class TestRunBenchmark:
    def test_all_profiles_have_results(self):
        results = run_benchmark()
        assert len(results) == len(BENCHMARK_PROFILES)

    def test_result_fields_present(self):
        results = run_benchmark()
        for r in results:
            assert "profile" in r
            assert "score" in r
            assert "state" in r
            assert "issues" in r
            assert "mode" in r

    def test_scores_in_valid_range(self):
        results = run_benchmark()
        for r in results:
            assert 0 <= r["score"] <= 100

    def test_states_are_valid(self):
        results = run_benchmark()
        for r in results:
            assert r["state"] in ("green", "yellow", "red")

    def test_risky_profile_scores_red_or_low(self):
        results = run_benchmark()
        risky = next(r for r in results if r["profile"] == "risky-secret")
        assert risky["score"] < 70

    def test_docs_only_scores_green(self):
        results = run_benchmark()
        docs = next(r for r in results if r["profile"] == "docs-only")
        assert docs["state"] == "green"

    def test_feature_with_tests_scores_high(self):
        results = run_benchmark()
        ft = next(r for r in results if r["profile"] == "feature-with-tests")
        assert ft["score"] >= 80

    def test_large_pr_scores_lower(self):
        results = run_benchmark()
        large = next(r for r in results if r["profile"] == "very-large-pr")
        normal = next(r for r in results if r["profile"] == "tiny-fix")
        assert large["score"] < normal["score"]


class TestFormatBenchmarkReport:
    def test_report_is_string(self):
        results = run_benchmark()
        report = format_benchmark_report(results)
        assert isinstance(report, str)

    def test_report_contains_table_header(self):
        results = run_benchmark()
        report = format_benchmark_report(results)
        assert "Profile" in report
        assert "Score" in report

    def test_report_contains_all_profiles(self):
        results = run_benchmark()
        report = format_benchmark_report(results)
        for p in BENCHMARK_PROFILES:
            assert p["name"] in report
