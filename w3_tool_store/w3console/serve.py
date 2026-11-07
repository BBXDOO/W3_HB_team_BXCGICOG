"""Serve the console and a read-only Git snapshot on the device."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import subprocess
from urllib.parse import parse_qs, urlsplit

from flow import build_flow

APP = Path(__file__).resolve().parent
ROOT = APP.parents[1]
FILE_LIMIT = 512 * 1024
PORT = 8765
ASSETS = {"/": ("index.html", "text/html"), "/repo.js": ("repo.js", "text/javascript"),
          "/repo.css": ("repo.css", "text/css")}


class Repo:
    def __init__(self, root, revision):
        self.root = root
        self.revision = self.git("rev-parse", "--verify", "--end-of-options", revision + "^{commit}").decode().strip()
        self.files = {}
        entries = self.git("ls-tree", "-rlz", self.revision)
        for entry in entries.split(b"\0"):
            if not entry:
                continue
            header, filename = entry.split(b"\t", 1)
            mode, kind, oid, size = header.decode("ascii").split()
            if mode in ("100644", "100755") and kind == "blob":
                try:
                    self.files[filename.decode("utf-8")] = (oid, int(size))
                except UnicodeDecodeError:
                    continue

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args], capture_output=True,
                              check=True, timeout=20).stdout

    def read(self, filename):
        oid, size = self.files[filename]
        if size > FILE_LIMIT:
            raise ValueError("ไฟล์เกินขนาดที่เปิดได้ (512 KiB)")
        raw = self.git("cat-file", "blob", oid)
        if b"\0" in raw:
            raise ValueError("ไฟล์ไบนารี")
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            raise ValueError("รองรับไฟล์ข้อความ UTF-8") from None


def evidence_for(repo, evidence_path):
    try:
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        if (evidence["kind"] != "w3console-croll-run/v1"
                or evidence["revision"] != repo.revision
                or evidence["status"] not in ("PASS", "FAIL", "TIMEOUT")
                or not isinstance(evidence["output"], str)
                or not isinstance(evidence["time"], str)):
            return None
        return evidence
    except (OSError, ValueError, KeyError, TypeError):
        return None


def handler_for(repo, port, evidence_path):
    class Handler(BaseHTTPRequestHandler):
        def send(self, status, kind, body):
            self.send_response(status)
            self.send_header("Content-Type", kind + "; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)

        def json(self, status, value):
            self.send(status, "application/json", json.dumps(value, ensure_ascii=False).encode())

        def do_GET(self):
            if self.headers.get("Host") not in (f"127.0.0.1:{port}", f"localhost:{port}"):
                self.json(403, {"error": "เปิดได้จากเครื่องนี้เท่านั้น"})
                return
            url = urlsplit(self.path)
            try:
                if url.path in ASSETS:
                    path, kind = ASSETS[url.path]
                    self.send(200, kind, (APP / path).read_bytes())
                elif url.path == "/api/repo":
                    self.json(200, {"revision": repo.revision, "files": sorted(repo.files)})
                elif url.path == "/api/flow":
                    self.json(200, {"steps": build_flow(repo), "run": evidence_for(repo, evidence_path)})
                elif url.path == "/api/file":
                    name = parse_qs(url.query).get("path", [""])[0]
                    self.json(200, {"path": name, "text": repo.read(name)})
                else:
                    self.json(404, {"error": "ไม่พบรายการ"})
            except KeyError:
                self.json(404, {"error": "ไม่พบไฟล์ใน Git revision นี้"})
            except ValueError as error:
                self.json(422, {"error": str(error)})
            except (OSError, subprocess.SubprocessError):
                self.json(503, {"error": "เปิดข้อมูล Git ไม่สำเร็จ"})

    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--ref", default="HEAD")
    parser.add_argument("--port", type=int, default=PORT)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("port ต้องอยู่ระหว่าง 1 ถึง 65535")
    repo = Repo(args.root.resolve(), args.ref)
    address = ("127.0.0.1", args.port)
    with ThreadingHTTPServer(address, handler_for(repo, args.port, APP / ".local/run.json")) as server:
        print(f"เปิด http://127.0.0.1:{args.port} · Git {repo.revision[:12]}", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
