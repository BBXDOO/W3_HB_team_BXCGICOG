W3 Cross API

Overview

W3 Cross API is the gateway between external tools and the W3 Runtime.

Base URL:

http://127.0.0.1:8000

---

Health Check

Request

curl http://127.0.0.1:8000/health

Response

{
  "status": "ok"
}

---

Cross Runtime

Endpoint

POST /w3/cross

Request

{
  "source": "BBX19",
  "intent": "review",
  "target": "REDR",
  "focus": "memory",
  "mode": "cross"
}

---

Fields

source

Request owner.

Examples:

BBX19
SYSTEM
GW
USER

---

intent

Action type.

Supported:

review

Future:

analyze
design
route
audit

---

target

Module under review.

Supported:

REDR
DTML
LRC2
PSP2
W3

---

focus

Review focus.

Supported:

memory
risk
law
system

Future:

runtime
signal
identity
health

---

mode

Execution mode.

Supported:

cross

---

Example

Review REDR memory

curl -X POST http://127.0.0.1:8000/w3/cross \
-H "Content-Type: application/json" \
-d '{
  "source":"BBX19",
  "intent":"review",
  "target":"REDR",
  "focus":"memory",
  "mode":"cross"
}'

---

Tool Wrapper

Using:

python tools/w3api.py review REDR memory

Equivalent to:

{
  "source":"BBX19",
  "intent":"review",
  "target":"REDR",
  "focus":"memory",
  "mode":"cross"
}

---

Current Modules

REDR

Risk Escalation Decision Router

---

DTML

Decision Trace Mapping Layer

---

LRC2

Lifecycle Review Checkpoint v2

---

PSP2

Pointer Stamp / PR Flow Router

---

System Review

python tools/w3api.py review W3 system

Returns system-wide module status.

Bash
mkdir -p docs

cat > docs/API.md <<'MD'
# W3 Cross API

## Server

Start API server:

```bash
python W3_API_SERVER_SIMPLE.py
Server URL:
Plain text
http://127.0.0.1:8000
Health
Bash
python tools/w3api.py health
Review REDR memory
Bash
python tools/w3api.py review REDR memory
Review DTML law
Bash
python tools/w3api.py review DTML law
Review W3 system
Bash
python tools/w3api.py review W3 system
Fields
Plain text
intent = งานที่สั่ง เช่น review
target = เป้าหมาย เช่น REDR, DTML, LRC2, PSP2, W3
focus  = จุดที่ตรวจ เช่น memory, risk, law, system
mode   = cross
Server control
Bash
python tools/w3api.py start
python tools/w3api.py stop
python tools/w3api.py restart
python tools/w3api.py status
MD

## 2) วางทับ `tools/w3api.py` ทั้งไฟล์

```bash
mkdir -p tools

cat > tools/w3api.py <<'PY'
#!/usr/bin/env python3
import json
import os
import signal
import subprocess
import sys
import time
import urllib.request
import urllib.error


BASE = "http://127.0.0.1:8000"
API_URL = BASE + "/w3/cross"
HEALTH_URL = BASE + "/health"
SERVER_FILE = "W3_API_SERVER_SIMPLE.py"
PID_FILE = ".w3_api_server.pid"


def get_json(url):
    with urllib.request.urlopen
