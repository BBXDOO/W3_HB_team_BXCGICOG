"""Regression checks for the IGET v9 GitHub Actions wiring."""

from pathlib import Path


WORKFLOW = (Path(__file__).resolve().parents[2] / ".github" / "workflows" / "iget.yml").read_text(
    encoding="utf-8"
)


def test_workflow_identifies_v9_and_runs_trusted_base_code():
    assert "name: IGET v9" in WORKFLOW
    assert "pull_request_target:" in WORKFLOW
    assert "github.event.pull_request.base.sha || github.sha" in WORKFLOW
    assert "persist-credentials: false" in WORKFLOW


def test_manual_dispatch_requires_pr_number():
    assert "workflow_dispatch:" in WORKFLOW
    assert "pr_number:" in WORKFLOW
    assert "required: true" in WORKFLOW
    assert "github.event.pull_request.number || inputs.pr_number" in WORKFLOW


def test_workflow_has_comment_permissions_and_disables_inline_by_default():
    assert "pull-requests: write" in WORKFLOW
    assert "issues: write" in WORKFLOW
    assert 'IGET_INLINE_COMMENTS: "false"' in WORKFLOW
    assert "python -m pytest iget/tests -q" in WORKFLOW
