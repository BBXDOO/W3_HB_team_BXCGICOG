import importlib.util
import sys
import types
from pathlib import Path


def load_auto_responder():
    github_stub = types.ModuleType("github")
    github_stub.Github = object
    github_stub.GithubException = Exception
    sys.modules.setdefault("github", github_stub)

    path = Path(__file__).resolve().parent / "auto_responder.py"
    spec = importlib.util.spec_from_file_location("w3_auto_responder", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_extract_module_tags_from_iget_issue_body():
    responder = load_auto_responder()
    body = """
    # IGET Issue Brief
    - @module:IGET
    - @module:W3-API
    - @module:MPCP
    - @module:IGET
    """

    assert responder.extract_module_tags(body) == ["IGET", "W3-API", "MPCP"]


def test_should_trigger_from_module_tag_without_legacy_keyword():
    responder = load_auto_responder()

    assert responder.should_trigger("Dispatch preview", "route to @module:DTML", []) is True


def test_agent_comment_acknowledges_modules_and_keeps_boundary():
    responder = load_auto_responder()

    body = responder.agent_comment_body("th", ["IGET", "W3-API"])

    assert "@module:IGET" in body
    assert "@module:W3-API" in body
    assert "BBX19" in body
    assert "Boundary:" in body
