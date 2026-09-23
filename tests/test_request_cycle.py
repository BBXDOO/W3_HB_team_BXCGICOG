import json
from concurrent.futures import ThreadPoolExecutor

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
    assert warning == "normalized target_module '<copilot_gm>' -> 'Copilot-Gm'"


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


def test_append_checkin_entry_concurrent_unique_rows(monkeypatch, tmp_path):
    monkeypatch.setattr(rc, "ROOT", tmp_path)
    monkeypatch.setattr(rc, "CHECKIN_DIR", tmp_path / "logs" / "check-in")
    monkeypatch.setattr(rc, "REQUEST_LOG_DIR", tmp_path / "logs" / "request_cycle")

    def _run(index: int):
        return rc.append_checkin_entry(
            request_name=f"RQ-{index}",
            person="BBXDOO",
            operation=True,
            suggestions="ok",
            timestamp="2026-01-02T00:00:00Z",
        )

    with ThreadPoolExecutor(max_workers=4) as pool:
        entries = list(pool.map(_run, range(1, 9)))

    row_numbers = sorted(entry["entry_no"] for entry in entries)
    assert row_numbers == list(range(1, 9))


def test_append_checkin_entry_serializes_suggestions_and_keeps_entry_numbers(monkeypatch, tmp_path):
    monkeypatch.setattr(rc, "ROOT", tmp_path)
    monkeypatch.setattr(rc, "CHECKIN_DIR", tmp_path / "logs" / "check-in")
    monkeypatch.setattr(rc, "REQUEST_LOG_DIR", tmp_path / "logs" / "request_cycle")

    first = rc.append_checkin_entry(
        request_name="RQ-1",
        person="BBXDOO",
        operation=True,
        suggestions="line1\n• NO.99 : fake",
        timestamp="2026-01-01T00:00:00Z",
    )
    second = rc.append_checkin_entry(
        request_name="RQ-2",
        person="BBXDOO",
        operation=True,
        suggestions="ok",
        timestamp="2026-01-01T00:10:00Z",
    )

    assert first["entry_no"] == 1
    assert second["entry_no"] == 2
    content = (rc.CHECKIN_DIR / "CID_@R000A1.md").read_text(encoding="utf-8")
    assert "• Suggestions : \"line1\\n• NO.99 : fake\"" in content


def test_process_backfills_evidence_for_existing_completed_result(monkeypatch, tmp_path):
    monkeypatch.setattr(rc, "ROOT", tmp_path)
    monkeypatch.setattr(rc, "REQUESTS", tmp_path / "requests")
    monkeypatch.setattr(rc, "RESULTS", tmp_path / "requests" / "results")
    monkeypatch.setattr(rc, "EVENTS", tmp_path / "repo_events")
    monkeypatch.setattr(rc, "CHECKIN_DIR", tmp_path / "logs" / "check-in")
    monkeypatch.setattr(rc, "REQUEST_LOG_DIR", tmp_path / "logs" / "request_cycle")
    monkeypatch.setattr(rc, "resolve_module_name", lambda target: ("ChatGPT", None))
    monkeypatch.setattr(rc, "_identity_or_none", lambda _: {"display_name": "ChatGPT", "status": "active", "responsibilities": []})

    request_path = tmp_path / "requests" / "RQ-100.md"
    request_path.parent.mkdir(parents=True, exist_ok=True)
    request_path.write_text(
        "---\nrequest_id: RQ-100\ntask_keyword: design\ntarget_module: ChatGPT\nrequester: BBXDOO\n---\n# x\n",
        encoding="utf-8",
    )
    rc.RESULTS.mkdir(parents=True, exist_ok=True)
    result_path = rc.RESULTS / "RQ-100_RESULT.json"
    result_path.write_text(
        json.dumps(
            {
                "request_id": "RQ-100",
                "runtime_result": {"status": "COMPLETED", "output": {"summary": "done"}, "time": "2026-01-01T00:00:00Z"},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    response = rc.process(request_path)
    assert response["status"] == "SKIPPED"
    assert response["evidence_backfilled"] is True

    saved = json.loads(result_path.read_text(encoding="utf-8"))
    assert saved["checkin"]["path"].startswith("logs/check-in/")
    assert saved["request_log"].startswith("logs/request_cycle/")
    assert (tmp_path / saved["checkin"]["path"]).exists()
    assert (tmp_path / saved["request_log"]).exists()
    request_log_content = (tmp_path / saved["request_log"]).read_text(encoding="utf-8")
    assert "- target_module: `ChatGPT`" in request_log_content
    assert '{"summary": "done"}' in request_log_content


def test_process_backfill_is_single_writer_under_concurrency(monkeypatch, tmp_path):
    monkeypatch.setattr(rc, "ROOT", tmp_path)
    monkeypatch.setattr(rc, "REQUESTS", tmp_path / "requests")
    monkeypatch.setattr(rc, "RESULTS", tmp_path / "requests" / "results")
    monkeypatch.setattr(rc, "EVENTS", tmp_path / "repo_events")
    monkeypatch.setattr(rc, "CHECKIN_DIR", tmp_path / "logs" / "check-in")
    monkeypatch.setattr(rc, "REQUEST_LOG_DIR", tmp_path / "logs" / "request_cycle")
    monkeypatch.setattr(rc, "resolve_module_name", lambda target: ("ChatGPT", None))
    monkeypatch.setattr(rc, "_identity_or_none", lambda _: {"display_name": "ChatGPT", "status": "active", "responsibilities": []})

    request_path = tmp_path / "requests" / "RQ-101.md"
    request_path.parent.mkdir(parents=True, exist_ok=True)
    request_path.write_text(
        "---\nrequest_id: RQ-101\ntask_keyword: design\ntarget_module: ChatGPT\nrequester: BBXDOO\n---\n# x\n",
        encoding="utf-8",
    )
    rc.RESULTS.mkdir(parents=True, exist_ok=True)
    result_path = rc.RESULTS / "RQ-101_RESULT.json"
    result_path.write_text(
        json.dumps(
            {
                "request_id": "RQ-101",
                "runtime_result": {"status": "COMPLETED", "output": {"summary": "done"}, "time": "2026-01-01T00:00:00Z"},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(lambda _: rc.process(request_path), range(2)))

    assert sum(1 for item in responses if item.get("evidence_backfilled") is True) == 1

    saved = json.loads(result_path.read_text(encoding="utf-8"))
    checkin_path = tmp_path / saved["checkin"]["path"]
    request_log_path = tmp_path / saved["request_log"]
    assert checkin_path.exists()
    assert request_log_path.exists()
    checkin_content = checkin_path.read_text(encoding="utf-8")
    assert checkin_content.count("• NO.") == 1


def test_process_backfill_skips_when_status_not_completed(monkeypatch, tmp_path):
    monkeypatch.setattr(rc, "ROOT", tmp_path)
    monkeypatch.setattr(rc, "REQUESTS", tmp_path / "requests")
    monkeypatch.setattr(rc, "RESULTS", tmp_path / "requests" / "results")
    monkeypatch.setattr(rc, "EVENTS", tmp_path / "repo_events")
    monkeypatch.setattr(rc, "CHECKIN_DIR", tmp_path / "logs" / "check-in")
    monkeypatch.setattr(rc, "REQUEST_LOG_DIR", tmp_path / "logs" / "request_cycle")
    monkeypatch.setattr(rc, "resolve_module_name", lambda target: ("ChatGPT", None))
    monkeypatch.setattr(rc, "_identity_or_none", lambda _: {"display_name": "ChatGPT", "status": "active", "responsibilities": []})
    monkeypatch.setattr(rc, "already_done", lambda _rid: True)

    request_path = tmp_path / "requests" / "RQ-102.md"
    request_path.parent.mkdir(parents=True, exist_ok=True)
    request_path.write_text(
        "---\nrequest_id: RQ-102\ntask_keyword: design\ntarget_module: ChatGPT\nrequester: BBXDOO\n---\n# x\n",
        encoding="utf-8",
    )
    rc.RESULTS.mkdir(parents=True, exist_ok=True)
    result_path = rc.RESULTS / "RQ-102_RESULT.json"
    result_path.write_text(
        json.dumps(
            {
                "request_id": "RQ-102",
                "runtime_result": {"status": "FAILED", "error": "boom", "time": "2026-01-01T00:00:00Z"},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    response = rc.process(request_path)
    assert response["status"] == "SKIPPED"
    assert response["evidence_backfilled"] is False
    assert not list((tmp_path / "logs" / "check-in").glob("*.md"))


def test_process_event_uses_target_module_and_executed_by(monkeypatch, tmp_path):
    monkeypatch.setattr(rc, "ROOT", tmp_path)
    monkeypatch.setattr(rc, "REQUESTS", tmp_path / "requests")
    monkeypatch.setattr(rc, "RESULTS", tmp_path / "requests" / "results")
    monkeypatch.setattr(rc, "EVENTS", tmp_path / "repo_events")
    monkeypatch.setattr(rc, "CHECKIN_DIR", tmp_path / "logs" / "check-in")
    monkeypatch.setattr(rc, "REQUEST_LOG_DIR", tmp_path / "logs" / "request_cycle")
    monkeypatch.setattr(rc, "resolve_module_name", lambda target: ("ChatGPT", None))
    monkeypatch.setattr(rc, "_identity_or_none", lambda _: {"display_name": "ChatGPT", "status": "active", "responsibilities": []})
    monkeypatch.setattr(rc, "route_task", lambda _: {"assigned_module": "ChatGPT"})
    monkeypatch.setattr(rc, "build_context", lambda *_args, **_kwargs: {"trace_id": "trace-1"})
    monkeypatch.setattr(rc, "dispatch", lambda *_args, **_kwargs: {"status": "COMPLETED", "summary": "done", "mutated": False, "artifacts": []})
    monkeypatch.setattr(rc, "validate_agent_result", lambda *_args, **_kwargs: {"ok": True})
    monkeypatch.setattr(rc, "add_memory", lambda **_kwargs: None)

    request_path = tmp_path / "requests" / "RQ-200.md"
    request_path.parent.mkdir(parents=True, exist_ok=True)
    request_path.write_text(
        "---\nrequest_id: RQ-200\ntask_keyword: design\ntarget_module: ChatGPT\nrequester: BBXDOO\n---\n# x\n",
        encoding="utf-8",
    )

    rc.process(request_path)

    event_path = tmp_path / "repo_events" / "RQ-200_EXECUTION.md"
    event_content = event_path.read_text(encoding="utf-8")
    assert "- target_module: `ChatGPT`" in event_content
    assert "- requested_target_module: `ChatGPT`" in event_content
    assert "- executed_by: `ChatGPT`" in event_content


def test_pending_allows_routing_without_target_module(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(rc, "ROOT", tmp_path)
    monkeypatch.setattr(rc, "REQUESTS", tmp_path / "requests")

    rc.REQUESTS.mkdir(parents=True, exist_ok=True)
    valid = rc.REQUESTS / "valid.md"
    invalid = rc.REQUESTS / "invalid.md"
    valid.write_text(
        "---\nrequest_id: RQ-OK\ntask_keyword: design\ntarget_module: ChatGPT\n---\n",
        encoding="utf-8",
    )
    invalid.write_text(
        "---\nrequest_id: RQ-BAD\ntask_keyword: design\n---\n",
        encoding="utf-8",
    )

    processed = []

    def fake_process(path):
        processed.append(path.name)
        return {"status": "COMPLETED", "request": path.name}

    monkeypatch.setattr(rc, "process", fake_process)
    monkeypatch.setattr("sys.argv", ["request_cycle.py", "--pending"])

    try:
        rc.main()
    except SystemExit as exc:
        assert exc.code == 0

    capsys.readouterr()
    assert processed == ["invalid.md", "valid.md"]
