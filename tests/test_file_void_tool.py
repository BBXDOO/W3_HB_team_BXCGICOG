import pytest

from protocol.files_void import FileVoidError, create_void, file_void_tool
from protocol.mpcp.adapter.file_void_tool import build_file_void_stage, call_file_void_tool


def test_file_void_manifest_preserves_source_and_creates_temporary_artifact():
    record = create_void(source_ref="wx/templates/paper/fast_patch.md", source_body="hello")
    manifested = record.resolve(env="md.env", lib="markdown.lib").manifest("markdown")

    body = manifested.to_dict()
    assert body["state"] == "MANIFESTED"
    assert body["source_mutated"] is False
    assert body["invariants"]["file_void_is_artifact"] is False
    assert body["manifestation"]["temporary"] is True
    assert body["manifestation"]["write_performed"] is False
    assert body["manifestation"]["content"] == "hello"


def test_file_void_rejects_manifest_before_resolve():
    record = create_void(source_ref="BOX:TEMPLATE", source_body="x")

    with pytest.raises(FileVoidError):
        record.manifest("text")


def test_file_void_save_is_handoff_not_direct_write():
    result = file_void_tool(
        action="save",
        source_ref="BOX:TEMPLATE",
        source_body="content",
        env="text.env",
        lib="text.lib",
        artifact_type="text",
        target_ref="outcomes/append_only_ledger/FV-001.json",
        blueprint_ref="protocol/Files.void/void.runtime.spec.md",
        mpcp_task="TASK:FILE_VOID_SAVE",
    )

    assert result["state"] == "SUCCESS"
    payload = result["result"]
    assert payload["state"] == "PERSISTED"
    assert payload["source_mutated"] is False
    assert payload["manifestation"]["artifact_ref"] == "outcomes/append_only_ledger/FV-001.json"
    assert payload["manifestation"]["write_performed"] is False
    assert payload["manifestation"]["metadata"]["handoff_required"] is True
    assert result["review"] is True


def test_mpcp_adapter_can_call_file_void_from_context():
    result = call_file_void_tool(
        {
            "TASK": "manifest_cross_code",
            "ACTION": "manifest",
            "SOURCE_REF": "BOX:CROSS_L_BLOCK",
            "SOURCE_BODY": "return {state='pass'}",
            "ENV": "lua.env",
            "LIB": "lua.lib",
            "ARTIFACT_TYPE": "lua",
        }
    )

    assert result["state"] == "SUCCESS"
    assert result["cause"] == "manifest_cross_code"
    assert result["result"]["state"] == "MANIFESTED"
    assert result["result"]["manifestation"]["artifact_type"] == "lua"


def test_mpcp_pillar_stage_shape_returns_success_payload():
    stage = build_file_void_stage("manifest")
    result = stage(
        None,
        {
            "TASK": "file_void_stage",
            "SOURCE_REF": "BOX:FAST_PATCH",
            "SOURCE_BODY": "patch candidate",
            "ARTIFACT_TYPE": "markdown",
        },
    )

    assert result["state"] == "SUCCESS"
    assert result["result"]["state"] == "MANIFESTED"
