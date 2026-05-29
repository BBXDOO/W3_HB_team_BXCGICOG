import importlib.util
import json
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from codex import build_execution_packet, load_manifest, validate_manifest


def test_codex_manifest_declares_non_overlapping_governance_boundaries():
    manifest = load_manifest()

    assert validate_manifest(manifest) == []
    assert manifest["class"] == "implementation_executor"
    assert manifest["boundaries"]["human_review_required"] is True
    assert manifest["boundaries"]["governance_gate_required"] is True
    assert manifest["boundaries"]["no_truth_mutation"] is True
    assert manifest["boundaries"]["no_self_merge"] is True
    assert "approve_truth" in manifest["forbidden_authority"]
    assert "merge_pr" in manifest["forbidden_authority"]


def test_codex_execution_packet_is_five_line_w3lgu_and_immutable():
    packet = build_execution_packet(
        "create adapter gateway",
        source="BBX19",
        target="W3-API",
        mode="implementation",
        timestamp="2026-05-29T00:00:00Z",
        event_id="codex-test",
    )

    lines = packet.w3lgu.splitlines()
    assert packet.id == "codex-test"
    assert packet.status == "ready_for_human_review"
    assert len(lines) == 5
    assert lines[0].startswith("MEM:")
    assert lines[1].startswith("PATCH:")
    assert lines[2].startswith("LAW:")
    assert lines[3].startswith("EVENT:")
    assert lines[4].startswith("SIGNAL:")
    assert packet.governance["human_review_required"] is True
    assert packet.governance["truth_mutation_allowed"] is False

    with pytest.raises(FrozenInstanceError):
        packet.status = "merged"  # type: ignore[misc]


def test_codex_registered_in_module_loader_and_central_registry():
    loader_path = Path("core/module-loader/router.py")
    spec = importlib.util.spec_from_file_location("w3_module_loader_router", loader_path)
    assert spec is not None and spec.loader is not None
    router = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(router)

    plan = router.execution_plan("implementation")
    assert plan["run_with"] == "Codex"
    assert plan["role"] == "Implementation Agent / Repo Executor"
    assert plan["status"] == "ACTIVE"

    central = json.loads(Path("modules/registry.json").read_text(encoding="utf-8"))
    assert central["routing"]["implementation"] == "Codex"
    assert any(module["name"] == "Codex" for module in central["modules"])


def test_codex_idp_and_module_json_reference_each_other():
    idp = json.loads(Path("core/module-loader/identity/Codex.idp.json").read_text(encoding="utf-8"))
    module = json.loads(Path("modules/Codex/module.json").read_text(encoding="utf-8"))
    manifest = json.loads(Path("codex/modules.json").read_text(encoding="utf-8"))

    assert idp["schema"] == "W3-IDP"
    assert idp["version"] == "2.0"
    assert idp["module"] == "Codex"
    assert module["idp_ref"] == "BBX19/modules/BBX19/idp/IDP-V2.0/Codex-IDP.md"
    assert manifest["idp_ref"] == module["idp_ref"]
    assert Path(module["idp_ref"]).exists()
