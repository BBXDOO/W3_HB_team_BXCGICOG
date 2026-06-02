from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HANDBOOK = ROOT / "docs/architecture/mytec_info/W3UNIVE.md"


def test_w3unive_handbook_exists_and_is_practical_thai_technical_doc():
    doc = HANDBOOK.read_text(encoding="utf-8")

    assert "# W3UNIVE" in doc
    assert "คู่มือทางเทคนิค" in doc
    assert "refactor/v0.2" in doc
    assert "philosophy paper" in doc
    assert "ทำอย่างไร" in doc
    assert "ใช้ไฟล์ไหน" in doc
    assert "รันคำสั่งอะไร" in doc


def test_w3unive_handbook_covers_required_systems_and_boundaries():
    doc = HANDBOOK.read_text(encoding="utf-8")

    for required in (
        "W3-API",
        "Cross-X",
        "W3Lgu",
        "W3DB",
        "Hospitication",
        "G-State",
        "IGET",
        "Codex",
        "Config / Registry / Runtime",
        "REDR",
        "PSP2",
        "DTML",
        "LRC2",
    ):
        assert required in doc

    for boundary in ("mutated:false", "read-only", "plan-only", "gateway-only"):
        assert boundary in doc


def test_w3unive_handbook_links_to_real_core_paths():
    doc = HANDBOOK.read_text(encoding="utf-8")

    for link in (
        "../../../w3_api/",
        "../../../cross_x/",
        "../../../protocol/w3lgu/",
        "../../../src/w3db/",
        "../../../hospitication/",
        "../../../tools/run_hospitication.py",
        "../../../tools/w3api.py",
        "../../governance/G_STATE_PAPER.md",
        "../../../codex/",
        "../../../config/",
    ):
        assert link in doc


def test_w3unive_handbook_lists_known_commands_without_promoting_missing_w3db_tests():
    doc = HANDBOOK.read_text(encoding="utf-8")

    for command in (
        "python tools/w3_agent_ci.py",
        "python -m pytest tests/test_g_state_foundation.py",
        "python -m pytest tests/test_hospitication_runner.py",
        "python tools/run_hospitication.py",
        "python tools/w3api.py --health",
        "python -m iget.tests.test_iget_v8",
    ):
        assert command in doc

    assert "ตรวจสอบ path ก่อนใช้งาน" in doc
    assert "python SYSTEM/TESTS/w3db/test_crud.py" in doc
    assert "python SYSTEM/TESTS/w3db/test_flow.py" in doc
