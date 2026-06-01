from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_doc(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_g_state_paper_defines_awareness_not_execution():
    doc = read_doc("docs/governance/G_STATE_PAPER.md")

    assert "A shared awareness layer" in doc
    assert "What condition are we currently operating under?" in doc
    assert "G-State must not:" in doc
    assert "execute tasks" in doc
    assert "override ROT" in doc
    assert "override Paper" in doc
    assert "mutate runtime directly" in doc
    assert "Awareness does not grant authority." in doc
    assert "Awareness creates responsibility." in doc


def test_g_state_paper_declares_canonical_states_and_integration_boundaries():
    doc = read_doc("docs/governance/G_STATE_PAPER.md")

    for state in (
        "GSTATE:BUILD",
        "GSTATE:AUDIT",
        "GSTATE:RESEARCH",
        "GSTATE:RECOVERY",
        "GSTATE:MAINTENANCE",
        "GSTATE:LEARNING",
    ):
        assert state in doc

    for system in ("ROT", "Paper", "Modew", "Condien", "W3Lgu", "IGET", "Hospitication"):
        assert f"`{system}`" in doc

    for hook in ("GSTATE_META", "GSTATE_PROFILE", "GSTATE_FEEDBACK"):
        assert hook in doc


def test_g_state_examples_are_human_readable_and_non_runtime():
    examples = sorted((ROOT / "examples/gstate").glob("*.gstate"))

    assert {example.name for example in examples} == {
        "audit.gstate",
        "build.gstate",
        "recovery.gstate",
    }
    for example in examples:
        text = example.read_text(encoding="utf-8")
        assert text.startswith("GSTATE:")
        assert "CONDITION:" in text
        assert "AWARENESS:" in text
        assert "BOUNDARY:" in text
        assert "RESPONSIBILITY:" in text
        assert "not " in text.lower()


def test_v0_2_to_v0_3_readiness_locks_truth_and_gateway_boundaries():
    doc = read_doc("docs/reports/V0_2_TO_V0_3_READINESS.md")

    assert "Registry / protocol / source code" in doc
    assert "Config" in doc
    assert "Orientation map" in doc
    assert "W3-API" in doc
    assert "Gateway-only" in doc
    assert "Cross-X" in doc
    assert "Plan-only" in doc
    assert "EP_SIGNAL / RYTM" in doc
    assert "Preview / signal trace" in doc
    assert "refactor/v0.2" in doc
    assert "main" in doc
