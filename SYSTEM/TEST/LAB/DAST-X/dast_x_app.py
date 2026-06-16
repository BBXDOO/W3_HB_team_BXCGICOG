#!/usr/bin/env python3
"""DAST-X app skeleton.

This first scaffold starts a local FastAPI page for the DAST-X lab.
The detailed repo viewer logic should stay read-only and be added in small reviewed steps.
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os

app = FastAPI(title="DAST-X", version="0.1.0")

HTML = """
<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DAST-X</title>
<style>
body{margin:0;background:#141414;color:#eee;font-family:system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}.wrap{max-width:1100px;margin:0 auto;padding:16px}.card{background:#050505;border:1px solid #222;border-radius:20px;padding:16px;margin:12px 0;box-shadow:-18px 18px 40px rgba(0,0,0,.25)}code,pre{font-family:ui-monospace,monospace}.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}.muted{color:#aaa}@media(max-width:800px){.grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="wrap">
  <div class="card">
    <h1>DAST-X</h1>
    <p class="muted">Termux Repo Desk / Local Web App</p>
    <p>สถานะ: v0.1 scaffold — read-only first</p>
    <p class="muted">default port: 8181</p>
  </div>
  <div class="grid">
    <div class="card"><h2>WINDOW A — Repo Tree</h2><p>พื้นที่นี้จะใช้แสดง root-repo, folder tree และการเลือกไฟล์</p></div>
    <div class="card"><h2>WINDOW B — Termux Tools</h2><p>พื้นที่นี้จะใช้แสดง package, tools, path และ saved commands</p></div>
  </div>
  <div class="card"><h2>Viewer</h2><p>พื้นที่นี้จะใช้แสดง Markdown / Code / Text จากไฟล์ที่เลือก</p></div>
</div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def index():
    return HTML

if __name__ == "__main__":
    import uvicorn
    host = os.environ.get("DASTX_HOST", "127.0.0.1")
    port = int(os.environ.get("DASTX_PORT", "8181"))
    uvicorn.run(app, host=host, port=port)
