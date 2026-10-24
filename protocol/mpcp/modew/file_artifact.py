"""Concrete text equipment: template → File.void → external artifact writer.

The host supplies an output root when registering the Modew. File.void itself
still never writes final storage. Existing artifacts are never overwritten.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path, PurePosixPath
from string import Template

from protocol.files_void import create_void
from .base_modew import BaseModew


class FileVoidTextModew(BaseModew):
    def __init__(self, output_root: Path):
        super().__init__()
        self.output_root = Path(output_root).resolve()
        self.wrote = False

    def stage_D_process(self, data):
        content = data.get("CONTENT")
        if not isinstance(content, dict) or set(content) != {"template", "values", "target"}:
            raise ValueError("TEXT_LIB: template,values,target required")
        template, values, target = content["template"], content["values"], content["target"]
        if not isinstance(template, str) or not isinstance(values, dict):
            raise ValueError("TEXT_LIB: invalid template or values")
        if not all(isinstance(k, str) and isinstance(v, str) for k, v in values.items()):
            raise ValueError("TEXT_LIB: values must be text")
        if not isinstance(target, str) or not target or "\\" in target:
            raise ValueError("TEXT_LIB: relative target required")
        relative = PurePosixPath(target)
        if relative.is_absolute() or any(p in {".", "..", ""} for p in target.split("/")):
            raise ValueError("TEXT_LIB: unsafe target")
        if relative.suffix not in {".md", ".txt"}:
            raise ValueError("TEXT_LIB: only markdown/text supported")
        path = self.output_root / str(relative)
        if not path.resolve().is_relative_to(self.output_root):
            raise ValueError("TEXT_LIB: target outside host root")
        for parent in (path, *path.parents):
            if parent == self.output_root:
                break
            if parent.is_symlink():
                raise ValueError("TEXT_LIB: symlink target prohibited")
        original = create_void(source_ref=f"PAPER:{data['PAPER_ID']}:template", source_body=template,
                               env="text.env", lib="template-text.lib")
        manifestation = original.resolve().manifest(
            "markdown" if relative.suffix == ".md" else "text",
            resolver=lambda record: Template(record.source_body).substitute(values),
        )
        handoff = manifestation.persist(target_ref=target, mpcp_task=data["TASK"])
        body = handoff.manifestation.content.encode("utf-8")
        path.parent.mkdir(parents=True, exist_ok=True)
        # This writer is separate from File.void and only acts under a host grant.
        with path.open("xb") as stream:
            self.wrote = True
            stream.write(body)
            stream.flush()
            os.fsync(stream.fileno())
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != hashlib.sha256(body).hexdigest():
            raise ValueError("TEXT_LIB: written artifact mismatch")
        self._file_void = handoff.to_dict()
        return {"artifact": {"path": str(relative), "sha256": digest, "bytes": len(body)},
                "file_void": self._file_void, "writer": "external_text_writer", "write_performed": True}

    def run(self):
        self.wrote = False
        result = super().run()
        result["mutated"] = self.wrote
        return result


def verify_text_artifact(root: Path, paper: dict, result: dict) -> dict:
    """Recompute intended content, not just a producer-reported file hash."""
    try:
        expected = paper["CONTENT"]
        body = Template(expected["template"]).substitute(expected["values"]).encode("utf-8")
        artifact = result["result"]["artifact"]
        path = (Path(root).resolve() / expected["target"]).resolve()
        passed = (path.is_relative_to(Path(root).resolve()) and path.is_file()
                  and artifact["path"] == expected["target"] and path.read_bytes() == body
                  and hashlib.sha256(body).hexdigest() == artifact["sha256"])
        return {"passed": passed, "check": "intended_content_and_artifact_hash"}
    except (KeyError, TypeError, ValueError, OSError):
        return {"passed": False, "check": "intended_content_and_artifact_hash"}
