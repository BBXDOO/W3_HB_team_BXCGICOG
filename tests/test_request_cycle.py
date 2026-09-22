import json
from pathlib import Path
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
