import tools.request_cycle as rc

def test_parse_request_frontmatter(tmp_path):
    p=tmp_path/"r.md"
    p.write_text("---\nrequest_id: RQ-X\ntask_keyword: design\ntarget_module: ChatGPT\nfinal_signoff_required: true\n---\n# x\n",encoding="utf-8")
    data=rc.parse_request(p)
    assert data["request_id"]=="RQ-X"
    assert data["task_keyword"]=="design"
    assert data["target_module"]=="ChatGPT"
    assert data["final_signoff_required"] is True

def test_safe_id():
    assert rc.safe_id("RQ X/1")=="RQ-X-1"


def test_parse_request_preserves_body(tmp_path):
    p=tmp_path/"r.md"
    p.write_text("---\nrequest_id: RQ-BODY\ntask_keyword: structural_review\ntarget_module: Cast\n---\n# Flow Study\nPlatform -> W3\n",encoding="utf-8")
    data=rc.parse_request(p)
    assert "# Flow Study" in data["_request_text"]
    assert "Platform -> W3" in data["_request_text"]


def test_resolve_module_name_normalizes_symbols():
    resolved, warning = rc.resolve_module_name("<copilot_gm>")
    assert resolved == "Copilot-Gm"
    assert warning is not None


def test_resolve_module_name_exact_keeps_identity():
    resolved, warning = rc.resolve_module_name("ChatGPT")
    assert resolved == "ChatGPT"
    assert warning is None


def test_resolve_module_name_unknown_returns_fallback_warning():
    resolved, warning = rc.resolve_module_name("module-loader")
    assert resolved == "module-loader"
    assert "fallback runtime contract" in str(warning)


def test_next_doc_id_rollover():
    assert rc._next_doc_id("A", 1) == ("A", 2)
    assert rc._next_doc_id("A", 50) == ("B", 1)
    assert rc._next_doc_id("Z", 50) == ("AA", 1)


def test_append_checkin_entry_rotates_after_50(monkeypatch, tmp_path):
    monkeypatch.setattr(rc, "ROOT", tmp_path)
    monkeypatch.setattr(rc, "CHECKIN_DIR", tmp_path / "logs" / "check-in")
    monkeypatch.setattr(rc, "REQUEST_LOG_DIR", tmp_path / "logs" / "request_cycle")

    first_doc = rc.CHECKIN_DIR / "CID_@R000A1.md"
    rows = ["DOCS - ID : CID_@R000A1", "", "DOCS - REQUEST CHECK-IN SHEET", "---"]
    for idx in range(1, 51):
        rows.extend(
            [
                f"• NO.{idx} : RQ-{idx}",
                "• DATE : 2026-01-01T00:00:00Z",
                "• Person : BBXDOO",
                "• Operation : ทรู",
                "• Suggestions : ok",
                "---",
            ]
        )
    first_doc.parent.mkdir(parents=True, exist_ok=True)
    first_doc.write_text("\n".join(rows) + "\n", encoding="utf-8")

    checkin = rc.append_checkin_entry(
        request_name="RQ-51",
        person="BBXDOO",
        operation=False,
        suggestions="fallback",
        timestamp="2026-01-02T00:00:00Z",
    )
    assert checkin["doc_id"] == "CID_@R000A2"
    rotated_doc = rc.CHECKIN_DIR / "CID_@R000A2.md"
    assert rotated_doc.exists()
    assert "• NO.1 : RQ-51" in rotated_doc.read_text(encoding="utf-8")


def test_select_checkin_doc_prefers_newer_series(monkeypatch, tmp_path):
    monkeypatch.setattr(rc, "ROOT", tmp_path)
    monkeypatch.setattr(rc, "CHECKIN_DIR", tmp_path / "logs" / "check-in")

    rc.CHECKIN_DIR.mkdir(parents=True, exist_ok=True)
    (rc.CHECKIN_DIR / "CID_@R000Z50.md").write_text(
        "DOCS - ID : CID_@R000Z50\n---\n• NO.1 : OLD\n---\n",
        encoding="utf-8",
    )
    (rc.CHECKIN_DIR / "CID_@R000AA1.md").write_text(
        "DOCS - ID : CID_@R000AA1\n---\n• NO.1 : NEW\n---\n",
        encoding="utf-8",
    )

    _, doc_id, next_no = rc._select_checkin_doc(rc.CHECKIN_DIR)
    assert doc_id == "CID_@R000AA1"
    assert next_no == 2
