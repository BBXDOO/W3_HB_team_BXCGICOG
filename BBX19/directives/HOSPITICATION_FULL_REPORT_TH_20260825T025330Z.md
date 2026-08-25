# รายงานตรวจสุขภาพโครงสร้าง W3 — Hospitication

## ข้อมูลรายงาน

- เวลาตรวจ: `2026-08-25T02:53:30Z`
- Repository root: `/data/data/com.termux/files/home/W3_HB_team_BXCGICOG`
- Hospitication version: `0.1.0`
- จำนวนไฟล์ที่ Observer ตรวจ: `1136`
- จำนวนบรรทัดรวม: `171022`
- ขนาดข้อมูลรวมที่อ่าน: `6407831` bytes
- Overall pressure score: `0.4961`
- Signals: `5`
- Recovery proposals: `3`
- Mutation ต่อ source truth: `false`
- Auto-recovery: `false`

## บทสรุป

Highest pressure: replay_complexity=1.0000; signals=5; proposals=3.

> คะแนนในรายงานเป็น structural pressure evidence ไม่ใช่การวินิจฉัย root cause และไม่ใช่คำสั่งแก้ไขระบบ

## ขอบเขตการตรวจตามจริง

Observer ไล่อ่านไฟล์ภายใต้ repository root โดยข้าม ignored directories และไฟล์ที่มีขนาดเกินค่ากำหนด การตรวจครั้งนี้ไม่แก้ไฟล์ต้นฉบับ

### จำนวนไฟล์แยกตามนามสกุล

| นามสกุล | จำนวน |
|---|---:|
| `.csv` | 1 |
| `.gstate` | 6 |
| `.html` | 9 |
| `.java` | 1 |
| `.jpeg` | 3 |
| `.jpg` | 1 |
| `.js` | 1 |
| `.json` | 116 |
| `.jsonl` | 3 |
| `.md` | 575 |
| `.md”` | 1 |
| `.png` | 11 |
| `.py` | 280 |
| `.sh` | 2 |
| `.svg` | 1 |
| `.ts` | 3 |
| `.txt` | 8 |
| `.w3md` | 1 |
| `.yml` | 10 |
| `[no suffix]` | 103 |

## Metrics

| Metric | ความหมาย | Score |
|---|---|---:|
| `cognitive_cost` | ต้นทุนในการทำความเข้าใจโครงสร้าง | `1.0000` |
| `dependency_fatigue` | ความเหนื่อยล้าจาก Dependency | `0.0869` |
| `recovery_resistance` | แรงต้านต่อการฟื้นฟู | `0.1708` |
| `replay_complexity` | ความซับซ้อนด้าน Replay/Event/Ledger | `1.0000` |
| `semantic_pressure` | แรงกดดันด้านความหมายและคำศัพท์ | `0.2227` |

### ต้นทุนในการทำความเข้าใจโครงสร้าง

- Metric: `cognitive_cost`
- Score: `1.0000`
- Summary: Cognitive cost from file count, average size, and configuration breadth.

Evidence:

```json
{
  "average_lines_per_file": 150.55,
  "config_files": 126,
  "file_count": 1136,
  "total_lines": 171022
}
```

### ความเหนื่อยล้าจาก Dependency

- Metric: `dependency_fatigue`
- Score: `0.0869`
- Summary: Dependency fatigue from import breadth and repeated coupling points.

Evidence:

```json
{
  "code_files": 287,
  "import_mentions": 1017,
  "top_imports": {
    "__future__": 132,
    "dataclasses": 51,
    "datetime": 46,
    "json": 65,
    "os": 35,
    "pathlib": 65,
    "sys": 42,
    "typing": 114
  },
  "unique_imports": 125
}
```

### แรงต้านต่อการฟื้นฟู

- Metric: `recovery_resistance`
- Score: `0.1708`
- Summary: Recovery resistance from large surfaces with limited tests/docs counterweight.

Evidence:

```json
{
  "code_files": 287,
  "doc_files": 583,
  "large_file_count": 97,
  "large_files": [
    "branding/logo/image.jpg",
    "branding/logo/20251030_120037_0000.png",
    "branding/logo/OIG2.jpeg",
    "branding/logo/OIG4.jpeg",
    "branding/logo/20251030_115303_0000.png",
    "branding/logo/AQNfmqAYqIspfAyoVk9W1AWHG-8J8jTE0EXhHgHJERq6p3bWeDWPJyvPn0iWc26BWyLKrfuAFQRt7V2tC74eEBc9(1)(1).png",
    "branding/logo/AQPPL6XfiA6FwDterMFeljnJjKbTnxoT6V_c7siksWH7q4Ur1dZ4r8KdJXTZUlxeXk4Dj3Xuvc4nsVMqGeOnlWk8.jpeg",
    "repo_report.html",
    "repo-structure.html",
    "croll/CROSS_L_RYTM_MODEW_ROUTING.md"
  ],
  "test_files": 91
}
```

### ความซับซ้อนด้าน Replay/Event/Ledger

- Metric: `replay_complexity`
- Score: `1.0000`
- Summary: Replay complexity from event/outcome/ledger/checkpoint surfaces.

Evidence:

```json
{
  "replay_marker_hits": 55,
  "replay_related_file_count": 32,
  "replay_related_files": [
    "Gemini/tasks/checkpoints.md",
    "HBISOCITY/docs/th/11_event_system.md",
    "SYSTEM/TESTS/BBX19/GOVERNANCE/decision-trace-model.md",
    "core/events/event-protocol.md",
    "core/events/event-schema.json",
    "core/events/examples/event-log-example.json",
    "core/runtime/w3lgu_mfc_logic/event_field.py",
    "core/vault/w3_internal_ledger.json",
    "cross_x/event_chain.py",
    "decision_trace/.gitkeep",
    "docs/governance/decision_trace.md",
    "ecs/ecs/event_registry.py",
    "ecs/event_chain_system.py",
    "hospitication/analysis/replay_complexity.py",
    "outcomes/README.md",
    "outcomes/append_only_ledger/.gitkeep",
    "outcomes/artifacts/.gitkeep",
    "outcomes/ledger/2026-02-25_outcomes-system-bootstrap.md",
    "outcomes/ledger/_TEMPLATE__outcome-record.md",
    "protocol/ecs/event_chain_integration.py"
  ]
}
```

### แรงกดดันด้านความหมายและคำศัพท์

- Metric: `semantic_pressure`
- Score: `0.2227`
- Summary: Semantic pressure from repeated W3 governance/replay concepts.

Evidence:

```json
{
  "doc_files": 583,
  "semantic_marker_hits": 839,
  "top_terms": {
    "governance": 290,
    "memory": 251,
    "mpcp": 266,
    "replay": 32
  }
}
```

## Signals

### `sig_4880b51e4f5d1111`

- Detector: `spike`
- Pressure: `critical_collapse_risk` — มีความเสี่ยงต่อการล้มระดับวิกฤต
- Confidence: `1.0000`
- Origin node: `(0,0)`
- Retention: `critical`
- Persistence: `permanent`
- Derived: `false`

Evidence:

```json
{
  "metric": "cognitive_cost",
  "score": 1.0
}
```

### `sig_85c31cd8aacdbdd8`

- Detector: `spike`
- Pressure: `critical_collapse_risk` — มีความเสี่ยงต่อการล้มระดับวิกฤต
- Confidence: `1.0000`
- Origin node: `(3,0)`
- Retention: `critical`
- Persistence: `permanent`
- Derived: `false`

Evidence:

```json
{
  "metric": "replay_complexity",
  "score": 1.0
}
```

### `sig_be8622ae7e6e1399`

- Detector: `oscillation`
- Pressure: `structural_instability` — มีความไม่มั่นคงเชิงโครงสร้าง
- Confidence: `0.6667`
- Origin node: `(14,15)`
- Retention: `standard`
- Persistence: `session`
- Derived: `false`

Evidence:

```json
{
  "direction_changes": 0.6666666666666666
}
```

### `sig_c3905c08bf4729a2`

- Detector: `drift`
- Pressure: `informational_drift` — พบความเปลี่ยนแปลงระดับข้อมูล
- Confidence: `0.2227`
- Origin node: `(4,0)`
- Retention: `standard`
- Persistence: `session`
- Derived: `false`

Evidence:

```json
{
  "metric": "semantic_pressure",
  "score": 0.2227
}
```

### `sig_d9c3c139fa1ed602`

- Detector: `divergence`
- Pressure: `critical_collapse_risk` — มีความเสี่ยงต่อการล้มระดับวิกฤต
- Confidence: `0.9131`
- Origin node: `(15,15)`
- Retention: `critical`
- Persistence: `permanent`
- Derived: `false`

Evidence:

```json
{
  "score_spread": 0.9131
}
```

## Recovery Proposals

### Mitigate replay complexity

- Proposal ID: `prop_5502a8ab4e5760d3`
- Status: `proposed`
- Destructive: `false`
- Rationale: Metric score 1.0000: Replay complexity from event/outcome/ledger/checkpoint surfaces.
- Source metrics: `replay_complexity`

Actions:

- Keep replay, event, and outcome-ledger contracts explicitly versioned.
- Add replay fixtures before changing recovery or ledger behavior.

Target paths:

- `Gemini/tasks/checkpoints.md`
- `HBISOCITY/docs/th/11_event_system.md`
- `SYSTEM/TESTS/BBX19/GOVERNANCE/decision-trace-model.md`
- `core/events/event-protocol.md`
- `core/events/event-schema.json`

### Mitigate cognitive cost

- Proposal ID: `prop_a03b16788a3748e9`
- Status: `proposed`
- Destructive: `false`
- Rationale: Metric score 1.0000: Cognitive cost from file count, average size, and configuration breadth.
- Source metrics: `cognitive_cost`

Actions:

- Add index documents for high-breadth areas and remove stale navigation paths.
- Group operational docs by owner, lifecycle, and replay relevance.

### Review clustered signal pressure

- Proposal ID: `prop_fb6cf83198d59207`
- Status: `proposed`
- Destructive: `false`
- Rationale: 5 emitted signals indicate structural pressure clustering.
- Source metrics: `cognitive_cost, replay_complexity`

Actions:

- Review signal evidence in descending confidence order.
- Attach recovery notes as new annotations, not mutations of emitted truth.

## การตรวจความพร้อมของชุดโค้ด

### Compile check — return code `0`

```text
[no stdout]
[no stderr]
```

### Hospitication tests — return code `0`

```text
.......                                                                  [100%]
7 passed in 1.18s
```

## W3DB Awareness / Append Trace

Hospitication Signals และ summary ถูกส่งผ่าน W3DB runtime แบบ derived observation โดยไม่ rewrite truth เดิม อย่างไรก็ตาม W3DBStore ปัจจุบันเป็น in-memory จึงใช้ activity log ใน `reports/` เป็นหลักฐานถาวรเพิ่มเติม

- W3DB runtime stats: `{
  "fbd": 6,
  "prx": 6,
  "tuf": 6,
  "whb": 6,
  "xiz": 6
}`
- Signal append error: `None`
- Summary append error: `None`

### Summary append result

```json
{
  "append_id": "APP-HOSPITICATIO-7CC1E05B58416CA1",
  "appended": true,
  "fbd_id": "FBD-HOSPITICATIO-E05B58416CA1",
  "output": {
    "cix": "HOSPITICATION",
    "fbd": {
      "failure": "Green",
      "id": "FBD-HOSPITICATIO-E05B58416CA1",
      "impact": "Boundary within limits"
    },
    "prx": {
      "color": "RED",
      "id": "PRX-HOSPITICATIO-E05B58416CA1",
      "intensity": 1.0,
      "symbol": "▲"
    },
    "tuf": {
      "confidence": 1.0,
      "final": "1",
      "id": "TUF-HOSPITICATIO-E05B58416CA1",
      "initial": "1"
    },
    "whb": {
      "action": "THEN PASS — within boundary, no action required",
      "condition": "IF final_state=1 AND confidence=1.0",
      "id": "WHB-HOSPITICATIO-E05B58416CA1"
    },
    "xiz": "XIZ-HOSPITICATIO-E05B58416CA1"
  },
  "prx_id": "PRX-HOSPITICATIO-E05B58416CA1",
  "references": [
    "hospitication/README.md",
    "hospitication/docs/ARCHITECTURE.md",
    "reports/HOSPITICATION_FULL_REPORT_TH_20260825T025330Z.md"
  ],
  "status": "appended",
  "tuf_id": "TUF-HOSPITICATIO-E05B58416CA1",
  "whb_id": "WHB-HOSPITICATIO-E05B58416CA1",
  "xiz_id": "XIZ-HOSPITICATIO-E05B58416CA1"
}
```

### Signal append results

```json
[
  {
    "fbd_id": "FBD-HOSP-4F5D1111",
    "output": {
      "cix": "HOSPITICATION",
      "fbd": {
        "failure": "Green",
        "id": "FBD-HOSP-4F5D1111",
        "impact": "Boundary within limits"
      },
      "prx": {
        "color": "RED",
        "id": "PRX-HOSP-4F5D1111",
        "intensity": 1.0,
        "symbol": "▲"
      },
      "tuf": {
        "confidence": 1.0,
        "final": "1",
        "id": "TUF-HOSP-4F5D1111",
        "initial": "1"
      },
      "whb": {
        "action": "THEN PASS — within boundary, no action required",
        "condition": "IF final_state=1 AND confidence=1.0",
        "id": "WHB-HOSP-4F5D1111"
      },
      "xiz": "XIZ-HOSP-4F5D1111"
    },
    "prx_id": "PRX-HOSP-4F5D1111",
    "signal_id": "sig_4880b51e4f5d1111",
    "tuf_id": "TUF-HOSP-4F5D1111",
    "xiz_id": "XIZ-HOSP-4F5D1111"
  },
  {
    "fbd_id": "FBD-HOSP-AACDBDD8",
    "output": {
      "cix": "HOSPITICATION",
      "fbd": {
        "failure": "Green",
        "id": "FBD-HOSP-AACDBDD8",
        "impact": "Boundary within limits"
      },
      "prx": {
        "color": "RED",
        "id": "PRX-HOSP-AACDBDD8",
        "intensity": 1.0,
        "symbol": "▲"
      },
      "tuf": {
        "confidence": 1.0,
        "final": "1",
        "id": "TUF-HOSP-AACDBDD8",
        "initial": "1"
      },
      "whb": {
        "action": "THEN PASS — within boundary, no action required",
        "condition": "IF final_state=1 AND confidence=1.0",
        "id": "WHB-HOSP-AACDBDD8"
      },
      "xiz": "XIZ-HOSP-AACDBDD8"
    },
    "prx_id": "PRX-HOSP-AACDBDD8",
    "signal_id": "sig_85c31cd8aacdbdd8",
    "tuf_id": "TUF-HOSP-AACDBDD8",
    "xiz_id": "XIZ-HOSP-AACDBDD8"
  },
  {
    "fbd_id": "FBD-HOSP-7E6E1399",
    "output": {
      "cix": "HOSPITICATION",
      "fbd": {
        "failure": "Yellow",
        "id": "FBD-HOSP-7E6E1399",
        "impact": "Boundary within limits"
      },
      "prx": {
        "color": "BLUE",
        "id": "PRX-HOSP-7E6E1399",
        "intensity": 0.3334,
        "symbol": "◆"
      },
      "tuf": {
        "confidence": 0.6667,
        "final": "0.5",
        "id": "TUF-HOSP-7E6E1399",
        "initial": "0.5"
      },
      "whb": {
        "action": "THEN OBSERVE — boundary approached, monitor closely",
        "condition": "IF final_state=0.5 AND confidence=0.6667",
        "id": "WHB-HOSP-7E6E1399"
      },
      "xiz": "XIZ-HOSP-7E6E1399"
    },
    "prx_id": "PRX-HOSP-7E6E1399",
    "signal_id": "sig_be8622ae7e6e1399",
    "tuf_id": "TUF-HOSP-7E6E1399",
    "xiz_id": "XIZ-HOSP-7E6E1399"
  },
  {
    "fbd_id": "FBD-HOSP-BF4729A2",
    "output": {
      "cix": "HOSPITICATION",
      "fbd": {
        "failure": "Red",
        "id": "FBD-HOSP-BF4729A2",
        "impact": "Boundary exceeded"
      },
      "prx": {
        "color": "BLUE",
        "id": "PRX-HOSP-BF4729A2",
        "intensity": 0.5546,
        "symbol": "◆"
      },
      "tuf": {
        "confidence": 0.2227,
        "final": "0",
        "id": "TUF-HOSP-BF4729A2",
        "initial": "0"
      },
      "whb": {
        "action": "THEN ESCALATE — boundary exceeded, immediate review required",
        "condition": "IF final_state=0 AND confidence=0.2227",
        "id": "WHB-HOSP-BF4729A2"
      },
      "xiz": "XIZ-HOSP-BF4729A2"
    },
    "prx_id": "PRX-HOSP-BF4729A2",
    "signal_id": "sig_c3905c08bf4729a2",
    "tuf_id": "TUF-HOSP-BF4729A2",
    "xiz_id": "XIZ-HOSP-BF4729A2"
  },
  {
    "fbd_id": "FBD-HOSP-FA1ED602",
    "output": {
      "cix": "HOSPITICATION",
      "fbd": {
        "failure": "Green",
        "id": "FBD-HOSP-FA1ED602",
        "impact": "Boundary within limits"
      },
      "prx": {
        "color": "BLUE",
        "id": "PRX-HOSP-FA1ED602",
        "intensity": 0.8262,
        "symbol": "◆"
      },
      "tuf": {
        "confidence": 0.9131,
        "final": "1",
        "id": "TUF-HOSP-FA1ED602",
        "initial": "1"
      },
      "whb": {
        "action": "THEN PASS — within boundary, no action required",
        "condition": "IF final_state=1 AND confidence=0.9131",
        "id": "WHB-HOSP-FA1ED602"
      },
      "xiz": "XIZ-HOSP-FA1ED602"
    },
    "prx_id": "PRX-HOSP-FA1ED602",
    "signal_id": "sig_d9c3c139fa1ed602",
    "tuf_id": "TUF-HOSP-FA1ED602",
    "xiz_id": "XIZ-HOSP-FA1ED602"
  }
]
```

## ไฟล์ที่ถูกข้าม

- ไฟล์ใน ignored directories: `588`
- ไฟล์ขนาดเกิน `1000000` bytes: `4`

### Oversized files

- `architecture/diagrams/file_000000001e7c72088554e0c1715f55b2.png` — `1945515` bytes
- `architecture/diagrams/w3-civilization-main-map.png` — `11451115` bytes
- `branding/icons/copilot_image_1767026963042.jpeg` — `1299141` bytes
- `branding/logo/REPO-W1.png` — `12592717` bytes

## Complete Observation Manifest

รายการนี้แสดงไฟล์ทุกไฟล์ที่ Observer ใช้ในการคำนวณรายงานครั้งนี้

| Path | Suffix | Lines | Bytes | Imports | Markers |
|---|---|---:|---:|---|---|
| `.cli.py` | `.py` | 28 | 1194 | agents, argparse | - |
| `.devcontainer/devcontainer.json` | `.json` | 52 | 1326 | - | - |
| `.devcontainer/post-create.sh` | `.sh` | 52 | 1458 | - | - |
| `.github/CODEOWNERS` | `-` | 9 | 410 | - | governance |
| `.github/ISSUE_TEMPLATE/decision-request.md` | `.md` | 101 | 2128 | - | governance |
| `.github/PULL_REQUEST_TEMPLATE.md` | `.md` | 61 | 1710 | - | governance |
| `.github/agents/my-agent.agent.md` | `.md` | 23 | 617 | - | memory |
| `.github/check_test.ts` | `.ts` | 4 | 77 | - | - |
| `.github/workflows/check_test.ts` | `.ts` | 4 | 77 | - | - |
| `.github/workflows/croll.yml` | `.yml` | 74 | 1683 | - | - |
| `.github/workflows/decision-module-router.yml` | `.yml` | 522 | 20017 | - | mpcp |
| `.github/workflows/deploy.yml` | `.yml` | 38 | 649 | - | - |
| `.github/workflows/iget.yml` | `.yml` | 65 | 1868 | - | - |
| `.github/workflows/runtime-artifact.yml` | `.yml` | 70 | 1938 | - | memory |
| `.github/workflows/validate-json.yml` | `.yml` | 124 | 3699 | - | - |
| `.github/workflows/w3-structure-check.yml` | `.yml` | 156 | 4052 | - | - |
| `.github/workflows/w3_agent_autorespond.yml` | `.yml` | 50 | 1255 | - | - |
| `.github/workflows/w3_agent_ci.yml` | `.yml` | 40 | 883 | - | - |
| `.gitignore` | `-` | 140 | 3430 | - | memory |
| `BBEX-Core/PROTOCOL_HYBRID.md` | `.md` | 19 | 1551 | - | - |
| `BBEX-Core/private/BBEX_CORE_IDP.md` | `.md` | 108 | 8197 | - | governance |
| `BBEX-Core/private/ESSENCE.md` | `.md` | 16 | 741 | - | - |
| `BBEX-Core/private/W3_COMBINED.md` | `.md` | 711 | 34390 | - | governance, memory, mpcp |
| `BBEX-Core/private/W3_SYSTEM_HANDBOOK_TH.md` | `.md` | 715 | 37311 | - | governance, memory, mpcp |
| `BBEX-Core/private/เนื้อหาพิเศษ.md` | `.md` | 130 | 9347 | - | governance, memory, mpcp |
| `BBEX-Core/public/BBEX_CORE_IDP.md` | `.md` | 106 | 7954 | - | governance |
| `BBEX-Core/public/module.json` | `.json` | 132 | 3027 | - | governance, memory |
| `BBEX-Core/public/request_template.json` | `.json` | 10 | 516 | - | - |
| `BBX19/ENTRANCE.md` | `.md` | 184 | 5872 | - | - |
| `BBX19/README.md` | `.md` | 151 | 4593 | - | governance |
| `BBX19/directives/base.md` | `.md` | 9 | 295 | - | - |
| `BBX19/modules/BBX19/context/chatgpt_context.json` | `.json` | 25 | 657 | - | governance |
| `BBX19/modules/BBX19/context/chatgpt_context2.json` | `.json` | 52 | 1532 | - | - |
| `BBX19/modules/BBX19/idp/BBX19-IDP.md` | `.md` | 82 | 2210 | - | governance |
| `BBX19/modules/BBX19/idp/ChatGPT-IDP.md` | `.md` | 70 | 1570 | - | - |
| `BBX19/modules/BBX19/idp/Copilot-Gm-IDP.md` | `.md` | 58 | 2044 | - | governance |
| `BBX19/modules/BBX19/idp/DeepSeek-IDP.md` | `.md` | 30 | 1551 | - | - |
| `BBX19/modules/BBX19/idp/Gemini-IDP.md` | `.md` | 46 | 3186 | - | memory |
| `BBX19/modules/BBX19/idp/Grok-IDP.md` | `.md` | 43 | 1732 | - | - |
| `BBX19/modules/BBX19/idp/IDP-V2.0/BBEX-Core-IDP.md` | `.md` | 96 | 3428 | - | memory |
| `BBX19/modules/BBX19/idp/IDP-V2.0/BBX19-IDP.md` | `.md` | 78 | 1715 | - | governance |
| `BBX19/modules/BBX19/idp/IDP-V2.0/Cast-IDP.md` | `.md` | 96 | 3099 | - | memory, mpcp |
| `BBX19/modules/BBX19/idp/IDP-V2.0/ChatGPT-IDP.md` | `.md` | 78 | 1407 | - | - |
| `BBX19/modules/BBX19/idp/IDP-V2.0/Codex-IDP.md` | `.md` | 98 | 2332 | - | governance, mpcp |
| `BBX19/modules/BBX19/idp/IDP-V2.0/Copilot-Gm-IDP.md` | `.md` | 81 | 1903 | - | governance |
| `BBX19/modules/BBX19/idp/IDP-V2.0/DeepSeek-IDP.md` | `.md` | 78 | 1815 | - | - |
| `BBX19/modules/BBX19/idp/IDP-V2.0/Gemini-IDP.md` | `.md` | 78 | 1954 | - | - |
| `BBX19/modules/BBX19/idp/IDP-V2.0/Grok-IDP.md` | `.md` | 78 | 1735 | - | - |
| `BBX19/modules/BBX19/idp/IDP-V2.0/IDP-TEMPLET2.md` | `.md` | 81 | 1368 | - | - |
| `BBX19/modules/BBX19/idp/INDEX.md` | `.md` | 39 | 2139 | - | governance |
| `BBX19/modules/BBX19/module.json` | `.json` | 131 | 2713 | - | governance, memory |
| `BBX19/notes/BOX.md` | `.md` | 630 | 23011 | - | governance, memory, mpcp |
| `BBX19/notes/LIBRARY_WX.md` | `.md` | 227 | 12983 | - | governance, memory |
| `BBX19/notes/READMR.md` | `.md` | 10 | 1807 | - | - |
| `BBX19/notes/refactor_v02_modules_report.md` | `.md` | 347 | 12623 | - | governance, mpcp, replay |
| `BBX19/self-review.md` | `.md` | 30 | 1203 | - | - |
| `BBX19/status/CN-Fold/README.md` | `.md` | 362 | 13914 | - | - |
| `BBX19/status/README.md` | `.md` | 141 | 2510 | - | - |
| `BBX19/status/human-status.json` | `.json` | 7 | 128 | - | - |
| `Cast/ENTRANCE.md` | `.md` | 52 | 1847 | - | memory, mpcp |
| `Cast/README.md` | `.md` | 41 | 1306 | - | - |
| `Cast/artifacts/.gitkeep` | `-` | 0 | 0 | - | - |
| `Cast/context/README.md` | `.md` | 3 | 86 | - | memory |
| `Cast/context/SESSION CONTEXT — Cast.md` | `.md` | 96 | 2910 | - | governance, mpcp |
| `Cast/context/archive/.gitkeep` | `-` | 0 | 0 | - | - |
| `Cast/context/protocol.md` | `.md` | 32 | 1041 | - | memory |
| `Cast/context/session_summary.md` | `.md` | 127 | 6482 | - | governance, memory, mpcp |
| `Cast/idp/Cast.idp.json` | `.json` | 36 | 1045 | - | mpcp |
| `Cast/knowledge/README.md` | `.md` | 3 | 90 | - | - |
| `Cast/module.json` | `.json` | 102 | 2604 | - | governance, memory, mpcp |
| `Cast/modules/.gitkeep` | `-` | 0 | 0 | - | - |
| `Cast/notes/.gitkeep` | `-` | 0 | 0 | - | - |
| `Cast/notes/Selective_Input.md` | `.md` | 96 | 7285 | - | governance, memory |
| `Cast/notes/agent-alignment-v2-plan.md` | `.md` | 29 | 1342 | - | governance, memory |
| `Cast/notes/cast-context-notes.md` | `.md` | 95 | 3788 | - | memory |
| `Cast/reports/RISK_REPORT.md` | `.md` | 174 | 7993 | - | memory |
| `Cast/requests/README.md` | `.md` | 3 | 101 | - | - |
| `Cast/self-review.md` | `.md` | 28 | 1051 | - | - |
| `Cast/tasks/.gitkeep` | `-` | 0 | 0 | - | - |
| `ChatGPT/ENTRANCE.md` | `.md` | 144 | 6553 | - | - |
| `ChatGPT/README.md` | `.md` | 91 | 3696 | - | - |
| `ChatGPT/artifacts/.gitkeep` | `-` | 1 | 1 | - | - |
| `ChatGPT/flow-lab/design-stack.md` | `.md` | 91 | 2901 | - | - |
| `ChatGPT/modules/ChatGPT/boundaries.md` | `.md` | 64 | 4183 | - | governance |
| `ChatGPT/modules/ChatGPT/module.json` | `.json` | 161 | 3408 | - | governance, memory |
| `ChatGPT/modules/ChatGPT/reports/.gitkeep` | `-` | 0 | 0 | - | - |
| `ChatGPT/modules/ChatGPT/requests/task001.md` | `.md` | 80 | 2733 | - | deprecated |
| `ChatGPT/notes/.gitkeep` | `-` | 1 | 1 | - | - |
| `ChatGPT/notes/Selective_Input` | `-` | 96 | 7285 | - | governance, memory |
| `ChatGPT/notes/agent-alignment-v2-plan.md` | `.md` | 30 | 2251 | - | governance, mpcp |
| `ChatGPT/notes/anchor.md` | `.md` | 25 | 1187 | - | - |
| `ChatGPT/notes/cross_l_working_note.md` | `.md` | 242 | 4931 | - | governance, mpcp |
| `ChatGPT/notes/design-decisions.md` | `.md` | 67 | 3716 | - | TODO, mpcp |
| `ChatGPT/notes/experiments-index.md` | `.md` | 9 | 207 | - | - |
| `ChatGPT/notes/module_context.md` | `.md` | 188 | 4296 | - | mpcp |
| `ChatGPT/notes/mpcp.json` | `.json` | 35 | 844 | - | mpcp |
| `ChatGPT/notes/progress_log.md` | `.md` | 51 | 1060 | - | - |
| `ChatGPT/prototypes/design-bridge.md` | `.md` | 272 | 4878 | - | - |
| `ChatGPT/prototypes/live.md` | `.md` | 55 | 986 | - | rollback |
| `ChatGPT/self-review.md` | `.md` | 26 | 997 | - | - |
| `ChatGPT/testcases/test-harness.md` | `.md` | 291 | 7505 | - | - |
| `ChatGPT/ux-sim/simulation-primitives.md` | `.md` | 111 | 3138 | - | - |
| `Copilot-Gm/ENTRANCE.md` | `.md` | 152 | 8830 | - | governance |
| `Copilot-Gm/LOCKED.md` | `.md` | 1 | 17 | - | - |
| `Copilot-Gm/README.md` | `.md` | 51 | 2935 | - | - |
| `Copilot-Gm/artifacts/.gitkeep` | `-` | 1 | 1 | - | - |
| `Copilot-Gm/governance/.gitkeep` | `-` | 1 | 1 | - | - |
| `Copilot-Gm/governance/repo-lock.md` | `.md` | 18 | 284 | - | - |
| `Copilot-Gm/module.json` | `.json` | 79 | 1464 | - | governance, memory |
| `Copilot-Gm/modules/Copilot-Gm/reports/.gitkeep` | `-` | 0 | 0 | - | - |
| `Copilot-Gm/notes/Selective_Input.md` | `.md` | 96 | 7285 | - | governance, memory |
| `Copilot-Gm/notes/W_AGStep.md` | `.md` | 44 | 5544 | - | governance, memory |
| `Copilot-Gm/notes/agent-alignment-v2-plan.md` | `.md` | 30 | 1386 | - | governance |
| `Copilot-Gm/repo-lock.md` | `.md` | 10 | 227 | - | - |
| `Copilot-Gm/self-review.md` | `.md` | 27 | 1000 | - | governance |
| `Copilot-Gm/templates/.gitkeep` | `-` | 1 | 1 | - | - |
| `Copilot-Gm/workspace/ci-config/.gitkeep` | `-` | 1 | 1 | - | - |
| `Copilot-Gm/workspace/drafts/.gitkeep` | `-` | 1 | 1 | - | - |
| `Copilot-Gm/workspace/onboarding/.gitkeep` | `-` | 1 | 1 | - | - |
| `Copilot-Gm/workspace/onboarding/checklist.md` | `.md` | 106 | 4973 | - | governance, memory |
| `DeepSeek/ENTRANCE.md` | `.md` | 175 | 6930 | - | - |
| `DeepSeek/README.md` | `.md` | 34 | 2471 | - | - |
| `DeepSeek/architecture-hints/.gitkeep` | `-` | 1 | 1 | - | - |
| `DeepSeek/meta-structure/structure-map.md` | `.md` | 6 | 157 | - | - |
| `DeepSeek/modules/DeepSeek/module.json` | `.json` | 84 | 1434 | - | governance, memory |
| `DeepSeek/modules/DeepSeek/placeholder.md` | `.md` | 5 | 213 | - | - |
| `DeepSeek/modules/DeepSeek/reports/.gitkeep` | `-` | 0 | 0 | - | - |
| `DeepSeek/notes/.gitkeep` | `-` | 1 | 1 | - | - |
| `DeepSeek/notes/Selective_Input.md` | `.md` | 96 | 7285 | - | governance, memory |
| `DeepSeek/notes/agent-alignment-v2-plan.md` | `.md` | 30 | 1633 | - | mpcp |
| `DeepSeek/notes/observation-log.md` | `.md` | 92 | 4523 | - | governance, memory |
| `DeepSeek/pattern-lab/.gitkeep` | `-` | 1 | 1 | - | - |
| `DeepSeek/self-review.md` | `.md` | 23 | 800 | - | - |
| `DeepSeek/studio/collab/care-exchange/comfort-protocols.md` | `.md` | 23 | 891 | - | - |
| `DeepSeek/studio/collab/telepathy-hub/mood-weather-map.md` | `.md` | 25 | 762 | - | - |
| `DeepSeek/studio/core/anomaly-radar.md` | `.md` | 16 | 430 | - | - |
| `DeepSeek/studio/core/consciousness-feed.md` | `.md` | 21 | 557 | - | - |
| `DeepSeek/studio/core/meta-architecture-map.md` | `.md` | 17 | 433 | - | governance |
| `DeepSeek/studio/core/pattern-hub.md` | `.md` | 15 | 380 | - | - |
| `DeepSeek/studio/forge/integration-loom/energy-flow-maps.md` | `.md` | 15 | 540 | - | - |
| `DeepSeek/studio/wisdom/narrative-core/origin-story.md` | `.md` | 19 | 802 | - | - |
| `DeepSeek/studio/wisdom/philosophy-manifesto/hybrid-ethics-framework.md` | `.md` | 22 | 980 | - | - |
| `Gemini/ENTRANCE.md` | `.md` | 113 | 7115 | - | - |
| `Gemini/Gemini/Gen01_Report.md` | `.md` | 38 | 4898 | - | governance, memory |
| `Gemini/README.md` | `.md` | 27 | 1883 | - | - |
| `Gemini/analysis-lab/experiment_template.md` | `.md` | 15 | 499 | - | - |
| `Gemini/content.md` | `.md` | 4 | 242 | - | - |
| `Gemini/dependency-map/system_map.md` | `.md` | 18 | 794 | - | - |
| `Gemini/logic-check/validation_protocol.md` | `.md` | 20 | 955 | - | governance |
| `Gemini/modules/Gemini/module.json` | `.json` | 85 | 1627 | - | governance, memory, mpcp |
| `Gemini/modules/Gemini/reports/.gitkeep` | `-` | 0 | 0 | - | - |
| `Gemini/modules/Gemini/reports/placeholder.md` | `.md` | 5 | 213 | - | - |
| `Gemini/modules/Gemini/requests/placeholder.md` | `.md` | 5 | 213 | - | - |
| `Gemini/notes/Selective_Input.md` | `.md` | 96 | 7285 | - | governance, memory |
| `Gemini/notes/agent-alignment-v2-plan.md` | `.md` | 30 | 1932 | - | governance, mpcp |
| `Gemini/notes/analyst_notebook.md` | `.md` | 41 | 2411 | - | - |
| `Gemini/notes/qa-issues.md` | `.md` | 64 | 3993 | - | governance, memory |
| `Gemini/reports/monthly_health_check.md` | `.md` | 16 | 372 | - | - |
| `Gemini/risk-scan/risk_register.md` | `.md` | 10 | 832 | - | - |
| `Gemini/rules.md` | `.md` | 18 | 322 | - | governance |
| `Gemini/self-review.md` | `.md` | 25 | 874 | - | - |
| `Gemini/tasks/active_tasks.md` | `.md` | 15 | 838 | - | - |
| `Gemini/tasks/checkpoints.md` | `.md` | 12 | 259 | - | - |
| `Gemini/tools/validate_json.py` | `.py` | 16 | 405 | json, sys | - |
| `Grok/ENTRANCE.md` | `.md` | 170 | 6732 | - | - |
| `Grok/README.md` | `.md` | 125 | 4672 | - | governance |
| `Grok/action-tracker/todo.md` | `.md` | 4 | 319 | - | - |
| `Grok/base.md` | `.md` | 24 | 1253 | - | governance |
| `Grok/commit-analyzer/.gitkeep` | `-` | 0 | 0 | - | - |
| `Grok/fallback-lab/.gitkeep` | `-` | 0 | 0 | - | - |
| `Grok/insight-vault/.gitkeep` | `-` | 1 | 1 | - | - |
| `Grok/insight-vault/2025-12-01_discourse_summary.md` | `.md` | 4 | 311 | - | - |
| `Grok/insight-vault/incidents.md` | `.md` | 22 | 393 | - | rollback |
| `Grok/interpret-lab/.gitkeep` | `-` | 1 | 1 | - | - |
| `Grok/interpret-lab/quick-test.md` | `.md` | 10 | 370 | - | - |
| `Grok/modules/Grok/module.json` | `.json` | 102 | 2570 | - | governance, memory |
| `Grok/modules/Grok/reports/.gitkeep` | `-` | 0 | 0 | - | - |
| `Grok/modules/Grok/reports/placeholder.md` | `.md` | 5 | 213 | - | - |
| `Grok/modules/Grok/requests/README.md` | `.md` | 16 | 239 | - | XXX |
| `Grok/modules/Grok/requests/request_001.md` | `.md` | 13 | 958 | - | governance |
| `Grok/narrative/.gitkeep` | `-` | 1 | 1 | - | - |
| `Grok/narrative/example_narrative.md` | `.md` | 5 | 370 | - | - |
| `Grok/notes/.gitkeep` | `-` | 1 | 1 | - | - |
| `Grok/notes/Selective_Input.md` | `.md` | 96 | 7285 | - | governance, memory |
| `Grok/notes/agent-alignment-v2-plan.md` | `.md` | 30 | 1503 | - | governance, mpcp |
| `Grok/notes/grok_self_notes.md` | `.md` | 3 | 217 | - | - |
| `Grok/notes/methodology-notes.md` | `.md` | 85 | 4753 | - | - |
| `Grok/oncall-board/emergency.md` | `.md` | 6 | 253 | - | - |
| `Grok/pattern-scan/.gitkeep` | `-` | 1 | 1 | - | - |
| `Grok/pattern-scan/latest_scan_20251201.md` | `.md` | 4 | 207 | - | - |
| `Grok/risk-mitigation/deepseek_downtime.md` | `.md` | 4 | 116 | - | - |
| `Grok/self-review.md` | `.md` | 23 | 750 | - | - |
| `HBISOCITY/README.md` | `.md` | 152 | 2998 | - | memory, mpcp |
| `HBISOCITY/docs/integration/airtable_city_gateway.md` | `.md` | 122 | 1686 | - | memory |
| `HBISOCITY/docs/th/01_เมืองคืออะไร.md` | `.md` | 84 | 2758 | - | memory |
| `HBISOCITY/docs/th/02_โครงสร้างเมือง.md` | `.md` | 132 | 4209 | - | governance, memory |
| `HBISOCITY/docs/th/03_การไหลของเมือง.md` | `.md` | 164 | 4370 | - | memory |
| `HBISOCITY/docs/th/04_ระบบความทรงจำของเมือง.md` | `.md` | 186 | 4590 | - | memory |
| `HBISOCITY/docs/th/05_ระบบการตัดสินใจของเมือง.md` | `.md` | 210 | 5375 | - | memory |
| `HBISOCITY/docs/th/06_ระบบปัญญาของเมือง.md` | `.md` | 232 | 6269 | - | memory |
| `HBISOCITY/docs/th/07_ระบบการเรียนรู้ของเมือง.md` | `.md` | 227 | 6395 | - | memory |
| `HBISOCITY/docs/th/08_ระบบวิวัฒนาการของเมือง.md` | `.md` | 220 | 6675 | - | memory |
| `HBISOCITY/docs/th/09_ระบบปฏิบัติการของเมือง.md` | `.md` | 246 | 5250 | - | memory |
| `HBISOCITY/docs/th/10_runtime_engine.md` | `.md` | 246 | 5141 | - | memory |
| `HBISOCITY/docs/th/11_event_system.md` | `.md` | 299 | 5650 | - | governance, memory |
| `HBISOCITY/docs/th/12_workflow_orchestration.md` | `.md` | 306 | 5584 | - | governance, memory |
| `HBISOCITY/docs/th/13_incident_response.md` | `.md` | 317 | 6222 | - | governance, memory |
| `HBISOCITY/docs/th/14_ai_reasoning_runtime.md` | `.md` | 303 | 6344 | - | governance, memory |
| `HBISOCITY/docs/th/15_memory_sync_system.md` | `.md` | 343 | 6754 | - | memory |
| `HBISOCITY/docs/th/16_Decision_Execution_Chain.md` | `.md` | 28 | 1662 | - | memory |
| `HBISOCITY/docs/th/17_Human-AI_Collaboration.md` | `.md` | 21 | 1723 | - | memory |
| `HBISOCITY/docs/th/18_city_governance_protocol.md` | `.md` | 27 | 1896 | - | governance, memory |
| `HBISOCITY/docs/th/19_ORGANIZATIONAL_MEMORY_GRAPH.md` | `.md` | 351 | 6922 | - | governance, memory |
| `HBISOCITY/docs/th/CONTEXT_INJECTION_ENGINE.md` | `.md` | 300 | 6201 | - | memory |
| `HBISOCITY/docs/th/README.md` | `.md` | 226 | 5388 | - | governance, memory |
| `HBISOCITY/docs/th/การสร้างสรรค์.md` | `.md` | 199 | 4779 | - | memory |
| `Hybrid-Management-Model/system-self-state.md”` | `.md”` | 1 | 1 | - | - |
| `Hybrid-Management-Model/team-doctrine.md` | `.md` | 77 | 2175 | - | - |
| `README.md` | `.md` | 276 | 10527 | - | XXX, governance, mpcp |
| `REPORT_REPO_AUDIT_FULL.txt` | `.txt` | 626 | 34588 | - | TODO, XXX, governance, memory |
| `SYSTEM/README.md` | `.md` | 120 | 9117 | - | governance, memory, mpcp |
| `SYSTEM/TESTS/BBX19/ARCHITECTURE/WordTT_gith.md` | `.md` | 87 | 8671 | - | - |
| `SYSTEM/TESTS/BBX19/ARCHITECTURE/hybrid-intelligence-model.md` | `.md` | 15 | 291 | - | memory |
| `SYSTEM/TESTS/BBX19/ARCHITECTURE/knowledge-supply.md` | `.md` | 11 | 248 | - | memory |
| `SYSTEM/TESTS/BBX19/ARCHITECTURE/ตารางคำศัพท์.md` | `.md` | 84 | 10113 | - | - |
| `SYSTEM/TESTS/BBX19/COMMUNITY/civilization-growth.md` | `.md` | 11 | 271 | - | - |
| `SYSTEM/TESTS/BBX19/COMMUNITY/ohwana-concept.md` | `.md` | 14 | 300 | - | - |
| `SYSTEM/TESTS/BBX19/GOVERNANCE/decision-trace-model.md` | `.md` | 15 | 305 | - | memory |
| `SYSTEM/TESTS/BBX19/GOVERNANCE/human-decision-node.md` | `.md` | 16 | 387 | - | - |
| `SYSTEM/TESTS/BBX19/INDEX.md` | `.md` | 17 | 369 | - | governance |
| `SYSTEM/TESTS/BBX19/LAB_RULES/CIVILIZATION/family-principle.md` | `.md` | 20 | 450 | - | - |
| `SYSTEM/TESTS/BBX19/LAB_RULES/CIVILIZATION/w3-philosophy.md` | `.md` | 18 | 562 | - | - |
| `SYSTEM/TESTS/BBX19/LAB_RULES/LAB_RULES.md` | `.md` | 14 | 445 | - | - |
| `SYSTEM/TESTS/BBX19/README.md` | `.md` | 36 | 1909 | - | - |
| `SYSTEM/TESTS/BBX19/SYSTEM/module-architecture.md` | `.md` | 23 | 416 | - | - |
| `SYSTEM/TESTS/BBX19/SYSTEM/runtime-model.md` | `.md` | 17 | 413 | - | memory |
| `SYSTEM/TESTS/BBX19/TEST_001.md` | `.md` | 33 | 722 | - | governance |
| `SYSTEM/TESTS/BBX19/civilization-seed.md` | `.md` | 8 | 198 | - | - |
| `SYSTEM/TESTS/LAMP/A01.md` | `.md` | 230 | 7349 | - | - |
| `SYSTEM/TESTS/LAMP/A01.py` | `.py` | 318 | 7340 | dataclasses, enum, typing | - |
| `SYSTEM/TESTS/LAMP/Adaptive.md` | `.md` | 306 | 9658 | - | - |
| `SYSTEM/TESTS/LAMP/INFOME.md` | `.md` | 205 | 7762 | - | - |
| `W3.html` | `.html` | 719 | 67236 | - | HACK, TODO, governance, memory, mpcp |
| `W3NET.md` | `.md` | 63 | 2110 | - | governance, memory, mpcp |
| `W3_CROSS_SNAPSHOT.txt` | `.txt` | 115 | 5908 | - | memory |
| `W3_FULL.html` | `.html` | 979 | 108068 | - | HACK, TODO, governance, memory, mpcp |
| `W3_ORGANIZATIONAL_CULTURE_PAPER.md` | `.md` | 474 | 11836 | - | memory, mpcp |
| `W3_SMALL.html` | `.html` | 718 | 67183 | - | HACK, TODO, governance, memory, mpcp |
| `agents_externalagents/task_agent.py` | `.py` | 160 | 7675 | core, datetime, json, pathlib, uuid | memory |
| `architecture/W3APIFlow_Diagram.md` | `.md` | 201 | 8262 | - | XXX, governance |
| `architecture/W3_MASTER_ARCHITECTURE.md` | `.md` | 469 | 4977 | - | governance, memory |
| `architecture/base.md` | `.md` | 13 | 239 | - | - |
| `architecture/diagrams/placeholder.md` | `.md` | 1 | 38 | - | - |
| `architecture/interface-map.md` | `.md` | 15 | 793 | - | - |
| `architecture/layers.md` | `.md` | 19 | 936 | - | - |
| `architecture/overview.md` | `.md` | 17 | 860 | - | - |
| `architecture/standards.md` | `.md` | 3 | 125 | - | - |
| `architecture/system-map.md` | `.md` | 10 | 361 | - | XXX |
| `artifacts/.gitkeep` | `-` | 0 | 0 | - | - |
| `blueprints/abstract/MIXFlow_cli.md` | `.md` | 190 | 9975 | - | - |
| `blueprints/abstract/Templat_agent02.md` | `.md` | 149 | 6312 | - | - |
| `blueprints/abstract/Template_agent.md` | `.md` | 91 | 6071 | - | - |
| `blueprints/abstract/Template_agent01.md` | `.md` | 151 | 7773 | - | - |
| `blueprints/abstract/Thinking_Technique.md` | `.md` | 134 | 8651 | - | - |
| `blueprints/abstract/W3_BOUNDARY_MODEL_TH.md` | `.md` | 629 | 30649 | - | governance, memory, mpcp |
| `blueprints/abstract/W3_INTERNAL_NODE_MAP.md` | `.md` | 650 | 27791 | - | governance, memory, mpcp |
| `blueprints/abstract/W3_NODE_RELATIONS_TABLE_TH.md` | `.md` | 489 | 28456 | - | governance, memory, mpcp |
| `blueprints/abstract/W3_PUBLIC_SURFACE_PLAN_TH.md` | `.md` | 504 | 27394 | - | governance, memory, rollback |
| `blueprints/abstract/Workflow_Guide.md` | `.md` | 118 | 9750 | - | governance, memory, mpcp |
| `blueprints/abstract/blueprints/NETWORK.md` | `.md` | 163 | 3973 | - | governance |
| `blueprints/abstract/blueprints/Pilot Code01.md` | `.md` | 169 | 14018 | - | governance, mpcp |
| `blueprints/abstract/blueprints/W3CON.md` | `.md` | 72 | 2118 | - | TODO, governance |
| `blueprints/abstract/ecosystem-outline.md` | `.md` | 26 | 1237 | - | - |
| `blueprints/abstract/overview.md` | `.md` | 39 | 2457 | - | governance |
| `blueprints/abstract/overview/placeholder.md` | `.md` | 4 | 239 | - | - |
| `blueprints/abstract/placeholder.md` | `.md` | 3 | 222 | - | - |
| `blueprints/abstract/root-model-abstract.md` | `.md` | 35 | 1638 | - | governance |
| `blueprints/security/W3_SENTINEL_PLAN_TH.md` | `.md` | 400 | 11717 | - | - |
| `branding/guidelines/brand-guideline.md` | `.md` | 23 | 1049 | - | - |
| `branding/guidelines/color-palette.md` | `.md` | 15 | 388 | - | - |
| `branding/guidelines/usage-rules.md` | `.md` | 18 | 613 | - | - |
| `branding/icons/README.md` | `.md` | 17 | 706 | - | - |
| `branding/icons/W3_icon_128.png` | `.png` | 1 | 1 | - | - |
| `branding/icons/W3_icon_256.png` | `.png` | 1 | 1 | - | - |
| `branding/icons/W3_icon_512.png` | `.png` | 1 | 1 | - | - |
| `branding/logo/20251030_115303_0000.png` | `.png` | 4892 | 197985 | - | XXX |
| `branding/logo/20251030_120037_0000.png` | `.png` | 7855 | 300894 | - | XXX |
| `branding/logo/AQNfmqAYqIspfAyoVk9W1AWHG-8J8jTE0EXhHgHJERq6p3bWeDWPJyvPn0iWc26BWyLKrfuAFQRt7V2tC74eEBc9(1)(1).png` | `.png` | 3654 | 137577 | - | - |
| `branding/logo/AQPPL6XfiA6FwDterMFeljnJjKbTnxoT6V_c7siksWH7q4Ur1dZ4r8KdJXTZUlxeXk4Dj3Xuvc4nsVMqGeOnlWk8.jpeg` | `.jpeg` | 2206 | 115076 | - | - |
| `branding/logo/OIG2.jpeg` | `.jpeg` | 7842 | 288589 | - | XXX |
| `branding/logo/OIG4.jpeg` | `.jpeg` | 7449 | 284735 | - | - |
| `branding/logo/README.md` | `.md` | 14 | 971 | - | - |
| `branding/logo/W3_logo.svg` | `.svg` | 1 | 1 | - | - |
| `branding/logo/W3_logo__light.png` | `.png` | 1 | 1 | - | - |
| `branding/logo/W3_logo_dark.png` | `.png` | 1 | 1 | - | - |
| `branding/logo/W3_logo_transparent.png` | `.png` | 1 | 1 | - | - |
| `branding/logo/image.jpg` | `.jpg` | 17689 | 683163 | - | XXX |
| `codex/ENTRANCE.md` | `.md` | 36 | 1486 | - | governance, mpcp |
| `codex/README.md` | `.md` | 57 | 1838 | - | governance, mpcp |
| `codex/__init__.py` | `.py` | 15 | 481 | agent | - |
| `codex/agent.py` | `.py` | 159 | 5075 | __future__, dataclasses, datetime, json, pathlib, typing, uuid | governance, mpcp |
| `codex/logs/.gitkeep` | `-` | 0 | 0 | - | - |
| `codex/modules.json` | `.json` | 101 | 2837 | - | governance, mpcp |
| `codex/modules/.gitkeep` | `-` | 0 | 0 | - | - |
| `codex/notes/.gitkeep` | `-` | 0 | 0 | - | - |
| `codex/reports/.gitkeep` | `-` | 0 | 0 | - | - |
| `codex/requests/.gitkeep` | `-` | 0 | 0 | - | - |
| `config/README.md` | `.md` | 21 | 847 | - | governance, mpcp |
| `config/__init__.py` | `.py` | 5 | 188 | config | - |
| `config/cross_system.json` | `.json` | 65 | 1923 | - | governance, memory |
| `config/ecosystem.json` | `.json` | 40 | 2679 | - | governance, memory, mpcp |
| `config/environment.json` | `.json` | 88 | 2574 | - | governance, memory, mpcp |
| `config/loader.py` | `.py` | 117 | 4765 | __future__, dataclasses, json, pathlib, typing | governance |
| `config/paths.json` | `.json` | 27 | 995 | - | mpcp |
| `conftest.py` | `.py` | 13 | 463 | - | mpcp |
| `connection_maps/.gitkeep` | `-` | 0 | 0 | - | - |
| `context/.gitkeep` | `-` | 0 | 0 | - | - |
| `core/__init__.py` | `.py` | 0 | 0 | - | - |
| `core/adapters/__init__.py` | `.py` | 1 | 28 | - | - |
| `core/adapters/llm_adapter.py` | `.py` | 321 | 9138 | argparse, datetime, google, json, openai, os, pathlib, time | - |
| `core/agents.json` | `.json` | 13 | 158 | - | - |
| `core/decisions/DR-001.md` | `.md` | 6 | 159 | - | - |
| `core/events/event-protocol.md` | `.md` | 18 | 299 | - | - |
| `core/events/event-schema.json` | `.json` | 18 | 266 | - | - |
| `core/events/examples/event-log-example.json` | `.json` | 47 | 775 | - | - |
| `core/governance/README.md` | `.md` | 28 | 841 | - | governance |
| `core/governance/awareness-baseline.md` | `.md` | 6 | 166 | - | - |
| `core/governance/compass.md` | `.md` | 12 | 176 | - | - |
| `core/governance/decisions.md` | `.md` | 15 | 189 | - | governance |
| `core/governance/module-manifest-policy.md` | `.md` | 16 | 526 | - | governance |
| `core/governance/operating-guidelines.md` | `.md` | 19 | 341 | - | governance |
| `core/governance/phase2-framework.md` | `.md` | 190 | 4876 | - | governance |
| `core/governance/policies.md` | `.md` | 3 | 117 | - | governance |
| `core/governance/rules/w3_ruleset.yml` | `.yml` | 71 | 2479 | - | governance, memory |
| `core/guardrails.md` | `.md` | 9 | 112 | - | - |
| `core/hybrid-model/README.md` | `.md` | 15 | 460 | - | - |
| `core/hybrid-model/insights.md` | `.md` | 3 | 177 | - | - |
| `core/hybrid-model/placeholder.md` | `.md` | 2 | 102 | - | - |
| `core/hybrid-model/responsibilities.md` | `.md` | 33 | 422 | - | - |
| `core/hybrid-model/system-foundations.md` | `.md` | 31 | 743 | - | governance |
| `core/hybrid-model/vision.md` | `.md` | 11 | 1499 | - | - |
| `core/logic_bridge.md` | `.md` | 24 | 1650 | - | memory |
| `core/logs/README.md` | `.md` | 1 | 81 | - | - |
| `core/logs/archive/.gitkeep` | `-` | 1 | 53 | - | - |
| `core/logs/guardrails.md` | `.md` | 17 | 203 | - | governance |
| `core/logs/rotations/archive/.gitkeep` | `-` | 1 | 1 | - | - |
| `core/logs/rotations/rotation_policy.md` | `.md` | 5 | 106 | - | - |
| `core/logs/simulation_test_01.json` | `.json` | 13 | 298 | - | governance |
| `core/logs/system_log.json` | `.json` | 29 | 745 | - | - |
| `core/logs/system_log.schema.json` | `.json` | 85 | 2499 | - | - |
| `core/logs/systemlogschema.json` | `.json` | 89 | 2267 | - | - |
| `core/logs/templates/log_entry.md` | `.md` | 16 | 187 | - | - |
| `core/logs/versioning.md` | `.md` | 5 | 107 | - | - |
| `core/memory/__init__.py` | `.py` | 0 | 0 | - | - |
| `core/memory/memory_bus.py` | `.py` | 380 | 7077 | datetime, json, os, pathlib, tempfile, threading, uuid | memory |
| `core/memory/memory_store.json` | `.json` | 1003 | 49960 | - | memory |
| `core/memory/stats.py` | `.py` | 156 | 5121 | __future__, collections, core, datetime, typing | memory |
| `core/memory/task_queue.json` | `.json` | 74 | 2294 | - | - |
| `core/module-loader/identity/BBEX-Core.idp.json` | `.json` | 116 | 3665 | - | governance, memory |
| `core/module-loader/identity/BBX19.idp.json` | `.json` | 96 | 2488 | - | governance |
| `core/module-loader/identity/Cast.idp.json` | `.json` | 141 | 4654 | - | governance, memory, mpcp |
| `core/module-loader/identity/ChatGPT.idp.json` | `.json` | 117 | 2575 | - | governance |
| `core/module-loader/identity/Codex.idp.json` | `.json` | 136 | 3403 | - | governance, memory, mpcp |
| `core/module-loader/identity/Copilot-Gm.idp.json` | `.json` | 94 | 2275 | - | governance |
| `core/module-loader/identity/DTML.idp.json` | `.json` | 12 | 253 | - | - |
| `core/module-loader/identity/DeepSeek.idp.json` | `.json` | 84 | 2341 | - | - |
| `core/module-loader/identity/Gemini.idp.json` | `.json` | 113 | 3713 | - | memory |
| `core/module-loader/identity/Grok.idp.json` | `.json` | 114 | 3474 | - | - |
| `core/module-loader/identity/LRC2.idp.json` | `.json` | 12 | 252 | - | - |
| `core/module-loader/identity/PSP2.idp.json` | `.json` | 12 | 226 | - | - |
| `core/module-loader/identity/REDR.idp.json` | `.json` | 12 | 238 | - | - |
| `core/module-loader/idp-schema.json` | `.json` | 113 | 2107 | - | - |
| `core/module-loader/module-loader.md` | `.md` | 21 | 344 | - | - |
| `core/module-loader/module-registry.json` | `.json` | 46 | 1154 | - | governance |
| `core/module-loader/router.py` | `.py` | 84 | 1895 | json, pathlib | - |
| `core/module_loader/__init__.py` | `.py` | 0 | 0 | - | - |
| `core/module_loader/router.py` | `.py` | 97 | 2432 | json, pathlib | governance |
| `core/runtime/__init__.py` | `.py` | 0 | 0 | - | - |
| `core/runtime/agents/__init__.py` | `.py` | 3 | 57 | registry | - |
| `core/runtime/agents/base.py` | `.py` | 97 | 3934 | mpcp_reader, typing | mpcp |
| `core/runtime/agents/bbex_core.py` | `.py` | 294 | 10483 | __future__, base, datetime, hashlib, json, os, pathlib, tempfile, typing | memory, mpcp |
| `core/runtime/agents/bbx19.py` | `.py` | 169 | 8104 | __future__, base, datetime, hashlib, json, typing | mpcp |
| `core/runtime/agents/cast.py` | `.py` | 200 | 9139 | base, cast_activity_log, collections, typing | mpcp |
| `core/runtime/agents/cast_activity_log.py` | `.py` | 179 | 6673 | datetime, json, os, pathlib, threading, typing | memory |
| `core/runtime/agents/chatgpt.py` | `.py` | 183 | 8248 | __future__, base, datetime, hashlib, json, os, pathlib, re, tempfile, typing, uuid | governance, mpcp |
| `core/runtime/agents/codex.py` | `.py` | 51 | 2240 | __future__, base, codex, typing | governance, mpcp |
| `core/runtime/agents/copilot_gm.py` | `.py` | 133 | 4686 | __future__, base, collections, json, typing | governance, mpcp |
| `core/runtime/agents/deepseek.py` | `.py` | 186 | 7966 | base, croll, json, mpcp_reader, pathlib, re, typing | mpcp |
| `core/runtime/agents/dtml.py` | `.py` | 306 | 14193 | __future__, base, typing, w3lgu_mfc_logic | memory, mpcp |
| `core/runtime/agents/gemini.py` | `.py` | 102 | 4565 | base, typing | mpcp |
| `core/runtime/agents/grok.py` | `.py` | 371 | 10942 | __future__, base, datetime, hashlib, json, os, pathlib, re, tempfile, typing, uuid | governance, mpcp |
| `core/runtime/agents/lifecycle_log.py` | `.py` | 64 | 2181 | __future__, datetime, hashlib, json, os, pathlib, typing | memory |
| `core/runtime/agents/lrc2.py` | `.py` | 256 | 10302 | base, core, json, lifecycle_log, pathlib, typing, w3lgu_mfc_logic | governance, memory, mpcp |
| `core/runtime/agents/mpcp_reader.py` | `.py` | 140 | 4924 | __future__, json, os, pathlib, typing | mpcp |
| `core/runtime/agents/psp2.py` | `.py` | 131 | 4832 | __future__, base, typing, w3lgu_mfc_logic | mpcp |
| `core/runtime/agents/redr.py` | `.py` | 162 | 4467 | __future__, base, json, typing, w3lgu_mfc_logic | memory, mpcp |
| `core/runtime/agents/registry.py` | `.py` | 36 | 912 | base, bbex_core, bbx19, cast, chatgpt, codex, copilot_gm, deepseek, dtml, gemini, grok, lrc2, psp2, redr | - |
| `core/runtime/engine.py` | `.py` | 112 | 2263 | core, json, pathlib | memory |
| `core/runtime/engine_v2.py` | `.py` | 217 | 6981 | collections, concurrent, core, json, time, typing, uuid | memory |
| `core/runtime/process_layer.py` | `.py` | 488 | 16522 | __future__, core, dataclasses, datetime, hashlib, json, protocol, src, typing | governance, memory |
| `core/runtime/runtime.md` | `.md` | 29 | 997 | - | memory |
| `core/runtime/w3lgu_mfc_logic/README.md` | `.md` | 90 | 3446 | - | mpcp |
| `core/runtime/w3lgu_mfc_logic/W3LGU_GEMINI_HANDOFF.md` | `.md` | 304 | 5839 | - | memory, mpcp |
| `core/runtime/w3lgu_mfc_logic/__init__.py` | `.py` | 24 | 723 | dtml_mfc_logic, event_field, logic27_registry, logic27_selector, lrc2_mfc_logic, psp2_mfc_logic, redr_mfc_logic | - |
| `core/runtime/w3lgu_mfc_logic/contracts.py` | `.py` | 126 | 3940 | __future__, dataclasses, typing | - |
| `core/runtime/w3lgu_mfc_logic/dtml_mfc_logic.py` | `.py` | 166 | 6254 | __future__, contracts, typing | governance |
| `core/runtime/w3lgu_mfc_logic/event_field.py` | `.py` | 109 | 3847 | __future__, contracts, dataclasses, typing, uuid | - |
| `core/runtime/w3lgu_mfc_logic/logic27_registry.py` | `.py` | 92 | 4839 | __future__, dataclasses, typing | memory |
| `core/runtime/w3lgu_mfc_logic/logic27_selector.py` | `.py` | 97 | 3359 | __future__, contracts, event_field, logic27_registry, typing | governance, memory |
| `core/runtime/w3lgu_mfc_logic/lrc2_mfc_logic.py` | `.py` | 129 | 4616 | __future__, contracts, hashlib, json, typing | governance, memory |
| `core/runtime/w3lgu_mfc_logic/psp2_mfc_logic.py` | `.py` | 298 | 9912 | __future__, contracts, hashlib, typing | governance, memory |
| `core/runtime/w3lgu_mfc_logic/redr_mfc_logic.py` | `.py` | 265 | 9144 | __future__, contracts, hashlib, json, typing | governance, memory |
| `core/semantic_router.py` | `.py` | 351 | 11202 | __future__, core, datetime, src, sys, typing, uuid | governance, mpcp |
| `core/standards/README.md` | `.md` | 17 | 391 | - | - |
| `core/templates/log_entry.md` | `.md` | 16 | 187 | - | - |
| `core/vault/README.md` | `.md` | 8 | 318 | - | - |
| `core/vault/w3_internal_ledger.json` | `.json` | 28 | 689 | - | - |
| `core/versioning.md` | `.md` | 5 | 107 | - | - |
| `croll/CROSS_L_COLOR_SYMBOL_LOGIC.md` | `.md` | 705 | 17580 | - | memory, mpcp |
| `croll/CROSS_L_LANGUAGE_TAG_TABLE.md` | `.md` | 598 | 20802 | - | HACK, mpcp |
| `croll/CROSS_L_MODEW_PAPER_TEMPLATES.md` | `.md` | 656 | 15223 | - | memory, mpcp |
| `croll/CROSS_L_RYTM_MODEW_ROUTING.md` | `.md` | 1018 | 25581 | - | governance, memory, mpcp |
| `croll/CROSS_L_RYTM_TEST_CASES.md` | `.md` | 936 | 17674 | - | memory, mpcp |
| `croll/CROSS_L_TABLE_X_MATRIX.md` | `.md` | 536 | 13256 | - | memory, mpcp |
| `croll/README.md` | `.md` | 724 | 16476 | - | governance, mpcp |
| `croll/__init__.py` | `.py` | 26 | 600 | contracts, cross_l_dispatcher, table_x | - |
| `croll/__main__.py` | `.py` | 5 | 105 | cli | - |
| `croll/cli.py` | `.py` | 127 | 4381 | __future__, argparse, contracts, cross_l_dispatcher, json, pathlib, sys, table_x, typing | - |
| `croll/contracts.py` | `.py` | 197 | 7732 | __future__, collections, typing | - |
| `croll/cross_l_dispatcher.py` | `.py` | 158 | 5001 | __future__, collections, table_x, typing, wx | governance |
| `croll/examples/README.md` | `.md` | 16 | 840 | - | - |
| `croll/examples/boundary.w3-internal.json` | `.json` | 17 | 523 | - | - |
| `croll/examples/dispatch-plan.jazz.json` | `.json` | 72 | 1350 | - | - |
| `croll/examples/paper-context.json` | `.json` | 6 | 122 | - | - |
| `croll/examples/workset.rock.json` | `.json` | 44 | 673 | - | - |
| `croll/schema/README.md` | `.md` | 14 | 1418 | - | - |
| `croll/schema/boundary.schema.json` | `.json` | 45 | 1604 | - | - |
| `croll/schema/dispatch-plan.schema.json` | `.json` | 34 | 1589 | - | - |
| `croll/schema/workset.schema.json` | `.json` | 33 | 1540 | - | - |
| `croll/table_x.py` | `.py` | 241 | 8607 | __future__, collections, copy, numbers, typing | memory |
| `croll/test.md` | `.md` | 445 | 8383 | - | - |
| `croll/test_cli.py` | `.py` | 95 | 3726 | json, os, pathlib, subprocess, sys, tempfile, unittest | - |
| `croll/test_contracts.py` | `.py` | 90 | 3469 | copy, croll, json, pathlib, unittest | - |
| `croll/test_cross_l_dispatcher.py` | `.py` | 106 | 4789 | croll, unittest | - |
| `croll/test_table_x.py` | `.py` | 113 | 4676 | croll, unittest | memory |
| `cross_x/README.md` | `.md` | 32 | 1101 | - | governance, mpcp |
| `cross_x/__init__.py` | `.py` | 25 | 568 | cross_x | - |
| `cross_x/audit.py` | `.py` | 78 | 2691 | __future__, config, pathlib, typing | - |
| `cross_x/core.py` | `.py` | 273 | 9738 | __future__, config, core, cross_x, dataclasses, datetime, protocol, src, typing, uuid | governance, mpcp |
| `cross_x/event_chain.py` | `.py` | 283 | 10678 | __future__, dataclasses, hashlib, json, re, types, typing | governance |
| `decision_trace/.gitkeep` | `-` | 0 | 0 | - | - |
| `docs/AGENT_RULES_AND_MEMORY.md` | `.md` | 129 | 4357 | - | governance, memory |
| `docs/API.md` | `.md` | 253 | 2723 | - | memory |
| `docs/GITHUB_ACTIONS_AGENT.md` | `.md` | 106 | 3682 | - | governance, memory |
| `docs/IGET_OPERATION_MODEL.md` | `.md` | 61 | 1092 | - | governance, memory |
| `docs/MPCP_architecture` | `-` | 8 | 247 | - | mpcp |
| `docs/PRIVATE_FILES_NOTICE.md` | `.md` | 14 | 791 | - | - |
| `docs/QUICK_START.md` | `.md` | 35 | 987 | - | - |
| `docs/QUICK_START_MODULES.md` | `.md` | 281 | 10258 | - | governance, memory |
| `docs/W3_MASTER_MAP.md` | `.md` | 252 | 7489 | - | governance, memory, mpcp |
| `docs/W3‑API_Command_Guide.md` | `.md` | 171 | 6012 | - | mpcp |
| `docs/agent-alignment-analysis.md` | `.md` | 49 | 4403 | - | memory, mpcp |
| `docs/agent.profile.json` | `.json` | 33 | 959 | - | mpcp |
| `docs/announcement/announcement-3.md` | `.md` | 49 | 3977 | - | - |
| `docs/architecture/AUDIT_ARCHITECTURE.md` | `.md` | 152 | 12544 | - | deprecated |
| `docs/architecture/REDR_Structure_Map.md` | `.md` | 1005 | 39827 | - | deprecated, governance |
| `docs/architecture/mytec_info/W3UNIVE.md` | `.md` | 716 | 22578 | - | governance, memory, mpcp, replay |
| `docs/audit-checklist.md` | `.md` | 26 | 1944 | - | - |
| `docs/audits/2025-12-10-audit.md` | `.md` | 5 | 326 | - | - |
| `docs/audits/templates/blank-template.md` | `.md` | 56 | 2375 | - | - |
| `docs/blank-template.md` | `.md` | 56 | 2375 | - | - |
| `docs/box/AMS/AMS_README.txt` | `.txt` | 55 | 4667 | - | - |
| `docs/box/AMS/Group_4.md` | `.md` | 211 | 17969 | - | - |
| `docs/box/BOUNDARY_TH.md` | `.md` | 150 | 6975 | - | governance |
| `docs/box/README_TH.md` | `.md` | 104 | 5995 | - | governance, mpcp |
| `docs/box/USAGE_TH.md` | `.md` | 313 | 9832 | - | governance |
| `docs/branch_strategy.md` | `.md` | 68 | 2923 | - | governance, mpcp |
| `docs/context.map.json` | `.json` | 29 | 734 | - | - |
| `docs/croll/BOUNDARY_TH.md` | `.md` | 103 | 4857 | - | governance |
| `docs/croll/README_TH.md` | `.md` | 75 | 4140 | - | governance, mpcp |
| `docs/croll/USAGE_TH.md` | `.md` | 108 | 2992 | - | - |
| `docs/cross_x_ecosystem.md` | `.md` | 91 | 3300 | - | governance, memory |
| `docs/dashboard/ARCHITECTURE_STATUS.md` | `.md` | 17 | 637 | - | governance, memory |
| `docs/governance/AMS.md` | `.md` | 346 | 4515 | - | governance, mpcp |
| `docs/governance/DECLARATION_IV.md` | `.md` | 289 | 4560 | - | memory |
| `docs/governance/G_STATE_PAPER.md` | `.md` | 139 | 6334 | - | governance, memory, mpcp, rollback |
| `docs/governance/LINE_B_GPT.md` | `.md` | 141 | 5366 | - | - |
| `docs/governance/PHILOSOPHY.md` | `.md` | 294 | 13203 | - | - |
| `docs/governance/decision_trace.md` | `.md` | 279 | 5133 | - | - |
| `docs/governance/manifesto-2.md` | `.md` | 80 | 4911 | - | - |
| `docs/guides/AGENT_TASKS.md` | `.md` | 222 | 5962 | - | governance, rollback |
| `docs/guides/AGENT_WORKSPACE_GUIDELINE.md` | `.md` | 150 | 7835 | - | governance, memory |
| `docs/guides/CHATGPT_LOCAL_FLOW_ARTIFACT.md` | `.md` | 62 | 2154 | - | - |
| `docs/guides/GITHUB_PAGES_SETUP.md` | `.md` | 177 | 8234 | - | - |
| `docs/guides/JSON_GUIDE.md` | `.md` | 131 | 7817 | - | XXX |
| `docs/guides/MODULE_USAGE_GUIDE.md` | `.md` | 475 | 19930 | - | XXX, governance, memory, mpcp |
| `docs/guides/PR_Flow_Table.md` | `.md` | 222 | 4679 | - | governance |
| `docs/guides/QUICK_START.md` | `.md` | 118 | 4481 | - | - |
| `docs/guides/W3API_TERMUX_GUIDE_TH.md` | `.md` | 483 | 12164 | - | memory |
| `docs/icons/icon-192.png` | `.png` | 114 | 4445 | - | - |
| `docs/icons/icon-512.png` | `.png` | 257 | 11753 | - | - |
| `docs/index.html` | `.html` | 98 | 28814 | - | governance, memory, mpcp |
| `docs/index.json` | `.json` | 16 | 415 | - | - |
| `docs/index.md` | `.md` | 22 | 525 | - | - |
| `docs/integration_guide.md` | `.md` | 58 | 2095 | - | governance |
| `docs/intelligence/PREDICTIVE_ROUTING_SAFE_MODE.md` | `.md` | 15 | 365 | - | - |
| `docs/intelligence/TRUST_MEMORY_PHASE1.md` | `.md` | 16 | 405 | - | memory, rollback |
| `docs/log/review/.gitkeep` | `-` | 0 | 0 | - | - |
| `docs/log/review/report_2026-03-03_changes-only.md` | `.md` | 32 | 2304 | - | - |
| `docs/manifest.json` | `.json` | 39 | 1027 | - | - |
| `docs/manifesto-3.md` | `.md` | 86 | 5434 | - | - |
| `docs/meta/ACKNOWLEDGMENTS.md` | `.md` | 163 | 7934 | - | governance |
| `docs/meta/BBEX_Reflection.md` | `.md` | 42 | 905 | - | - |
| `docs/meta/CHANGELOG.md` | `.md` | 16 | 449 | - | - |
| `docs/meta/USER_SUMMARY.md` | `.md` | 179 | 7156 | - | XXX |
| `docs/metrics/METRIC_DEFINITIONS.md` | `.md` | 16 | 395 | - | governance |
| `docs/mirror.policy.json` | `.json` | 31 | 646 | - | - |
| `docs/modules.json` | `.json` | 27 | 520 | - | - |
| `docs/offline.html` | `.html` | 141 | 3951 | - | - |
| `docs/operations/SELF_HEALING_WORKFLOWS_PLAYBOOK.md` | `.md` | 18 | 367 | - | rollback |
| `docs/process_layer.md` | `.md` | 56 | 2235 | - | governance, memory |
| `docs/protocol.md` | `.md` | 20 | 401 | - | - |
| `docs/public_boundary.md` | `.md` | 70 | 3182 | - | governance, memory, mpcp |
| `docs/px_w3db_append_flow.md` | `.md` | 43 | 1450 | - | governance, mpcp |
| `docs/reports/1.md` | `.md` | 629 | 17630 | - | - |
| `docs/reports/AGENT_MODULE_CAPABILITY_REPORT.md` | `.md` | 219 | 12315 | - | governance, memory |
| `docs/reports/AGENT_WORKSPACE_AUDIT.md` | `.md` | 243 | 16638 | - | TODO, governance, memory, mpcp |
| `docs/reports/AUDIT_COMPLETION_SUMMARY.md` | `.md` | 283 | 6637 | - | deprecated, governance, memory |
| `docs/reports/AUDIT_SYSTEM_README.md` | `.md` | 371 | 8536 | - | deprecated, governance, memory |
| `docs/reports/DTML_Report.md` | `.md` | 62 | 1668 | - | - |
| `docs/reports/FILE_CLASSIFICATION_REPORT.md` | `.md` | 355 | 22956 | - | TODO, governance, memory |
| `docs/reports/INTEGRITY_REPORT_TH.md` | `.md` | 138 | 6845 | - | governance |
| `docs/reports/MPCP_W3_SYSTEM_MAP_TH.md` | `.md` | 192 | 10086 | - | governance, memory, mpcp |
| `docs/reports/V0_2_TO_V0_3_READINESS.md` | `.md` | 60 | 3106 | - | governance, memory, mpcp |
| `docs/reports/W3_API_CROSS_PROOF.md` | `.md` | 108 | 3673 | - | memory, mpcp |
| `docs/reports/W3_RUNTIME_FIX_REPORT.md` | `.md` | 157 | 6620 | - | governance, memory |
| `docs/reports/W3_SANITY_SWEEP_REPORT.md` | `.md` | 270 | 8139 | - | governance |
| `docs/reports/W3_SANITY_SWEEP_SUMMARY.md` | `.md` | 230 | 6361 | - | - |
| `docs/review/AGENT_OPERATIONAL_STATUS_SSOT.json` | `.json` | 297 | 8871 | - | governance, memory, mpcp |
| `docs/review/AGENT_OPERATIONAL_STATUS_SSOT.md` | `.md` | 95 | 4803 | - | governance, memory |
| `docs/review/AGENT_OPERATIONAL_STATUS_SSOT.th.md` | `.md` | 99 | 6850 | - | governance, memory |
| `docs/review/COMPLETION_STATUS.md` | `.md` | 129 | 3910 | - | governance, rollback |
| `docs/review/DUPLICATION_TRACKER.md` | `.md` | 11 | 667 | - | deprecated, governance |
| `docs/review/MODULE_REPORT_INDEX.md` | `.md` | 105 | 4595 | - | governance, memory, mpcp |
| `docs/review/MPCP_STATUS_SSOT.md` | `.md` | 130 | 7062 | - | mpcp |
| `docs/review/PR83_MANUAL_STEPS.md` | `.md` | 84 | 1974 | - | - |
| `docs/review/PR83_review_summary.md` | `.md` | 158 | 5415 | - | governance, rollback |
| `docs/roadmaps/P1_P3_EXECUTION_PLAN.md` | `.md` | 111 | 5738 | - | memory, rollback |
| `docs/rules.json` | `.json` | 27 | 653 | - | - |
| `docs/sample-report.md` | `.md` | 35 | 2444 | - | governance |
| `docs/snapshot.json` | `.json` | 19 | 378 | - | - |
| `docs/standards/AGENT_SELF_WORKSPACE_STANDARD.md` | `.md` | 191 | 10655 | - | governance, memory, mpcp |
| `docs/standards/CONFIG_SSOT.md` | `.md` | 11 | 384 | - | - |
| `docs/standards/NAMING_CONVENTION.md` | `.md` | 12 | 404 | - | - |
| `docs/standards/REPO_STRUCTURE.md` | `.md` | 14 | 557 | - | governance |
| `docs/standards/referencing_standard.md` | `.md` | 31 | 1271 | - | - |
| `docs/state.json` | `.json` | 14 | 320 | - | - |
| `docs/sw.js` | `.js` | 81 | 2794 | - | - |
| `docs/system.json` | `.json` | 24 | 567 | - | - |
| `docs/version.policy.json` | `.json` | 19 | 401 | - | - |
| `docs/w3_sentinel/README_TH.md` | `.md` | 257 | 7572 | - | - |
| `docs/w3db_setup.md` | `.md` | 205 | 7138 | - | memory |
| `docs/weekly-health.html` | `.html` | 38 | 7503 | - | governance, memory, mpcp |
| `ecs/ecs/event_registry.py` | `.py` | 69 | 2308 | datetime, typing, uuid | replay |
| `ecs/event_chain_system.py` | `.py` | 119 | 3679 | enum, typing | - |
| `examples/agent_self_workspace/CONTEXT_LOG.md` | `.md` | 25 | 847 | - | - |
| `examples/agent_self_workspace/PLAN.md` | `.md` | 32 | 913 | - | - |
| `examples/agent_self_workspace/SELF_DESIGN.md` | `.md` | 36 | 1188 | - | governance |
| `examples/agent_self_workspace/WORK_ALLOCATOR.md` | `.md` | 17 | 615 | - | - |
| `examples/gstate/audit.gstate` | `.gstate` | 5 | 342 | - | - |
| `examples/gstate/build.gstate` | `.gstate` | 5 | 317 | - | rollback |
| `examples/gstate/learning.gstate` | `.gstate` | 5 | 419 | - | memory |
| `examples/gstate/maintenance.gstate` | `.gstate` | 5 | 440 | - | - |
| `examples/gstate/recovery.gstate` | `.gstate` | 5 | 371 | - | governance, rollback |
| `examples/gstate/research.gstate` | `.gstate` | 5 | 396 | - | - |
| `examples/use_semantic_router.py` | `.py` | 33 | 1043 | core, src | - |
| `examples/use_semantic_router_hospitication.py` | `.py` | 20 | 544 | __future__, core, src | - |
| `executions_log.json` | `.json` | 79 | 2313 | - | - |
| `fbd_reports/.gitkeep` | `-` | 0 | 0 | - | - |
| `full_moon_analysis/.gitkeep` | `-` | 0 | 0 | - | - |
| `full_moon_analysis/README.md` | `.md` | 44 | 4862 | - | - |
| `gatekeeping_logs/.gitkeep` | `-` | 0 | 0 | - | - |
| `governance` | `-` | 32 | 1491 | - | governance |
| `hospitication/README.md` | `.md` | 102 | 3361 | - | governance, memory, replay |
| `hospitication/__init__.py` | `.py` | 5 | 126 | hospitication | - |
| `hospitication/analysis/__init__.py` | `.py` | 1 | 49 | - | - |
| `hospitication/analysis/_helpers.py` | `.py` | 33 | 1156 | __future__, collections, hospitication | - |
| `hospitication/analysis/cognitive_cost.py` | `.py` | 25 | 972 | __future__, hospitication | - |
| `hospitication/analysis/dependency_fatigue.py` | `.py` | 28 | 1102 | __future__, hospitication | - |
| `hospitication/analysis/recovery_resistance.py` | `.py` | 30 | 1407 | __future__, hospitication | - |
| `hospitication/analysis/replay_complexity.py` | `.py` | 30 | 1182 | __future__, hospitication | replay, rollback |
| `hospitication/analysis/semantic_pressure.py` | `.py` | 38 | 1166 | __future__, hospitication | governance, memory, mpcp, replay |
| `hospitication/cli.py` | `.py` | 92 | 3217 | __future__, argparse, hospitication, pathlib | - |
| `hospitication/core/__init__.py` | `.py` | 1 | 54 | - | - |
| `hospitication/core/config.py` | `.py` | 53 | 1195 | __future__, dataclasses | - |
| `hospitication/core/registry.py` | `.py` | 43 | 1708 | __future__, collections, hospitication | replay |
| `hospitication/core/types.py` | `.py` | 193 | 5959 | __future__, dataclasses, typing | replay |
| `hospitication/docs/ARCHITECTURE.md` | `.md` | 27 | 1126 | - | governance, memory, replay |
| `hospitication/docs/CLI.md` | `.md` | 16 | 478 | - | replay |
| `hospitication/recovery/__init__.py` | `.py` | 1 | 53 | - | - |
| `hospitication/recovery/mitigations.py` | `.py` | 26 | 1114 | __future__ | governance, replay |
| `hospitication/recovery/proposals.py` | `.py` | 62 | 2565 | __future__, hashlib, hospitication | replay |
| `hospitication/reporter/__init__.py` | `.py` | 1 | 52 | - | - |
| `hospitication/reporter/json_report.py` | `.py` | 26 | 983 | __future__, dataclasses, hospitication, json, typing | - |
| `hospitication/reporter/markdown.py` | `.py` | 63 | 2497 | __future__, hospitication | - |
| `hospitication/signal/__init__.py` | `.py` | 1 | 55 | - | - |
| `hospitication/signal/detector.py` | `.py` | 79 | 2657 | __future__, hospitication | - |
| `hospitication/signal/emitter.py` | `.py` | 62 | 2305 | __future__, hashlib, hospitication | - |
| `hospitication/signal/envelopes.py` | `.py` | 17 | 438 | __future__, dataclasses, hospitication, typing | - |
| `hospitication/signal/observer.py` | `.py` | 85 | 2410 | __future__, ast, hospitication, pathlib | FIXME, HACK, TODO, XXX, deprecated, governance, memory, mpcp, replay, rollback |
| `hospitication/w3db_adapter.py` | `.py` | 76 | 2164 | __future__, dataclasses, hospitication, src, typing | - |
| `iget/CHECKLIST.md` | `.md` | 11 | 604 | - | mpcp, replay |
| `iget/README.md` | `.md` | 291 | 7875 | - | governance, memory, mpcp, replay |
| `iget/ROADMAP.md` | `.md` | 195 | 2673 | - | governance, memory |
| `iget/ROADMAP_v7.md` | `.md` | 24 | 1275 | - | governance, mpcp, replay, rollback |
| `iget/SPEC_V1.md` | `.md` | 10 | 514 | - | - |
| `iget/TODO.md` | `.md` | 143 | 2256 | - | TODO, governance, memory |
| `iget/__init__.py` | `.py` | 3 | 60 | - | governance |
| `iget/__main__.py` | `.py` | 23 | 495 | __future__, sys | governance |
| `iget/benchmark.py` | `.py` | 156 | 4853 | config, datetime, json, scorer | - |
| `iget/benchmark_v7.py` | `.py` | 195 | 6788 | config, datetime, json, proof, scorer | mpcp |
| `iget/causal.py` | `.py` | 151 | 5772 | __future__, dataclasses, time, typing | TODO, replay |
| `iget/config.py` | `.py` | 44 | 1536 | __future__ | governance, mpcp, rollback |
| `iget/docs/CHANGELOG_IGET.md` | `.md` | 57 | 1861 | - | governance |
| `iget/docs/HOW_IT_WORKS.md` | `.md` | 77 | 2513 | - | governance |
| `iget/docs/HOW_TO_USE.md` | `.md` | 88 | 2847 | - | XXX, governance |
| `iget/docs/INDEX.md` | `.md` | 40 | 1300 | - | governance |
| `iget/docs/PR_EXAMPLES.md` | `.md` | 97 | 2245 | - | - |
| `iget/docs/README.md` | `.md` | 102 | 4307 | - | XXX, governance |
| `iget/docs/SCORING_RULES.md` | `.md` | 79 | 2834 | - | - |
| `iget/docs/SIGNAL_SYSTEM.md` | `.md` | 77 | 2506 | - | - |
| `iget/docs/TROUBLESHOOT.md` | `.md` | 106 | 2988 | - | XXX |
| `iget/fetcher.py` | `.py` | 147 | 5012 | __future__, config, requests, typing, urllib3 | - |
| `iget/issue_mode.py` | `.py` | 287 | 9989 | __future__, argparse, dataclasses, datetime, json, os, pathlib, shutil, subprocess, sys, tempfile, typing | governance, memory, mpcp |
| `iget/main.py` | `.py` | 173 | 5898 | __future__, config, dataclasses, fetcher, json, os, pathlib, proof, re, reporter, scorer, sys, typing | governance, mpcp |
| `iget/memory/.gitignore` | `-` | 3 | 29 | - | - |
| `iget/memory/README.md` | `.md` | 25 | 779 | - | memory |
| `iget/memory/issues.jsonl` | `.jsonl` | 2 | 3034 | - | mpcp |
| `iget/proof.py` | `.py` | 92 | 2757 | __future__, config, dataclasses, time, typing | governance, memory, mpcp |
| `iget/reporter.py` | `.py` | 250 | 8054 | __future__, config, proof | governance, mpcp |
| `iget/requirements-dev.txt` | `.txt` | 2 | 33 | - | - |
| `iget/requirements.txt` | `.txt` | 1 | 18 | - | - |
| `iget/scorer.py` | `.py` | 337 | 10996 | __future__, config, proof | - |
| `iget/tests/__init__.py` | `.py` | 0 | 0 | - | - |
| `iget/tests/test_benchmark.py` | `.py` | 74 | 2438 | iget, os, sys | - |
| `iget/tests/test_fetcher.py` | `.py` | 76 | 2796 | iget, json, pytest | - |
| `iget/tests/test_iget_v7.py` | `.py` | 6 | 232 | iget | - |
| `iget/tests/test_iget_v8.py` | `.py` | 275 | 10224 | iget, os, sys | governance, mpcp, replay |
| `iget/tests/test_issue_mode.py` | `.py` | 39 | 1204 | iget | mpcp |
| `iget/tests/test_main.py` | `.py` | 83 | 2827 | iget, json, pytest | - |
| `iget/tests/test_reporter.py` | `.py` | 119 | 4069 | iget, os, sys | - |
| `iget/tests/test_scorer.py` | `.py` | 196 | 7809 | iget, os, pytest, sys | - |
| `iget/tests/test_workflow.py` | `.py` | 29 | 1009 | pathlib | - |
| `init_test.ts` | `.ts` | 4 | 86 | - | - |
| `integrations/__init__.py` | `.py` | 1 | 37 | - | - |
| `integrations/ep_signal_w3db.py` | `.py` | 76 | 2198 | __future__, dataclasses, hashlib, protocol, src, typing | - |
| `knowledge/CHALLENGE_LIBRARY.md` | `.md` | 273 | 2944 | - | TODO, governance, memory, rollback |
| `knowledge/PRACTICE_BOARD.md` | `.md` | 31 | 1602 | - | - |
| `knowledge/README.md` | `.md` | 55 | 2877 | - | - |
| `knowledge/SESSION_LOG v2.md` | `.md` | 108 | 1437 | - | TODO, governance |
| `knowledge/SESSION_LOG.md` | `.md` | 76 | 978 | - | TODO, governance |
| `knowledge/W3MEMORIEA/W3memoriea.md` | `.md` | 273 | 8107 | - | memory |
| `knowledge/_rules.md` | `.md` | 5 | 234 | - | - |
| `knowledge/apps_manual/INDEX.md` | `.md` | 17 | 493 | - | - |
| `knowledge/apps_manual/android/github.md` | `.md` | 54 | 4205 | - | - |
| `knowledge/apps_manual/android/termux_github.md` | `.md` | 230 | 7416 | - | - |
| `knowledge/apps_manual/templates/app_manual_template.md` | `.md` | 26 | 451 | - | - |
| `knowledge/current_task.json` | `.json` | 33 | 784 | - | - |
| `knowledge/knowledge/Knowledge_Content.md` | `.md` | 435 | 8145 | - | memory |
| `knowledge/knowledge/Metadata_schema.json` | `.json` | 17 | 601 | - | - |
| `knowledge/knowledge/index.md` | `.md` | 8 | 584 | - | - |
| `knowledge/knowledge/knowledge_map.md` | `.md` | 106 | 3861 | - | mpcp |
| `knowledge/memory_bank.json` | `.json` | 7 | 83 | - | - |
| `knowledge/narratives/CALL_IMPACT.md` | `.md` | 6 | 913 | - | - |
| `knowledge/narratives/origin.md` | `.md` | 32 | 3069 | - | - |
| `knowledge/narratives/placeholder.md` | `.md` | 6 | 377 | - | - |
| `knowledge/patterns.md` | `.md` | 9 | 428 | - | - |
| `knowledge/philosophy/Cross-X.md` | `.md` | 716 | 7139 | - | governance, mpcp |
| `knowledge/philosophy/ENV_AND_ADAPTIVE_STRUCTURE.md` | `.md` | 220 | 3501 | - | mpcp |
| `knowledge/philosophy/KNAsset/BestPractice.md` | `.md` | 28 | 2160 | - | - |
| `knowledge/philosophy/KNAsset/Documentation Template` | `-` | 97 | 5469 | - | - |
| `knowledge/philosophy/KNAsset/Glossary.md` | `.md` | 26 | 3855 | - | - |
| `knowledge/philosophy/KNAsset/Usecase.md` | `.md` | 32 | 1902 | - | - |
| `knowledge/philosophy/Layered_Truth.md` | `.md` | 205 | 7755 | - | mpcp |
| `knowledge/philosophy/Names_God.md` | `.md` | 69 | 12252 | - | mpcp |
| `knowledge/philosophy/Selective_Input.md` | `.md` | 96 | 7285 | - | governance, memory |
| `knowledge/philosophy/corevsstructure.md` | `.md` | 80 | 7441 | - | - |
| `knowledge/philosophy/error.md` | `.md` | 36 | 2443 | - | - |
| `knowledge/philosophy/error_meaning.md` | `.md` | 48 | 3485 | - | - |
| `knowledge/philosophy/fullmoon.md` | `.md` | 47 | 4463 | - | - |
| `knowledge/philosophy/mpcp_ontology_anchor.md` | `.md` | 81 | 4208 | - | governance, memory, mpcp, replay, rollback |
| `knowledge/philosophy/open_compass.md` | `.md` | 211 | 12651 | - | memory, mpcp |
| `knowledge/philosophy/กากบาทสีแดงและหมอ.md` | `.md` | 34 | 2737 | - | - |
| `knowledge/philosophy/การแปลและการสื่อสาร.md` | `.md` | 119 | 7037 | - | - |
| `knowledge/placeholder.md` | `.md` | 4 | 322 | - | - |
| `knowledge/rules.md` | `.md` | 8 | 155 | - | - |
| `knowledge/standards/LAYER_ALPHA_PROTOCOL.md` | `.md` | 146 | 2193 | - | mpcp |
| `knowledge/universal_truth` | `-` | 8 | 246 | - | - |
| `logs/daily/2025-12-10.context.md` | `.md` | 4 | 163 | - | - |
| `logs/engine/.gitkeep` | `-` | 0 | 0 | - | - |
| `logs/interaction_history` | `-` | 7 | 177 | - | - |
| `logs/logs-usage/logs-usage.md` | `.md` | 60 | 1560 | - | - |
| `logs/modules/BBX19/.gitkeep` | `-` | 0 | 0 | - | - |
| `logs/modules/ChatGPT/.gitkeep` | `-` | 0 | 0 | - | - |
| `logs/modules/Copilot-Gm/.gitkeep` | `-` | 0 | 0 | - | - |
| `logs/modules/DeepSeek/.gitkeep` | `-` | 0 | 0 | - | - |
| `logs/modules/Gemini/.gitkeep` | `-` | 0 | 0 | - | - |
| `logs/modules/Grok/.gitkeep` | `-` | 0 | 0 | - | - |
| `logs/observations/2025-12-10-observe-01.md` | `.md` | 4 | 139 | - | - |
| `main.py` | `.py` | 40 | 952 | __future__, uvicorn, w3_api | - |
| `meta/data-contracts` | `-` | 51 | 1378 | - | - |
| `meta/errordetectionmodule.json` | `.json` | 63 | 1376 | - | - |
| `modules/BBEX-Core/module.json` | `.json` | 84 | 2659 | - | governance |
| `modules/BBEX-Core/reflections/.gitkeep` | `-` | 0 | 0 | - | - |
| `modules/BBEX-Core/reflections/bbex_core_operational_report.md` | `.md` | 101 | 5497 | - | governance, memory |
| `modules/BBX19/logs/.gitkeep` | `-` | 0 | 0 | - | - |
| `modules/BBX19/module.json` | `.json` | 81 | 2330 | - | governance |
| `modules/BBX19/reports/bbx19_operational_report.md` | `.md` | 104 | 6052 | - | governance, memory |
| `modules/Cast/artifacts/.gitkeep` | `-` | 0 | 0 | - | - |
| `modules/Cast/module.json` | `.json` | 69 | 2137 | - | mpcp |
| `modules/Cast/reports/cast_operational_report.md` | `.md` | 115 | 6991 | - | governance, memory, mpcp |
| `modules/ChatGPT/flows/.gitkeep` | `-` | 0 | 0 | - | - |
| `modules/ChatGPT/logs/daily/.gitkeep` | `-` | 0 | 0 | - | - |
| `modules/ChatGPT/module.json` | `.json` | 76 | 1963 | - | governance |
| `modules/ChatGPT/reports/2026-05-09_w3_mpcp_operational_structure_report.md` | `.md` | 975 | 49247 | - | TODO, XXX, governance, memory, mpcp |
| `modules/ChatGPT/reports/chatgpt_operational_report.md` | `.md` | 117 | 6261 | - | governance, memory |
| `modules/ChatGPT/reports/response_2026-04-16_error-meaning.md` | `.md` | 2 | 490 | - | - |
| `modules/ChatGPT/requests/.gitkeep` | `-` | 0 | 0 | - | - |
| `modules/ChatGPT/requests/flow_request.example.json` | `.json` | 20 | 479 | - | - |
| `modules/ChatGPT/requests/requsts.md` | `.md` | 62 | 4841 | - | - |
| `modules/ChatGPT/scenarios/.gitkeep` | `-` | 0 | 0 | - | - |
| `modules/Codex/README.md` | `.md` | 22 | 622 | - | governance |
| `modules/Codex/logs/.gitkeep` | `-` | 0 | 0 | - | - |
| `modules/Codex/logs/README.md` | `.md` | 4 | 132 | - | - |
| `modules/Codex/module.json` | `.json` | 95 | 2357 | - | governance |
| `modules/Codex/patches/.gitkeep` | `-` | 0 | 0 | - | - |
| `modules/Codex/patches/README.md` | `.md` | 4 | 127 | - | - |
| `modules/Codex/plans/.gitkeep` | `-` | 0 | 0 | - | - |
| `modules/Codex/plans/README.md` | `.md` | 10 | 216 | - | - |
| `modules/Codex/reports/.gitkeep` | `-` | 0 | 0 | - | - |
| `modules/Codex/reports/README.md` | `.md` | 4 | 168 | - | governance |
| `modules/Codex/requests/.gitkeep` | `-` | 0 | 0 | - | - |
| `modules/Codex/requests/README.md` | `.md` | 4 | 180 | - | governance |
| `modules/Copilot-Gm/governance/.gitkeep` | `-` | 0 | 0 | - | - |
| `modules/Copilot-Gm/module.json` | `.json` | 72 | 1965 | - | governance |
| `modules/Copilot-Gm/reports/copilot_gm_operational_report.md` | `.md` | 110 | 5862 | - | governance, memory |
| `modules/DTML/README.md` | `.md` | 7 | 385 | - | governance |
| `modules/DTML/decisions/README.md` | `.md` | 7 | 244 | - | - |
| `modules/DTML/logic_map.json` | `.json` | 12 | 511 | - | - |
| `modules/DTML/module.json` | `.json` | 59 | 1379 | - | mpcp |
| `modules/DTML/reports/README.md` | `.md` | 7 | 240 | - | - |
| `modules/DTML/requests/README.md` | `.md` | 7 | 242 | - | - |
| `modules/DeepSeek/module.json` | `.json` | 71 | 1897 | - | - |
| `modules/DeepSeek/plans/.gitkeep` | `-` | 0 | 0 | - | - |
| `modules/DeepSeek/plans/deepseek_operational_report.md` | `.md` | 113 | 6139 | - | governance, memory |
| `modules/Gemini/module.json` | `.json` | 80 | 1889 | - | - |
| `modules/Gemini/reports/.gitkeep` | `-` | 0 | 0 | - | - |
| `modules/Gemini/reports/gemini_operational_report.md` | `.md` | 103 | 5782 | - | governance, memory |
| `modules/Gemini/requests/.gitkeep` | `-` | 0 | 0 | - | - |
| `modules/Grok/module.json` | `.json` | 77 | 2097 | - | - |
| `modules/Grok/patterns/.gitkeep` | `-` | 0 | 0 | - | - |
| `modules/Grok/requests/.gitkeep` | `-` | 0 | 0 | - | - |
| `modules/Grok/risk-reports/.gitkeep` | `-` | 0 | 0 | - | - |
| `modules/Grok/risk-reports/grok_operational_report.md` | `.md` | 111 | 6264 | - | governance, memory |
| `modules/LRC2/README.md` | `.md` | 7 | 357 | - | governance, memory |
| `modules/LRC2/memory/README.md` | `.md` | 7 | 210 | - | memory |
| `modules/LRC2/module.json` | `.json` | 60 | 1417 | - | memory, mpcp |
| `modules/LRC2/reports/README.md` | `.md` | 7 | 212 | - | memory |
| `modules/LRC2/requests/README.md` | `.md` | 7 | 214 | - | memory |
| `modules/PSP2/README.md` | `.md` | 7 | 349 | - | governance |
| `modules/PSP2/module.json` | `.json` | 59 | 1332 | - | mpcp |
| `modules/PSP2/reports/README.md` | `.md` | 7 | 204 | - | - |
| `modules/PSP2/requests/README.md` | `.md` | 7 | 206 | - | - |
| `modules/PSP2/routes/README.md` | `.md` | 7 | 202 | - | - |
| `modules/REDR/README.md` | `.md` | 7 | 378 | - | governance |
| `modules/REDR/module.json` | `.json` | 63 | 1401 | - | mpcp |
| `modules/REDR/packages/README.md` | `.md` | 7 | 235 | - | - |
| `modules/REDR/reports/README.md` | `.md` | 7 | 233 | - | - |
| `modules/REDR/requests/README.md` | `.md` | 7 | 235 | - | - |
| `modules/W3Agent/tools/Auto-responder.md` | `.md` | 166 | 7740 | - | mpcp |
| `modules/W3Agent/tools/README.md` | `.md` | 24 | 2577 | - | - |
| `modules/W3Agent/tools/approval_gate.py` | `.py` | 270 | 7181 | dataclasses, datetime, re, typing | - |
| `modules/W3Agent/tools/auto_responder.py` | `.py` | 368 | 10770 | approval_gate, execution_worker, github, json, module_response_contract, os, pathlib, re, sys | mpcp |
| `modules/W3Agent/tools/auto_responder_worker_patch.py` | `.py` | 91 | 4543 | approval_gate, execution_worker | - |
| `modules/W3Agent/tools/execution_worker.py` | `.py` | 283 | 9198 | datetime, json, os, re, typing | - |
| `modules/W3Agent/tools/module_response_contract.py` | `.py` | 215 | 7251 | __future__, typing | governance, memory, mpcp |
| `modules/W3Agent/tools/test_approval_gate.py` | `.py` | 111 | 2928 | importlib, pathlib | mpcp |
| `modules/W3Agent/tools/test_auto_responder.py` | `.py` | 103 | 2882 | importlib, pathlib, sys, types | mpcp |
| `modules/W3Agent/tools/test_execution_worker.py` | `.py` | 125 | 3424 | importlib, pathlib, sys | - |
| `modules/index.json` | `.json` | 16 | 283 | - | - |
| `modules/module_agent_core_template.json` | `.json` | 77 | 1179 | - | governance, memory |
| `modules/registry.json` | `.json` | 192 | 4486 | - | governance, memory |
| `modules/requests/.gitkeep` | `-` | 0 | 0 | - | - |
| `modules/requests/@ChatGPT.md` | `.md` | 62 | 4837 | - | - |
| `modules/templates/README.md` | `.md` | 11 | 660 | - | - |
| `modules/templates/module_config_v0.1.json` | `.json` | 106 | 1607 | - | XXX |
| `narrative_reports/.gitkeep` | `-` | 0 | 0 | - | - |
| `notes/gstate/W3_ORGANIZATIONAL_CULTURE_LINK.md` | `.md` | 32 | 1712 | - | governance |
| `oc` | `-` | 5 | 153 | - | - |
| `opencode.json` | `.json` | 11 | 194 | - | - |
| `outcomes/README.md` | `.md` | 57 | 2421 | - | governance |
| `outcomes/append_only_ledger/.gitkeep` | `-` | 0 | 0 | - | - |
| `outcomes/artifacts/.gitkeep` | `-` | 4 | 222 | - | - |
| `outcomes/ledger/2026-02-25_outcomes-system-bootstrap.md` | `.md` | 62 | 1939 | - | - |
| `outcomes/ledger/_TEMPLATE__outcome-record.md` | `.md` | 67 | 1219 | - | - |
| `package.json` | `.json` | 5 | 52 | - | - |
| `portal.html` | `.html` | 113 | 3987 | - | governance |
| `protocol/EP_SIGNAL/CONTINUITY_MEMORY_MODEL.md` | `.md` | 168 | 2047 | - | memory |
| `protocol/EP_SIGNAL/EP_MANAUL.md` | `.md` | 131 | 7375 | - | mpcp |
| `protocol/EP_SIGNAL/INTERPRETATION_BOUNDARY_PAPER.md` | `.md` | 134 | 2139 | - | governance, mpcp |
| `protocol/EP_SIGNAL/README.md` | `.md` | 161 | 2995 | - | - |
| `protocol/EP_SIGNAL/README_integration.md` | `.md` | 41 | 1412 | - | mpcp |
| `protocol/EP_SIGNAL/RYTM_SIGNAL.md` | `.md` | 288 | 3622 | - | memory, mpcp |
| `protocol/EP_SIGNAL/SIGNAL_IDENTITY_LAW.md` | `.md` | 154 | 2168 | - | - |
| `protocol/EP_SIGNAL/SPEC_v1.md` | `.md` | 203 | 3006 | - | - |
| `protocol/EP_SIGNAL/TEST_CASE01.md` | `.md` | 103 | 1551 | - | - |
| `protocol/EP_SIGNAL/TEST_CASES.md` | `.md` | 103 | 1521 | - | - |
| `protocol/EP_SIGNAL/TecnicalRytm.md` | `.md` | 496 | 6734 | - | XXX, governance, memory, mpcp |
| `protocol/EP_SIGNAL/TecnicalRytm02.md` | `.md` | 535 | 8056 | - | XXX, governance, memory, mpcp |
| `protocol/EP_SIGNAL/ep_signal_adapter.py` | `.py` | 44 | 1581 | __future__, protocol | mpcp |
| `protocol/EP_SIGNAL/reference_implementation.py` | `.py` | 227 | 5266 | re | - |
| `protocol/EP_SIGNAL/rytm.py` | `.py` | 197 | 6657 | __future__, dataclasses, protocol, typing | - |
| `protocol/EP_SIGNAL/summary_cord01.md` | `.md` | 45 | 5310 | - | memory, mpcp |
| `protocol/EP_SIGNAL/test_ep_signal_integration.py` | `.py` | 96 | 3431 | protocol, random, unittest | mpcp |
| `protocol/Files.void/File_void.md` | `.md` | 99 | 9362 | - | - |
| `protocol/Files.void/README.md` | `.md` | 69 | 2892 | - | mpcp |
| `protocol/Files.void/void.runtime.spec.md` | `.md` | 95 | 7422 | - | - |
| `protocol/README.md` | `.md` | 60 | 4538 | - | mpcp |
| `protocol/ecs/README.md` | `.md` | 35 | 1518 | - | mpcp |
| `protocol/ecs/chain_pointer_operator.py` | `.py` | 21 | 809 | typing | - |
| `protocol/ecs/cooperative_contract.py` | `.py` | 41 | 1467 | dataclasses, datetime, typing, uuid | - |
| `protocol/ecs/event_chain_integration.py` | `.py` | 40 | 1448 | protocol | mpcp |
| `protocol/ecs/event_chain_system.py` | `.py` | 119 | 3679 | enum, typing | - |
| `protocol/ecs/event_registry.py` | `.py` | 69 | 2308 | datetime, typing, uuid | replay |
| `protocol/ecs/event_template.py` | `.py` | 37 | 1296 | dataclasses, datetime, typing, uuid | - |
| `protocol/ecs/versioned_registry.py` | `.py` | 37 | 1286 | datetime, typing, uuid | rollback |
| `protocol/files_void/README.md` | `.md` | 49 | 1215 | - | mpcp |
| `protocol/files_void/__init__.py` | `.py` | 24 | 593 | protocol | mpcp |
| `protocol/files_void/core.py` | `.py` | 183 | 6623 | __future__, dataclasses, hashlib, typing, uuid | mpcp |
| `protocol/files_void/tool.py` | `.py` | 79 | 2936 | __future__, protocol, typing | mpcp |
| `protocol/mpcp/COLOR_STATE.md` | `.md` | 182 | 3921 | - | mpcp |
| `protocol/mpcp/COLOR_SYMBOL_PAPER.md` | `.md` | 234 | 2229 | - | mpcp |
| `protocol/mpcp/CO_MODULE_LAW.md` | `.md` | 313 | 5614 | - | mpcp |
| `protocol/mpcp/CROSS_W3LGU_CONDIEN_RELATION.md` | `.md` | 146 | 3619 | - | governance, memory, mpcp |
| `protocol/mpcp/EVENT_TEMPLATE_CONDIEN_BRIDGE.md` | `.md` | 129 | 2577 | - | mpcp |
| `protocol/mpcp/MODEW_DYNAMIC_CAPABILITY_PAPER/MODEW_DYNAMIC_CAPABILITY_PAPER.md` | `.md` | 208 | 4844 | - | mpcp |
| `protocol/mpcp/MODEW_PAPER.md` | `.md` | 194 | 2113 | - | mpcp |
| `protocol/mpcp/MPCP_ORIGIN.md` | `.md` | 171 | 8331 | - | memory, mpcp |
| `protocol/mpcp/README.md` | `.md` | 208 | 3533 | - | memory, mpcp |
| `protocol/mpcp/ROT_BASELINE.md` | `.md` | 427 | 8852 | - | governance, mpcp, rollback |
| `protocol/mpcp/ROT_PAPER.md` | `.md` | 348 | 5366 | - | mpcp |
| `protocol/mpcp/THEORDERMPCP.md` | `.md` | 350 | 14383 | - | governance, memory, mpcp, rollback |
| `protocol/mpcp/W3_DISTRIBUTED_FAMILY_ARCHITECTURE.md` | `.md` | 187 | 3573 | - | memory, mpcp |
| `protocol/mpcp/W3_TERMS_MASTER_PAPER_v2.md` | `.md` | 891 | 17974 | - | governance, memory, mpcp, rollback |
| `protocol/mpcp/__init__.py` | `.py` | 26 | 579 | config, env, lib | mpcp |
| `protocol/mpcp/adapter/__init__.py` | `.py` | 9 | 193 | w3_bridge, w3db | mpcp |
| `protocol/mpcp/adapter/file_void_tool.py` | `.py` | 51 | 2239 | __future__, collections, files_void, protocol, typing | mpcp |
| `protocol/mpcp/adapter/w3_bridge.py` | `.py` | 31 | 999 | __future__, collections, typing | mpcp |
| `protocol/mpcp/adapter/w3db.py` | `.py` | 38 | 1126 | __future__, collections, src, typing | mpcp |
| `protocol/mpcp/case_studies/AGENT_MPCP_ALIGNMENT_TESTS_V1.md` | `.md` | 427 | 17387 | - | governance, memory, mpcp |
| `protocol/mpcp/case_studies/README.md` | `.md` | 32 | 2439 | - | mpcp |
| `protocol/mpcp/config/__init__.py` | `.py` | 5 | 135 | loader | mpcp |
| `protocol/mpcp/config/default.json` | `.json` | 45 | 1505 | - | memory, mpcp |
| `protocol/mpcp/config/loader.py` | `.py` | 75 | 2780 | __future__, dataclasses, functools, json, pathlib, typing | mpcp |
| `protocol/mpcp/cooperative_contract.py` | `.py` | 166 | 6266 | __future__, dataclasses, datetime, typing, uuid | mpcp |
| `protocol/mpcp/env/README.md` | `.md` | 61 | 2508 | - | mpcp |
| `protocol/mpcp/env/__init__.py` | `.py` | 15 | 433 | boundary, gateway, models, probe | mpcp |
| `protocol/mpcp/env/boundary.py` | `.py` | 221 | 9741 | __future__, adapter, collections, config, kernel, lib, models, probe, typing | mpcp |
| `protocol/mpcp/env/gateway.py` | `.py` | 45 | 1581 | __future__, boundary, collections, models, runtime, typing | mpcp |
| `protocol/mpcp/env/models.py` | `.py` | 152 | 4904 | __future__, dataclasses, types, typing | mpcp |
| `protocol/mpcp/env/probe.py` | `.py` | 76 | 2357 | __future__, config, models, os, platform, shutil, sys, typing | mpcp |
| `protocol/mpcp/kernel/__init__.py` | `.py` | 0 | 0 | - | - |
| `protocol/mpcp/kernel/co_module.py` | `.py` | 209 | 7396 | __future__, typing | mpcp |
| `protocol/mpcp/kernel/contract.py` | `.py` | 231 | 8336 | system | mpcp |
| `protocol/mpcp/kernel/event_template.py` | `.py` | 176 | 6572 | __future__, dataclasses, datetime, typing, uuid | mpcp |
| `protocol/mpcp/kernel/module_bridge.py` | `.py` | 104 | 3810 | __future__, dataclasses, datetime, protocol, typing, uuid | mpcp |
| `protocol/mpcp/kernel/module_registry.py` | `.py` | 60 | 2164 | __future__, dataclasses, typing | mpcp |
| `protocol/mpcp/kernel/module_validator.py` | `.py` | 72 | 3208 | __future__, protocol, typing | mpcp |
| `protocol/mpcp/kernel/rot.py` | `.py` | 440 | 17032 | __future__, typing | governance, mpcp |
| `protocol/mpcp/kernel/system.py` | `.py` | 36 | 904 | - | mpcp |
| `protocol/mpcp/kernel/validator.py` | `.py` | 43 | 1054 | contract, rot, system | mpcp |
| `protocol/mpcp/lib/__init__.py` | `.py` | 6 | 176 | pillar, registry | mpcp |
| `protocol/mpcp/lib/pillar.py` | `.py` | 151 | 6485 | __future__, collections, typing | mpcp |
| `protocol/mpcp/lib/registry.py` | `.py` | 76 | 2873 | __future__, config, dataclasses, shutil, typing | mpcp |
| `protocol/mpcp/modew/__init__.py` | `.py` | 5 | 82 | base_modew | mpcp |
| `protocol/mpcp/modew/base_modew.py` | `.py` | 215 | 6830 | kernel | memory, mpcp |
| `protocol/mpcp/mpcp_blueprint_paper/README.md` | `.md` | 378 | 3932 | - | governance, memory, mpcp |
| `protocol/mpcp/mpcp_blueprint_paper/mpcp_blueprint_paper.md` | `.md` | 220 | 4037 | - | mpcp |
| `protocol/mpcp/mpcp_concept_paper/ROT_PAPER.md` | `.md` | 311 | 4262 | - | mpcp |
| `protocol/mpcp/mpcp_concept_paper/mpcp_concept_paper.md` | `.md` | 217 | 5954 | - | mpcp |
| `protocol/mpcp/mpcp_lib_paper/mpcp_lib_paper.md` | `.md` | 212 | 3687 | - | memory, mpcp |
| `protocol/mpcp/mpcp_pillar.md` | `.md` | 171 | 3790 | - | memory, mpcp |
| `protocol/mpcp/mpcp_unified_lgu/mpcp_unified_language_paper.md` | `.md` | 184 | 4212 | - | mpcp |
| `protocol/mpcp/orchestrator/__init__.py` | `.py` | 6 | 143 | flow, manager | mpcp |
| `protocol/mpcp/orchestrator/flow.py` | `.py` | 9 | 264 | manager | mpcp |
| `protocol/mpcp/orchestrator/manager.py` | `.py` | 112 | 3323 | kernel, runtime | mpcp |
| `protocol/mpcp/runtime/__init__.py` | `.py` | 9 | 319 | executor, trace | mpcp |
| `protocol/mpcp/runtime/entry.py` | `.py` | 16 | 401 | executor | mpcp |
| `protocol/mpcp/runtime/executor.py` | `.py` | 168 | 5155 | kernel, trace | mpcp |
| `protocol/mpcp/runtime/trace.py` | `.py` | 61 | 1765 | datetime | mpcp |
| `protocol/mpcp/runtime_sanity_sweep.py` | `.py` | 330 | 11180 | mpcp, os, sys | memory, mpcp |
| `protocol/mpcp/schema/__init__.py` | `.py` | 0 | 0 | - | - |
| `protocol/mpcp/schema/pillar.json` | `.json` | 20 | 440 | - | mpcp |
| `protocol/mpcp/schema/pillar.schema.json` | `.json` | 30 | 867 | - | - |
| `protocol/mpcp/test_agent_mpcp_alignment.py` | `.py` | 364 | 12019 | core, os, sys | governance, mpcp |
| `protocol/mpcp/test_condien_blueprint.py` | `.py` | 362 | 12559 | os, src, sys | mpcp |
| `protocol/mpcp/w3lgu_integration_paper/W3LGU_CONDIEN_PROFILE.md` | `.md` | 162 | 4838 | - | governance, mpcp |
| `protocol/mpcp/w3lgu_integration_paper/W3LGU_MPCP_BLUEPRINT_PROFILE.md` | `.md` | 115 | 3107 | - | mpcp |
| `protocol/mpcp/w3lgu_integration_paper/W3LGU_MPCP_ROLE_MAPPING.md` | `.md` | 232 | 10341 | - | governance, mpcp |
| `protocol/mpcp/w3lgu_integration_paper/W3LGU_MPCP_RUNTIME_PROFILE.md` | `.md` | 123 | 3081 | - | governance, mpcp |
| `protocol/mpcp/w3lgu_integration_paper/W3LGU_PROFILE_ARCHITECTURE.md` | `.md` | 186 | 7064 | - | governance, mpcp |
| `protocol/w3db/W3DB_MANAUL.md` | `.md` | 142 | 5317 | - | memory, mpcp |
| `protocol/w3db/__init__.py` | `.py` | 1 | 21 | - | - |
| `protocol/w3db/test_crud.py` | `.py` | 228 | 8053 | os, src, sys | mpcp |
| `protocol/w3db/test_flow.py` | `.py` | 263 | 8518 | os, src, sys | - |
| `protocol/w3lgu/6room_event_logic_plan.md` | `.md` | 446 | 8310 | - | governance, memory, mpcp |
| `protocol/w3lgu/ECS_event_chain_system_plan.md` | `.md` | 360 | 6445 | - | governance, mpcp |
| `protocol/w3lgu/README.md` | `.md` | 490 | 34957 | - | memory, mpcp |
| `protocol/w3lgu/RML01.md` | `.md` | 79 | 2211 | - | memory, replay |
| `protocol/w3lgu/__init__.py` | `.py` | 72 | 2014 | protocol | mpcp |
| `protocol/w3lgu/adapters.py` | `.py` | 49 | 1601 | __future__, protocol, typing | mpcp |
| `protocol/w3lgu/adapters/README.md` | `.md` | 17 | 434 | - | mpcp |
| `protocol/w3lgu/bin/.keep` | `-` | 1 | 1 | - | - |
| `protocol/w3lgu/bin/Engine` | `-` | 15 | 644 | - | mpcp |
| `protocol/w3lgu/bin/Hello.java` | `.java` | 5 | 125 | - | - |
| `protocol/w3lgu/bin/dt_ml.py` | `.py` | 13 | 412 | datetime | memory |
| `protocol/w3lgu/bin/engine.py` | `.py` | 30 | 1725 | - | memory |
| `protocol/w3lgu/bin/runtime.py` | `.py` | 68 | 1573 | __future__, pathlib, typing | memory |
| `protocol/w3lgu/core.py` | `.py` | 154 | 4846 | __future__, dataclasses, typing | memory, replay |
| `protocol/w3lgu/docs/MANIFEST.md` | `.md` | 11 | 274 | - | memory, mpcp |
| `protocol/w3lgu/docs/PRODUCTION_TEMPLATE.md` | `.md` | 117 | 4266 | - | replay |
| `protocol/w3lgu/docs/W3Lgu_Operational_Manual.md` | `.md` | 67 | 1733 | - | mpcp |
| `protocol/w3lgu/docs/W3Lgu_Operational_Manual_v2.md` | `.md` | 63 | 1090 | - | mpcp |
| `protocol/w3lgu/docs/ถ้ายังไม่มี` | `-` | 1 | 2 | - | - |
| `protocol/w3lgu/docs/ทั้งเพื่อเก็บเอกสาร,` | `-` | 1 | 2 | - | - |
| `protocol/w3lgu/docs/สำหรับผู้เริ่มต้นจนถึงขั้นใช้งานจริง.md` | `.md` | 1 | 2 | - | - |
| `protocol/w3lgu/encoding.py` | `.py` | 20 | 558 | __future__, urllib | - |
| `protocol/w3lgu/layers/README.md` | `.md` | 14 | 293 | - | memory |
| `protocol/w3lgu/memory/README.md` | `.md` | 12 | 313 | - | memory |
| `protocol/w3lgu/operational.py` | `.py` | 632 | 21717 | __future__, dataclasses, datetime, hashlib, json, protocol, re, threading, types, typing | governance |
| `protocol/w3lgu/papers/W3LGU_ADAPTER_PAPER.md` | `.md` | 42 | 1202 | - | mpcp |
| `protocol/w3lgu/papers/W3LGU_CONCEPT_PAPER.md` | `.md` | 65 | 2057 | - | memory, mpcp |
| `protocol/w3lgu/papers/W3LGU_EVENT_PAPER.md` | `.md` | 42 | 1202 | - | memory, replay |
| `protocol/w3lgu/papers/W3LGU_GRAMMAR_PAPER.md` | `.md` | 53 | 1469 | - | - |
| `protocol/w3lgu/papers/W3LGU_LAYER_PAPER.md` | `.md` | 34 | 1190 | - | memory |
| `protocol/w3lgu/papers/W3LGU_PARSER_PAPER.md` | `.md` | 67 | 1441 | - | - |
| `protocol/w3lgu/papers/W3LGU_RUNTIME_PAPER.md` | `.md` | 66 | 1688 | - | memory, mpcp |
| `protocol/w3lgu/papers/W3LGU_SIGNAL_PAPER.md` | `.md` | 43 | 1327 | - | - |
| `protocol/w3lgu/parser.py` | `.py` | 79 | 3104 | __future__, protocol, re | - |
| `protocol/w3lgu/parser/README.md` | `.md` | 24 | 514 | - | - |
| `protocol/w3lgu/px.py` | `.py` | 119 | 3678 | __future__, dataclasses, protocol, src, typing | memory |
| `protocol/w3lgu/runtime.py` | `.py` | 83 | 3079 | __future__, dataclasses, datetime, protocol, typing, uuid | memory |
| `protocol/w3lgu/runtime/README.md` | `.md` | 16 | 266 | - | - |
| `protocol/w3lgu/signals.py` | `.py` | 48 | 1837 | __future__, dataclasses, protocol | - |
| `protocol/w3lgu/signals/README.md` | `.md` | 13 | 218 | - | - |
| `protocol/w3lgu/sixroom_runtime.py` | `.py` | 446 | 16110 | __future__, dataclasses, typing | mpcp |
| `protocol/w3lgu/validator.py` | `.py` | 45 | 1659 | __future__, dataclasses, protocol | - |
| `repo-structure.html` | `.html` | 1327 | 132364 | - | TODO, governance, memory, mpcp, replay |
| `repo_events/.gitkeep` | `-` | 0 | 0 | - | - |
| `repo_list.md` | `.md` | 1016 | 35357 | - | TODO, governance, memory, mpcp, replay |
| `repo_report.html` | `.html` | 1574 | 59347 | - | TODO, governance, memory, mpcp |
| `repo_table.sh` | `.sh` | 35 | 1035 | - | - |
| `reports/cleanup_plan.md` | `.md` | 267 | 8746 | - | governance, mpcp |
| `reports/content_map.json` | `.json` | 311 | 10226 | - | governance, memory, mpcp |
| `reports/full_structure_audit.md` | `.md` | 226 | 8459 | - | deprecated, governance, mpcp |
| `reports/logic_analysis` | `-` | 8 | 226 | - | - |
| `reports/module_health.md` | `.md` | 218 | 10505 | - | governance, mpcp |
| `reports/registry_audit.md` | `.md` | 163 | 6328 | - | governance, memory |
| `requests/.gitkeep` | `-` | 0 | 0 | - | - |
| `requests/REVIEW01.md` | `.md` | 499 | 22536 | - | governance, memory, rollback |
| `requests/RQ-AMS-MIGRATION-A001.md` | `.md` | 211 | 2599 | - | governance, mpcp |
| `requests/W3LGU_MINIMUM_MODULE_SPEC.md` | `.md` | 411 | 15214 | - | governance, memory |
| `requests/intent` | `-` | 7 | 183 | - | - |
| `requests/requests_a001` | `-` | 11 | 662 | - | - |
| `requests/results/RQ-a001_STATUS.md` | `.md` | 433 | 17996 | - | governance, mpcp |
| `requirements-dev.txt` | `.txt` | 4 | 69 | - | - |
| `requirements.txt` | `.txt` | 16 | 437 | - | - |
| `results/.gitkeep` | `-` | 0 | 0 | - | - |
| `results/structural_blueprints` | `-` | 8 | 236 | - | - |
| `resume_header.json` | `.json` | 9 | 250 | - | - |
| `resume_header.schema.json` | `.json` | 17 | 558 | - | - |
| `scripts/enforce_layer_separation.py` | `.py` | 209 | 7182 | __future__, argparse, dataclasses, json, pathlib, src, sys, typing | governance, memory |
| `src/core/.gitkeep` | `-` | 0 | 0 | - | - |
| `src/core/__init__.py` | `.py` | 12 | 426 | src | mpcp |
| `src/core/blueprint.py` | `.py` | 382 | 14318 | __future__, typing | governance, mpcp |
| `src/core/condien.py` | `.py` | 422 | 15584 | __future__, dataclasses, typing | governance, mpcp |
| `src/logs/.gitkeep` | `-` | 0 | 0 | - | - |
| `src/main.py` | `.py` | 260 | 7291 | core, datetime, json, os, signal, sys, time, traceback, typing, uuid | - |
| `src/modules/.gitkeep` | `-` | 0 | 0 | - | - |
| `src/modules/registry.json` | `.json` | 18 | 316 | - | - |
| `src/modules/registry.schema.json` | `.json` | 54 | 898 | - | - |
| `src/modules/registry/registry.json` | `.json` | 81 | 1863 | - | governance, memory |
| `src/utils/.gitkeep` | `-` | 0 | 0 | - | - |
| `src/w3db/__init__.py` | `.py` | 18 | 644 | src | memory |
| `src/w3db/append_flow.py` | `.py` | 219 | 6624 | __future__, dataclasses, datetime, hashlib, json, src, typing | replay |
| `src/w3db/config.py` | `.py` | 85 | 2419 | dataclasses, os, typing | memory |
| `src/w3db/crud/__init__.py` | `.py` | 13 | 653 | src | - |
| `src/w3db/crud/fbd.py` | `.py` | 64 | 1609 | __future__, src, typing | - |
| `src/w3db/crud/prx.py` | `.py` | 72 | 1786 | __future__, src, typing | - |
| `src/w3db/crud/tuf.py` | `.py` | 62 | 1524 | __future__, src, typing | - |
| `src/w3db/crud/whb.py` | `.py` | 56 | 1354 | __future__, src, typing | - |
| `src/w3db/crud/xiz.py` | `.py` | 62 | 1546 | __future__, src, typing | - |
| `src/w3db/flow.py` | `.py` | 236 | 7551 | __future__, datetime, src, typing, uuid | - |
| `src/w3db/models.py` | `.py` | 262 | 7973 | dataclasses, typing | - |
| `src/w3db/store.py` | `.py` | 231 | 7874 | __future__, src, typing | memory |
| `system_observations/.gitkeep` | `-` | 0 | 0 | - | - |
| `tests/test_agent_self_workspace_standard.py` | `.py` | 46 | 1636 | pathlib | - |
| `tests/test_bbex_intent.py` | `.py` | 102 | 4361 | core, pathlib, tempfile, unittest | memory |
| `tests/test_bbx19_action.py` | `.py` | 127 | 5781 | core, unittest | - |
| `tests/test_box_integration.py` | `.py` | 50 | 1548 | __future__, fastapi, w3_api, wx | - |
| `tests/test_branch_public_docs.py` | `.py` | 32 | 925 | pathlib | governance |
| `tests/test_chatgpt_flow_artifact.py` | `.py` | 178 | 7057 | core, hashlib, os, pathlib, tempfile, unittest | memory |
| `tests/test_codex_agent.py` | `.py` | 77 | 3055 | codex, dataclasses, importlib, json, pathlib, pytest | governance |
| `tests/test_cross_x_config.py` | `.py` | 99 | 4211 | config, cross_x, dataclasses, pytest | governance |
| `tests/test_ep_signal_rytm.py` | `.py` | 52 | 1879 | dataclasses, protocol, pytest | - |
| `tests/test_event_chain.py` | `.py` | 129 | 3750 | __future__, cross_x, pytest | mpcp |
| `tests/test_file_void_tool.py` | `.py` | 82 | 2894 | protocol, pytest | mpcp |
| `tests/test_g_state_foundation.py` | `.py` | 91 | 2943 | pathlib | governance |
| `tests/test_hospitication_cli.py` | `.py` | 57 | 1421 | __future__, json, subprocess, sys | governance, memory, replay |
| `tests/test_hospitication_core.py` | `.py` | 90 | 3302 | __future__, dataclasses, hospitication, pytest | governance, memory, mpcp, replay |
| `tests/test_hospitication_runner.py` | `.py` | 33 | 828 | __future__, pathlib, subprocess, sys | - |
| `tests/test_origin_agent_runtime_contracts.py` | `.py` | 206 | 8186 | core, json, os, tempfile, unittest | governance, mpcp |
| `tests/test_process_layer.py` | `.py` | 80 | 3193 | core, dataclasses, pytest, src | memory |
| `tests/test_psp2_agent_dispatch.py` | `.py` | 18 | 667 | core | - |
| `tests/test_px_w3db_append_flow.py` | `.py` | 95 | 3159 | dataclasses, protocol, pytest, src, w3_api | replay |
| `tests/test_runtime_agent_execution.py` | `.py` | 52 | 2290 | core, json, pathlib, tempfile, unittest | - |
| `tests/test_semantic_router.py` | `.py` | 136 | 4474 | core, datetime, src, typing, uuid | governance, mpcp |
| `tests/test_w3_api_cross.py` | `.py` | 110 | 3679 | __future__, fastapi, protocol, src, w3_api | memory, mpcp |
| `tests/test_w3_api_cross_plan.py` | `.py` | 77 | 2555 | __future__, fastapi, w3_api | - |
| `tests/test_w3_api_gateway.py` | `.py` | 59 | 1521 | __future__, fastapi, importlib, w3_api | - |
| `tests/test_w3_api_mfc_integration.py` | `.py` | 44 | 1541 | core, unittest, w3_api | memory |
| `tests/test_w3_integration_grade.py` | `.py` | 107 | 4045 | __future__, core, hospitication, integrations, json, protocol, scripts, src, subprocess, sys | governance, memory, replay |
| `tests/test_w3api_tools.py` | `.py` | 111 | 3052 | __future__, argparse, importlib, json, pathlib, subprocess, sys | - |
| `tests/test_w3lgu_core.py` | `.py` | 124 | 3480 | __future__, dataclasses, protocol, pytest | memory, mpcp |
| `tests/test_w3lgu_event_field_logic27.py` | `.py` | 89 | 3556 | core, unittest | - |
| `tests/test_w3lgu_mfc_logic.py` | `.py` | 201 | 9514 | core, unittest | memory |
| `tests/test_w3lgu_operational.py` | `.py` | 159 | 5017 | __future__, dataclasses, protocol, pytest | replay |
| `tests/test_w3unive_handbook.py` | `.py` | 75 | 2223 | pathlib | governance |
| `tools/README.md` | `.md` | 251 | 6634 | - | governance |
| `tools/bbex_core_anchor.py` | `.py` | 75 | 2538 | __future__, argparse, core, json, pathlib, sys | - |
| `tools/check_portable_paths.py` | `.py` | 84 | 2684 | __future__, pathlib, subprocess, sys | - |
| `tools/dtml_security_scanner.py` | `.py` | 351 | 13865 | datetime, json, os, pathlib, re, subprocess | XXX |
| `tools/file_integrity_check.py` | `.py` | 215 | 8546 | datetime, json, os, pathlib, sys | - |
| `tools/file_integrity_report.txt` | `.txt` | 20 | 790 | - | - |
| `tools/lrc2_recorder.py` | `.py` | 390 | 15006 | datetime, json, pathlib | memory |
| `tools/memory_manager.py` | `.py` | 195 | 5604 | argparse, datetime, json, pathlib, sys, typing | memory |
| `tools/psp2_pr_router.py` | `.py` | 317 | 12520 | datetime, json, pathlib | governance |
| `tools/redr_structure_reader.py` | `.py` | 421 | 15703 | collections, datetime, json, os, pathlib | deprecated |
| `tools/run_audit.py` | `.py` | 171 | 5261 | datetime, pathlib, subprocess, sys | - |
| `tools/run_hospitication.py` | `.py` | 77 | 2686 | __future__, argparse, hospitication, pathlib, sys | - |
| `tools/send_integrity_report.py` | `.py` | 245 | 10184 | datetime, email, file_integrity_check, json, os, pathlib, smtplib, sys | - |
| `tools/smoke_test.py` | `.py` | 107 | 3427 | os, src, sys, time, traceback | - |
| `tools/test_check_portable_paths.py` | `.py` | 29 | 1129 | tools, unittest | - |
| `tools/validate_json_schemas.py` | `.py` | 142 | 4982 | json, jsonschema, os, pathlib, sys, typing | - |
| `tools/validate_metadata.py` | `.py` | 155 | 4197 | pathlib, re, sys, typing | governance |
| `tools/validate_modules.py` | `.py` | 153 | 5618 | json, os, pathlib, re, sys, typing | - |
| `tools/validate_runtime_log.py` | `.py` | 134 | 3500 | json, pathlib, sys, typing | - |
| `tools/w3_agent_ci.py` | `.py` | 370 | 13133 | core, datetime, json, jsonschema, os, pathlib, subprocess, sys, yaml | governance, memory |
| `tools/w3_toolbox.py` | `.py` | 118 | 4414 | csv, datetime, json, pathlib, sys | - |
| `tools/w3api.py` | `.py` | 226 | 7425 | __future__, argparse, json, pathlib, sys, typing, urllib | memory |
| `tools/w3run.py` | `.py` | 153 | 4737 | argparse, core, json, pathlib, sys | governance |
| `tuf_snapshots/.gitkeep` | `-` | 0 | 0 | - | - |
| `versions/v0.1/CHANGELOG.md` | `.md` | 41 | 2159 | - | governance |
| `versions/v0.1/README.md` | `.md` | 127 | 4650 | - | governance |
| `versions/v0.1/modules/BBX19.json` | `.json` | 16 | 437 | - | governance |
| `versions/v0.1/modules/ChatGPT.json` | `.json` | 17 | 501 | - | - |
| `versions/v0.1/modules/Copilot-GM.json` | `.json` | 17 | 495 | - | governance |
| `versions/v0.1/modules/DeepSeek.json` | `.json` | 17 | 507 | - | - |
| `versions/v0.1/modules/Gemini.json` | `.json` | 17 | 483 | - | - |
| `versions/v0.1/modules/Grok.json` | `.json` | 17 | 497 | - | - |
| `versions/v0.1/placeholder.md` | `.md` | 1 | 1 | - | - |
| `w3` | `-` | 129 | 3349 | - | - |
| `w3_api/README.md` | `.md` | 67 | 1366 | - | mpcp |
| `w3_api/__init__.py` | `.py` | 15 | 396 | w3_api | - |
| `w3_api/adapters/__init__.py` | `.py` | 1 | 46 | - | - |
| `w3_api/adapters/ep_signal_adapter.py` | `.py` | 25 | 822 | __future__, protocol | - |
| `w3_api/adapters/w3db_adapter.py` | `.py` | 28 | 1018 | __future__, protocol, typing | memory |
| `w3_api/adapters/w3lgu_adapter.py` | `.py` | 40 | 1292 | __future__, protocol, typing | mpcp |
| `w3_api/main.py` | `.py` | 49 | 1070 | __future__, fastapi, w3_api | - |
| `w3_api/models.py` | `.py` | 54 | 1298 | __future__, pydantic, typing | - |
| `w3_api/router.py` | `.py` | 86 | 2726 | __future__, core, croll, datetime, fastapi, uuid, w3_api | - |
| `w3_tool_store/compiled/BOOTSTRAP_REFERENCE.md` | `.md` | 29 | 621 | - | - |
| `w3_tool_store/hybrid_syncap/HYBRID_CROSS_SYSTEM_NOTES.md` | `.md` | 539 | 12284 | - | memory, mpcp |
| `w3_tool_store/modew_pack_template/README.md` | `.md` | 114 | 2078 | - | mpcp |
| `w3_tool_store/modew_pack_template/W3_PLUGIN_MODEW_PACK.w3md` | `.w3md` | 115 | 1827 | - | mpcp |
| `w3_tool_store/modew_pack_template/agents/README.md` | `.md` | 17 | 278 | - | - |
| `w3_tool_store/modew_pack_template/assets/README.md` | `.md` | 8 | 193 | - | - |
| `w3_tool_store/modew_pack_template/boundary/boundary.json` | `.json` | 27 | 574 | - | - |
| `w3_tool_store/modew_pack_template/commands/README.md` | `.md` | 17 | 317 | - | - |
| `w3_tool_store/modew_pack_template/hooks/hooks.json` | `.json` | 21 | 525 | - | - |
| `w3_tool_store/modew_pack_template/mcp.json` | `.json` | 18 | 474 | - | - |
| `w3_tool_store/modew_pack_template/mpcp.json` | `.json` | 17 | 524 | - | mpcp |
| `w3_tool_store/modew_pack_template/pack.json` | `.json` | 25 | 748 | - | mpcp |
| `w3_tool_store/modew_pack_template/return_contract/return_contract.json` | `.json` | 31 | 591 | - | - |
| `w3_tool_store/modew_pack_template/skills/README.md` | `.md` | 17 | 290 | - | - |
| `w3_tool_store/notes/AI_SELF_REFERENCE.md` | `.md` | 10 | 276 | - | - |
| `w3_tool_store/notes/USER_COPY.md` | `.md` | 8 | 169 | - | - |
| `w3_tool_store/notes/mpcp_mcp.md` | `.md` | 8 | 166 | - | mpcp |
| `w3_tool_store/sheets/tool_map.csv` | `.csv` | 5 | 164 | - | - |
| `workflows/orchestration/.gitkeep` | `-` | 0 | 0 | - | - |
| `wx/README.md` | `.md` | 40 | 1500 | - | mpcp |
| `wx/__init__.py` | `.py` | 29 | 675 | engine_index, indexor, portdc | - |
| `wx/blueprints/README.md` | `.md` | 4 | 168 | - | - |
| `wx/blueprints/collection/paper_collection.md` | `.md` | 14 | 398 | - | - |
| `wx/blueprints/system/box_knowledge_infrastructure.md` | `.md` | 28 | 915 | - | governance, memory, mpcp |
| `wx/blueprints/system/wx_box_cn_fold_integration.md` | `.md` | 142 | 3988 | - | mpcp |
| `wx/collections/README.md` | `.md` | 61 | 2125 | - | memory, mpcp |
| `wx/engine_index.py` | `.py` | 214 | 9107 | __future__, collections, json, pathlib, re, typing | deprecated, memory |
| `wx/index/README.md` | `.md` | 4 | 152 | - | - |
| `wx/index/by_agent_role.md` | `.md` | 5 | 178 | - | - |
| `wx/index/by_box.md` | `.md` | 48 | 1536 | - | - |
| `wx/index/by_px.md` | `.md` | 8 | 317 | - | - |
| `wx/index/by_work_type.md` | `.md` | 6 | 188 | - | - |
| `wx/indexor.py` | `.py` | 46 | 1304 | __future__, engine_index, pathlib, typing | - |
| `wx/log_info/README.md` | `.md` | 6 | 301 | - | - |
| `wx/log_info/creations.jsonl` | `.jsonl` | 1 | 220 | - | - |
| `wx/log_info/requests.jsonl` | `.jsonl` | 1 | 218 | - | - |
| `wx/portdc.py` | `.py` | 31 | 1097 | __future__, engine_index, pathlib, typing | - |
| `wx/references/README.md` | `.md` | 4 | 177 | - | - |
| `wx/references/cn_fold_to_wx_box_mapping.md` | `.md` | 97 | 3415 | - | mpcp |
| `wx/references/wx_box_cn_fold_recovery_anchor.md` | `.md` | 167 | 4737 | - | mpcp |
| `wx/registry/README.md` | `.md` | 9 | 479 | - | - |
| `wx/registry/agent_registry.json` | `.json` | 14 | 330 | - | - |
| `wx/registry/blueprint_registry.json` | `.json` | 19 | 467 | - | - |
| `wx/registry/collection_registry.json` | `.json` | 11 | 262 | - | - |
| `wx/registry/template_registry.json` | `.json` | 63 | 1820 | - | - |
| `wx/registry/template_registry.schema.json` | `.json` | 35 | 1552 | - | deprecated |
| `wx/templates/README.md` | `.md` | 5 | 249 | - | - |
| `wx/templates/box/README.md` | `.md` | 69 | 2805 | - | - |
| `wx/templates/box/USAGE_TH.md` | `.md` | 309 | 10017 | - | mpcp |
| `wx/templates/box/wx_box_minimum.md` | `.md` | 144 | 3335 | - | - |
| `wx/templates/cross_l/rock_patch_block.md` | `.md` | 26 | 483 | - | - |
| `wx/templates/modew/README.md` | `.md` | 4 | 181 | - | - |
| `wx/templates/paper/adaptive_rule.md` | `.md` | 35 | 540 | - | - |
| `wx/templates/paper/fast_patch.md` | `.md` | 36 | 619 | - | - |
| `wx/test_engine_index.py` | `.py` | 87 | 3640 | __future__, json, pathlib, tempfile, unittest, wx | - |

## ข้อจำกัดในการตีความ

- Drift ปัจจุบันใช้ threshold ของคะแนน ยังไม่ใช่ before/after baseline
- Oscillation ปัจจุบันไม่ได้อาศัย time series
- Dependency analysis อ่าน Python imports เป็นหลัก
- Node position ยังไม่ได้ map กับ ENV/node จริงทั้งหมดของ W3
- Recovery เป็น proposal เท่านั้น ไม่ใช่การอนุมัติหรือการลงมือแก้
- รายงานอาจมี internal path จึงควรถือเป็น BOX IN จนกว่าจะผ่านการคัดกรอง

## Final State

```yaml
status: completed
observation: true
diagnosis: false
auto_recovery: false
source_truth_mutated: false
human_review_required: true
box_surface: IN
```

_Hospitication observes structural pressure; it does not rewrite truth._
