from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "docs/standards/AGENT_SELF_WORKSPACE_STANDARD.md"
EXAMPLES = ROOT / "examples/agent_self_workspace"


def test_agent_self_workspace_standard_exists_and_defines_scope():
    doc = STANDARD.read_text(encoding="utf-8")

    assert "Agent Self Workspace Standard" in doc
    assert "workspace standard" in doc
    assert "ไม่ใช่ runtime engine" in doc
    assert "ไม่ใช่ runtime engine, workflow executor, state machine" in doc
    assert "MUTATION_ALLOWED:false" in doc
    assert "registry / protocol / source code" in doc


def test_agent_self_workspace_standard_covers_core_self_work_needs():
    doc = STANDARD.read_text(encoding="utf-8")

    for phrase in (
        "ออกแบบโมดูลตัวเอง",
        "บันทึกบริบทตัวเอง",
        "จัดสรรงานในพื้นที่ตัวเอง",
        "วางแผนและส่งต่อ",
        "Responsibility Routing",
        "Handoff",
    ):
        assert phrase in doc


def test_agent_self_workspace_templates_are_human_readable_and_non_runtime():
    expected = {
        "SELF_DESIGN.md",
        "CONTEXT_LOG.md",
        "WORK_ALLOCATOR.md",
        "PLAN.md",
    }

    assert expected == {path.name for path in EXAMPLES.glob("*.md")}
    for path in EXAMPLES.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        assert "MUTATION_ALLOWED:false" in text or "MUTATION_ALLOWED" in text
        assert "executor" not in text.lower() or "ไม่" in text
