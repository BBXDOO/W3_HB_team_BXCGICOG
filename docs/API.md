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
