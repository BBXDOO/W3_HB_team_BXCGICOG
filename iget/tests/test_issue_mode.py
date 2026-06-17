from iget.issue_mode import IssueBrief, build_issue_body, suggest_modules


def test_suggest_modules_from_brief_keywords():
    modules = suggest_modules(
        "IGET v10 issue dispatch",
        "IGET reads an issue and routes W3-API, DTML, W3DB, and MPCP with approval",
    )

    assert "IGET" in modules
    assert "W3-API" in modules
    assert "DTML" in modules
    assert "W3DB" in modules
    assert "MPCP" in modules


def test_suggest_modules_preserves_explicit_order_and_uniqueness():
    modules = suggest_modules("repo audit", "audit docs", explicit=("DTML", "IGET", "DTML"))

    assert modules[0:2] == ("DTML", "IGET")
    assert modules.count("DTML") == 1


def test_build_issue_body_contains_w3_contract():
    brief = IssueBrief(
        title="IGET v10 issue dispatch",
        brief="Create a GitHub issue from a BBX19 brief",
        modules=("IGET", "W3-API"),
    )

    body = build_issue_body(brief)

    assert "# IGET Issue Brief" in body
    assert "Source: BBX19" in body
    assert "Mode: issue_dispatch" in body
    assert "Status: waiting_triage" in body
    assert "@module:IGET" in body
    assert "@module:W3-API" in body
    assert "without BBX19 approval" in body
