Name : EP Signal Encoding — experimental pulse rhythm notation  
AM Ⅱ - BUILD : รูปแบบเข้ารหัสสัญญาณทดลองที่ใช้ start bit, alternating run-length และ check value; Rytm เป็นมุมมอง preview แยกจาก payload และไม่ถือเป็น transport ที่ผ่านการรับรอง  
Log time : 2026-11-22 (date only; time not recorded) ; ID : EP_SIGNAL-README-001  
≡ Br4ra - RAMS

## Body — บทบาทและขอบเขต

รูปแบบเข้ารหัสสัญญาณทดลองที่ใช้ start bit, alternating run-length และ check value; Rytm เป็นมุมมอง preview แยกจาก payload และไม่ถือเป็น transport ที่ผ่านการรับรอง

```yaml
AM_TYPE: II
ROLE: ADAPTATION
DERIVED_FROM:
  - protocol/EP_SIGNAL/SPEC_v1.md
  - protocol/EP_SIGNAL/RYTM_SIGNAL.md
DOCUMENT_PATH: protocol/EP_SIGNAL/README.md
```

**ขอบเขต:** README นี้อธิบายเฉพาะ `protocol/EP_SIGNAL/` ไม่ขยายสิทธิ์ของระบบอื่นและไม่ยืนยันผลทดสอบที่ไม่ได้มีหลักฐาน

## Movement — การนำทาง

### M1 — รายการในโฟลเดอร์นี้

| รายการ | ประเภท |
|---|---|
| [CONTINUITY_MEMORY_MODEL.md](CONTINUITY_MEMORY_MODEL.md) | เอกสาร |
| [EP_MANAUL.md](EP_MANAUL.md) | เอกสาร |
| [INTERPRETATION_BOUNDARY_PAPER.md](INTERPRETATION_BOUNDARY_PAPER.md) | เอกสาร |
| [README.md](README.md) | README / AMS |
| [README_integration.md](README_integration.md) | เอกสาร |
| [RYTM_SIGNAL.md](RYTM_SIGNAL.md) | เอกสาร |
| [SIGNAL_IDENTITY_LAW.md](SIGNAL_IDENTITY_LAW.md) | เอกสาร |
| [SPEC_v1.md](SPEC_v1.md) | เอกสาร |
| [TEST_CASE01.md](TEST_CASE01.md) | เอกสาร |
| [TEST_CASES.md](TEST_CASES.md) | เอกสาร |
| [TecnicalRytm.md](TecnicalRytm.md) | เอกสาร |
| [TecnicalRytm02.md](TecnicalRytm02.md) | เอกสาร |
| [ep_signal_adapter.py](ep_signal_adapter.py) | Python source / test |
| [reference_implementation.py](reference_implementation.py) | Python source / test |
| [rytm.py](rytm.py) | Python source / test |
| [summary_cord01.md](summary_cord01.md) | เอกสาร |
| [test_ep_signal_integration.py](test_ep_signal_integration.py) | Python source / test |

### M2 — เอกสารอ้างอิงนอกพื้นที่

| docs.* | Text link | ความสัมพันธ์ |
|---|---|---|
| docs.parent | [พื้นที่ protocol](../README.md) | พื้นที่ protocol |
| docs.core | [หลักการ Core vs Structure](../../knowledge/philosophy/corevsstructure.md) | หลักการ Core vs Structure |
| docs.ams | [กฎ AMS](../../docs/governance/AMS.md) | กฎ AMS |
| docs.mpcp | [ระบบที่อาจเชื่อมต่อ](../mpcp/README.md) | ระบบที่อาจเชื่อมต่อ |

---

### บันทึกเนื้อหา README เดิม (รักษาข้อมูลต้นทาง)

EP Signal Encoding (EP-Signal)

Status: Experimental
Owner: BBX19
Location: "protocol/EP_SIGNAL/"

---

Overview

EP Signal Encoding (EP-Signal) is a custom data encoding model designed to represent binary information through electrical pulse rhythm patterns instead of raw binary notation.

The system converts standard binary sequences into a compact structured signal format using:

1. Primary Start Signal
2. Alternating Run-Length Pulse Sequence
3. Integrity Check Value

This model is intended for experimental system design, protocol research, logic abstraction, and future integration into BBX19 architecture.

---

Core Format

[start_bit]/[pulse_sequence]-[check_value]

Example

0/221112133-8

---

Structure Definition

Segment| Meaning
"0/"| Primary signal. Indicates sequence starts with bit "0"
"221112133"| Consecutive run-length pattern with alternating bit states
"-8"| Validation value = total number of "1" bits in decoded sequence

---

Decode Example

Input:

0/221112133-8

Expansion:

00 11 0 1 0 11 0 111 000

Decoded Binary:

0011010110111000

Total number of "1" bits:

8

Validation passed.

---

Encoding Logic

Step 1 — Read Binary Input

0011010110111000

Step 2 — Detect Starting Bit

0

Step 3 — Count Consecutive Runs

2 2 1 1 1 2 1 3 3

Step 4 — Count Total Ones

8

Final Output

0/221112133-8

---

Objectives

- Create alternative binary representation model
- Reduce repetitive binary patterns
- Introduce rhythm-based signal notation
- Build experimental protocol layer for future systems
- Integrate with BBX19 decision and signal architecture

---

Current Status

Item| State
Concept Model| Complete
Manual Encode/Decode| Working
Validation Rule| Working
Automation Script| Pending
Compression Benchmark| Pending
Protocol Integration| Pending

---

Future Roadmap

EP v1

- Basic encode/decode
- Ones-count validation

EP v2

- Length verification
- Multi-block packet support
- Symbol dictionary

EP v3

- Runtime implementation
- Native transport protocol
- Hardware pulse simulation

---

Notes

EP-Signal is an independent experimental format and does not replace binary systems.
It acts as an abstraction layer for signal representation and future protocol innovation.

---

Maintainer Note

Created under BBX19 research direction.
All future revisions should preserve decode reversibility and validation consistency.

---

## Cross-X / Rytm Runtime Base

EP_SIGNAL now has a small importable Rytm layer for Cross-X planning:

- `protocol/EP_SIGNAL/rytm.py` exposes immutable Rytm packets.
- Rytm packets preserve reversible binary truth and add pulse-cadence metadata.
- Cross-X and W3-API use Rytm as `preview_only`; it does not persist or rewrite EP_SIGNAL payloads.
- Canonical preview shape: `[START]/[RHYTHM]'META'-[VERIFY]//[FORMAT].`

Example:

```text
EP_SIGNAL: 0/2222-4'BIN
RYTM:      0/2222'CROSS_X'-4//BIN.
```

Design rule: EP_SIGNAL remains the compact transport payload; Rytm is the readable rhythm view carried beside it.

---

OWNER : BBX19 — เจ้าของแนวคิด/ระบบตามข้อมูลต้นทาง  
MAKER : ChatGPT / Codex — ปรับ README ให้สอดคล้อง AMS โดยรักษาเนื้อหาเดิม
