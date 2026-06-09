from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_doc(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_branch_strategy_defines_active_base_and_truth_layers():
    doc = read_doc("docs/branch_strategy.md")

    assert "refactor/v0.2" in doc
    assert "Registry / protocol / source code = truth" in doc
    assert "Config = orientation map" in doc
    assert "No AI self-merge" in doc
    assert "Human Review" in doc
    assert "Governance Gate" in doc


def test_public_boundary_defines_public_internal_labels_and_release_flow():
    doc = read_doc("docs/public_boundary.md")

    assert "PUBLIC" in doc
    assert "INTERNAL" in doc
    assert "REVIEW" in doc
    assert "EXPERIMENTAL" in doc
    assert "main" in doc
    assert "refactor/v0.2" in doc
    assert "Registry / protocol / source code = truth" in doc
    assert "Config = orientation map" in doc
