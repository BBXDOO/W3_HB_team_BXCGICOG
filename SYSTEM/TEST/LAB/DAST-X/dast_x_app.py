#!/usr/bin/env python3
"""DAST-X v0.1 — dependency-free Termux Repo Desk.

Uses Python standard library only.
Default URL: http://127.0.0.1:8181/
"""

from __future__ import annotations

import html
import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

APP_DIR = Path(__file__).resolve().parent
REPO_ROOT = Path(os.environ.get("DASTX_REPO_ROOT", str(APP_DIR.parents[3]))).expanduser().resolve()
DATA_DIR = Path(os.environ.get("DASTX_DATA_DIR", str(APP_DIR / "data"))).expanduser().resolve()
DATA_DIR.mkdir(parents=True, exist_ok=True)
COMMANDS_FILE = DATA_DIR / "commands.json"
EXAMPLE_COMMANDS_FILE = APP_DIR / "commands.example.json"
MAX_READ = 400_000

TEXT_EXTS = {".md", ".txt", ".py", ".js", ".json", ".yaml", ".yml", ".html", ".css", ".sh", ".bash", ".toml", ".csv", ".xml", ".lua", ".sql"}


def safe_path(p: str) -> Path:
    p = (p or ".").strip() or "."
    target = (REPO_ROOT / p).resolve()
    if target != REPO_ROOT and REPO_ROOT not in target.parents:
        raise ValueError("path escapes repo root")
    return target


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(REPO_ROOT)) or "."
    except Exception:
        return str(p)


def branch_name() -> str:
    head = REPO_ROOT / ".git" / "HEAD"
    if not head.exists():
        return "-"
    text = head.read_text(encoding="utf-8", errors="replace").strip()
    return text.replace("ref: refs/heads/", "") if text.startswith("ref: refs/heads/") else text[:12]


def load_commands() -> list:
    if not COMMANDS_FILE.exists() and EXAMPLE_COMMANDS_FILE.exists():
        COMMANDS_FILE.write_text(EXAMPLE_COMMANDS_FILE.read_text(encoding="utf-8"), encoding="utf-8")
    if not COMMANDS_FILE.exists():
        return []
    try:
        data = json.loads(COMMANDS_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def is_text(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTS or path.name in {"README", "LICENSE", "Makefile", "Dockerfile"}


HTML = """<!doctype html><html lang='th'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>DAST-X</title><style>
body{margin:0;background:radial-gradient(circle at top left,#343434,#171717 60%,#080808);color:#eee;font-family:system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}.wrap{max-width:1400px;margin:0 auto;padding:14px}.top,.card{background:rgba(0,0,0,.78);border:1px solid #242424;border-radius:22px;padding:14px;box-shadow:-20px 20px 50px rgba(0,0,0,.25)}.top{display:flex;justify-content:space-between;gap:12px;align-items:center}.grid{display:grid;grid-template-columns:320px 350px 1fr;gap:12px;margin-top:12px}h1,h2{margin:0 0 10px}.meta{color:#aaa;font-family:ui-monospace,monospace;font-size:13px;overflow-wrap:anywhere}.btn{background:#161616;color:#eee;border:1px solid #333;border-radius:12px;padding:8px 10px;margin:2px}.input{width:100%;background:#090909;color:#eee;border:1px solid #333;border-radius:12px;padding:10px;margin:4px 0}.list{max-height:58vh;overflow:auto}.row{padding:8px 6px;border-bottom:1px solid #171717;cursor:pointer;font-family:ui-monospace,monospace;font-size:13px;overflow-wrap:anywhere}.row:hover{background:#111}.badge{font-size:11px;color:#111;background:#ddd;border-radius:8px;padding:2px 6px;margin-right:6px}.viewer{min-height:72vh;max-height:82vh;overflow:auto}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-family:ui-monospace,monospace}.ok{color:#8ef58e}.bad{color:#ff8b8b}.cmd{background:#101010;border:1px solid #242424;border-radius:12px;padding:8px;margin:8px 0}a{color:#cfcfcf}@media(max-width:980px){.grid{grid-template-columns:1fr}.viewer{max-height:none}.top{display:block}}
</style></head><body><div class='wrap'><section class='top'><div><h1>DAST-X</h1><div id='summary' class='meta'>loading...</div></div><div><button class='btn' onclick='loadAll()'>Refresh</button><button class='btn' onclick="loadTree('.')">Root</button></div></section><section class='grid'><aside class='card'><h2>WINDOW A — Repo Tree</h2><input id='pathBox' class='input' value='.'><button class='btn' onclick="loadTree(document.getElementById('pathBox').value)">Open Path</button><button class='btn' onclick='loadTree(parentPath)'>Up</button><div id='tree' class='list'></div></aside><aside class='card'><h2>WINDOW B — Termux / Tools</h2><div id='termux' class='meta'>loading...</div><h2>Saved Commands</h2><div id='commands'></div></aside><main class='card viewer'><h2 id='viewerTitle'>Viewer</h2><div id='viewer'>แตะไฟล์จาก WINDOW A เพื่ออ่านเนื้อหา</div></main></section></div><script>
let parentPath='.';async function api(u){let r=await fetch(u);if(!r.ok)throw new Error(await r.text());return await r.json()}function esc(s){return(s||'').toString().replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))}async function loadSummary(){let s=await api('/api/summary');document.getElementById('summary').innerHTML=`repo=${esc(s.repo)} | branch=${esc(s.branch)} | python stdlib only | port=8181<br>root=${esc(s.root)}`}async function loadTree(p='.'){let d=await api('/api/tree?path='+encodeURIComponent(p));parentPath=d.parent;document.getElementById('pathBox').value=d.cwd;let el=document.getElementById('tree');el.innerHTML='';d.items.forEach(it=>{let row=document.createElement('div');row.className='row';row.innerHTML=`<span class='badge'>${it.type}</span>${esc(it.name)}<div class='meta'>${esc(it.path)}</div>`;row.onclick=()=>it.type==='dir'?loadTree(it.path):openFile(it.path);el.appendChild(row)})}async function openFile(p){let f=await api('/api/file?path='+encodeURIComponent(p));document.getElementById('viewerTitle').innerText=f.path;document.getElementById('viewer').innerHTML=f.html}async function loadTermux(){let t=await api('/api/termux');let h=`PREFIX: ${esc(t.prefix)}<br>HOME: ${esc(t.home)}<hr>`;t.tools.forEach(x=>h+=`<div><span class='${x.ok?'ok':'bad'}'>${x.ok?'ok':'missing'}</span> ${esc(x.name)}<br><span class='meta'>${esc(x.path)}</span></div>`);document.getElementById('termux').innerHTML=h}async function loadCommands(){let items=await api('/api/commands');document.getElementById('commands').innerHTML=items.map(c=>`<div class='cmd'><b>${esc(c.group)} / ${esc(c.name)}</b><br><code>${esc(c.command)}</code><div class='meta'>${esc(c.note||'')}</div></div>`).join('')}async function loadAll(){await loadSummary();await loadTree('.');await loadTermux();await loadCommands()}loadAll().catch(e=>document.body.insertAdjacentHTML('afterbegin','<pre>'+esc(e.message)+'</pre>'))
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def send_json(self, data):
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def send_html(self, text):
        raw = text.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        try:
            if u.path == "/":
                return self.send_html(HTML)
            if u.path == "/api/summary":
                return self.send_json({"repo": REPO_ROOT.name, "root": str(REPO_ROOT), "branch": branch_name()})
            if u.path == "/api/tree":
                base = safe_path(q.get("path", ["."])[0])
                if base.is_file():
                    base = base.parent
                items = []
                for p in sorted(base.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))[:600]:
                    if p.name in {".git", "__pycache__", "node_modules", ".pytest_cache"}:
                        continue
                    items.append({"name": p.name, "path": rel(p), "type": "dir" if p.is_dir() else "file"})
                parent = rel(base.parent) if base != REPO_ROOT else "."
                return self.send_json({"cwd": rel(base), "parent": parent, "items": items})
            if u.path == "/api/file":
                p = safe_path(q.get("path", [""])[0])
                if p.is_dir():
                    return self.send_json({"path": rel(p), "html": "<p>folder</p>"})
                if not is_text(p):
                    return self.send_json({"path": rel(p), "html": "<p>Binary หรือไฟล์ที่ยังไม่รองรับ preview</p>"})
                text = p.read_bytes()[:MAX_READ].decode("utf-8", errors="replace")
                if p.suffix.lower() == ".md":
                    safe = html.escape(text)
                    body = "<pre>" + safe + "</pre>"
                else:
                    body = "<pre>" + html.escape(text) + "</pre>"
                return self.send_json({"path": rel(p), "html": body})
            if u.path == "/api/termux":
                tools = []
                for name in ["bash", "git", "python", "node", "gh", "termux-info", "termux-open", "rg", "tree", "jq", "nano"]:
                    found = None
                    for d in os.environ.get("PATH", "").split(os.pathsep):
                        cand = Path(d) / name
                        if cand.exists():
                            found = str(cand)
                            break
                    tools.append({"name": name, "ok": bool(found), "path": found or "-"})
                return self.send_json({"prefix": os.environ.get("PREFIX", "-"), "home": os.environ.get("HOME", "-"), "tools": tools})
            if u.path == "/api/commands":
                return self.send_json(load_commands())
            self.send_response(404); self.end_headers()
        except Exception as e:
            self.send_response(500); self.end_headers(); self.wfile.write(str(e).encode("utf-8"))


def main():
    host = os.environ.get("DASTX_HOST", "127.0.0.1")
    port = int(os.environ.get("DASTX_PORT", "8181"))
    print(f"DAST-X stdlib server: http://{host}:{port}/")
    HTTPServer((host, port), Handler).serve_forever()


if __name__ == "__main__":
    main()
