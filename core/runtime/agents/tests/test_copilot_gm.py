from core.runtime.agents.copilot_gm import CopilotGmAgent


def test_execute_no_doc_text_needs_revision():
    agent = CopilotGmAgent()
    out = agent.execute(
        task="review origin notes alignment",
        plan={"min_coverage": 0.5, "responsibilities": ["governance check"]},
        context={"target": "Origin"},
    )
    assert out["status"] == "REVIEW_REQUIRED"
    assert out["traceable"] is True
    assert "continuity" in out


def test_execute_partial_doc_text_default_threshold_completed():
    agent = CopilotGmAgent()
    out = agent.execute(
        task="review policy doc",
        plan={},  # default min_coverage = 0.5
        context={"doc_text": "This proposal improves governance and compliance."},
    )
    assert out["status"] == "COMPLETED"
    assert out["result"]["coverage_ratio"] >= 0.5


def test_execute_strict_threshold_needs_revision():
    agent = CopilotGmAgent()
    out = agent.execute(
        task="review structural policy",
        plan={"min_coverage": 1.0},
        context={"doc_text": "governance and policy only"},
    )
    assert out["status"] == "REVIEW_REQUIRED"
    assert out["result"]["min_coverage"] == 1.0


def test_invalid_packet_fails_safe_without_exception():
    out = CopilotGmAgent().execute("review", None, "invalid")

    assert out["status"] == "REVIEW_REQUIRED"
    assert out["decision"] == "invalid_review_input"
    assert out["mutated"] is False


def test_structured_review_material_is_normalized():
    out = CopilotGmAgent().execute(
        "review",
        {},
        {"doc_text": {"policy": "governance", "checks": ["compliance"]}},
    )

    assert out["status"] == "COMPLETED"
    assert out["details"]["evidence_type"] == "dict"
    assert out["details"]["merge_performed"] is False


def test_api_payload_evidence_is_reviewable():
    out = CopilotGmAgent().execute(
        "governance",
        {},
        {"payload": {"evidence": "governance policy compliance"}},
    )

    assert out["status"] == "COMPLETED"


def test_threshold_zero_cannot_complete_empty_review():
    out = CopilotGmAgent().execute(
        "review", {"min_coverage": 0}, {"doc_text": "unrelated material"}
    )

    assert out["status"] == "REVIEW_REQUIRED"
    assert out["result"]["min_coverage"] == 0.25


def test_continuity_packet_does_not_claim_persistence():
    out = CopilotGmAgent().execute(
        "review", {}, {"doc_text": "governance policy compliance"}
    )

    assert out["continuity"]["persisted"] is False
    assert out["continuity"]["persistence_owner"] == "dispatcher_or_storage_layer"
    assert out["evidence"][0]["evidence_class"] == "input_evidence"
