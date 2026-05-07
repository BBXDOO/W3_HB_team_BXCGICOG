# W3DB_Memories

## Files_Database

### 1) CIX_IDENTITY
- สร้างเป็น **New Database → Table**

### 2) WGU_LOGIC
| Property | Type | Options / Notes |
|---|---|---|
| WGU_ID | Title | ใช้เป็นชื่อหลัก |
| Symbol | Select | ▲, ●, ■, ◆ |
| Line | Select | A, B, C, N |
| Meaning | Text |  |
| Default Action | Text |  |

> ใส่รายการเริ่มต้น 4 ตัวก่อน

### 3) TUF_STATE
| Property | Type | Options / Notes |
|---|---|---|
| TUF_ID | Title | ใช้เป็นชื่อหลัก |
| CIX | Relation | เชื่อมกับ CIX_IDENTITY |
| Initial | Select | 0 / 0.5 / 1 |
| Final | Select | 0 / 0.5 / 1 |
| Resolution | Text |  |
| Note | Text |  |

### 4) XIZ_LOGS
| Property | Type | Options / Notes |
|---|---|---|
| XIZ_ID | Title | ใช้เป็นชื่อหลัก |
| TUF | Relation | เชื่อมกับ TUF_DECISION |
| Action | Text |  |
| Timestamp | Date |  |
| Result | Text |  |
| Immutable | Checkbox | ติ๊กไว้เสมอ |

### 5) PRX_PERCEPTION
| Property | Type | Options / Notes |
|---|---|---|
| PRX_ID | Title | ใช้เป็นชื่อหลัก |
| TUF | Relation | เชื่อมกับ TUF_DECISION |
| Symbol | Select | ▲, ●, ■, ◆ |
| Color | Select | Red, Yellow, Green, Blue |
| Intensity | Formula | ใช้สูตรด้านล่าง |
| Source TUF | Relation |  |

### 6) FBD_BOUNDARY
| Property | Type | Options / Notes |
|---|---|---|
| FBD_ID | Title | ใช้เป็นชื่อหลัก |
| TUF | Relation | เชื่อมกับ TUF_DECISION |
| First Deviation | Text |  |
| Failure | Text | Red, Yellow, Green, Blue |
| Conditions | Text | ใช้สูตรด้านล่าง |
| Impact | Text |  |

### 7) WHB_LAW
| Property | Type | Options / Notes |
|---|---|---|
| LAW_ID | Title | ใช้เป็นชื่อหลัก |
| FBD | Relation | เชื่อมกับ FBD_BOUNDARY |
| Condition | Text | เชื่อมกับ TUF_DECISION |
| Action | Text |  |

---

## Formula สำหรับ State
> ใช้ค่า State แบบ Observation: `0 / 0.5 / 1`

## Formula สำหรับ Intensity
```text
abs(confidence - 0.5) * scale
```

> ถ้า workspace ยังใช้ relation formula แบบนี้ไม่ได้ ให้ทำ workaround โดยใช้ **Rollup** ดึงค่า Confidence มาก่อน แล้วค่อยคำนวณจากค่า Rollup

---

## IDENTITY & CORE
- **CIX**: Identity Root Binding
- **STATE**: 0 (Fail) / 0.5 (Uncertain) / 1 (True) **[OBSERVATION ONLY]**
- **RULE**: No Interrupt | No Mid-run Modification | No Action by State Trigger

---

## FILE SYSTEM / NOTION STRUCTURE
| File | Meaning |
|---|---|
| `.cix` | Identity Anchor |
| `.w3x` | Container Unit (Deployable) |
| `.wgu` | Logic Archetype |
| `.sws` | Memory Storage |
| `.xiz` | Execution Trace (Full Log) |
| `.tuf` | Decision State (Internal Observation) |
| `.whb` | Behavior Pattern |
| `.prx` | Perception Output (Visual Trigger) |
| `.fbd` | Failed Boundary Detection **[NEW]** |

---

## PERCEPTION MAPPING (COLOR & SYMBOL)
| Line | Value | Symbol | Color | Meaning |
|---|---:|---|---|---|
| LINE A | 1.0 | ▲ | RED | FORCE / SYSTEM |
| LINE B | 0.5 | ● | YELLOW | UNCERTAIN / HUMAN |
| LINE C | 0.0 | ■ | GREEN | STABLE / RESULT |
| NETWORK | EXT | ◆ | BLUE | EXTERNAL |

- **INTENSITY**: `|confidence - 0.5| * scale`

---

## EXECUTION FLOW (PROCESS-DRIVEN)
`INPUT (Event/Signal) -> .xiz -> PROCESS (Full Run - No Interrupt) -> OBSERVE (Initial -> Transition -> Final) -> .tuf -> DETECT (First Deviation -> Failure Point) -> .fbd -> PATCH (Generate Law IF -> THEN) -> .whb (Line 3) -> RENDER (Visual Signaling) -> .prx`

---

## FAILED BOUNDARY SPEC (.fbd)
```json
{
  "fbd_id": "string",
  "source_tuf": "string",
  "first_deviation": "string",
  "failure_point": "string",
  "conditions": "string",
  "impact": "string",
  "line3_patch": "string [IF -> THEN]"
}
```

---

## ACTION PHILOSOPHY
- Action must **NOT** be triggered by Pattern or Command.
- Action must answer: **"Why is this action taken based on observed reality?"**
- State 0/0.5/1 is for **LEARNING**, not for **DECIDING**.

---

## NOTION MCP CONFIG
- **DB_IDENTITY**: `[.cix, .wgu]`
- **DB_PROCESS**: `[.xiz, .tuf, .fbd]`
- **DB_PERCEPTION**: `[.prx]`
- **RELATION**: `XIZ -> TUF -> FBD -> WHB -> WGU`

เพิ่มเติม:

---

## AGENT-GRADE CLEAN SPEC

### CORE
- `CIX`: identity
- `STATE`: `{0, 0.5, 1}` (observation only)
- `RULE`: `no_interrupt | no_mid_run_modification | no_action_by_state`

### FILE_MAP
| Files | Meaning |
|---|---|
| `.cix` | identity |
| `.w3x` | container |
| `.wgu` | logic archetype |
| `.sws` | memory |
| `.xiz` | execution trace |
| `.tuf` | process state snapshot |
| `.fbd` | failed boundary |
| `.whb` | contextual law (line3) |
| `.prx` | perception (derived only) |

### FLOW
`INPUT -> XIZ -> PROCESS (full run) -> TUF -> FBD -> WHB -> PRX`

### STATE (OBSERVATION)
```json
{ "initial": "0|0.5|1", "transitions": [], "final": "0|0.5|1" }
```

### FBD
```json
{ "fbd_id": "string", "source_tuf": "string", "first_deviation": "string", "failure_point": "string", "conditions": "string", "impact": "string" }
```

### WHB (LINE3)
```json
{ "condition": "IF ...", "action": "THEN ..." }
```

### PRX (DERIVED)
```json
{ "symbol": "▲|●|■|◆", "color": "RED|YELLOW|GREEN|BLUE", "intensity": "abs(confidence-0.5)*scale" }
```

### OUTPUT
```json
{ "cix": "...", "xiz": "...", "tuf": {"...": "..."}, "fbd": {"...": "..."}, "whb": {"...": "..."}, "prx": {"...": "..."} }
```

### FINAL
- `state ≠ decision`
- `process must complete`
- `failure = boundary`
- `action must answer: why`

---

## เคสจริง 1 เคส

### CIX
- **CIX-001**
- Type: `case`

### TUF
- **TUF-001**
- CIX -> `CIX-001`
- Confidence -> `0.72`
- ผลลัพธ์ State ควรออกเป็น `0.5`

### PRX
- **PRX-001**
- TUF -> `TUF-001`
- Symbol -> `●`
- Color -> `Yellow`
- Action Required -> `Observe`

### XIZ
- **XIZ-001**
- TUF -> `TUF-001`
- Action -> `Checked patient`
- Result -> `Stable`
- Immutable -> `✓`

---

## Dashboard
สร้างหน้าใหม่ชื่อ **OPD Dashboard**

เพิ่ม view จากฐานข้อมูล **PRX_PERCEPTION**
- View type: `Gallery`
- Card preview: `None`
- Show properties:
  - Symbol
  - Color
  - Intensity
  - Action Required

### เป้าหมาย
เปิดหน้าแล้วควรเห็น **● สีเหลือง** และเข้าใจได้ทันทีว่าต้องเข้าไปดู

### เช็กลิสต์เปิดระบบ
- เห็น ● แล้วรู้ไหมว่าต้องไปดู
- ไม่ต้องอ่าน text เยอะใช่ไหม
- ตัดสินใจได้ใน 1–2 วินาทีไหม
- ถ้าใช่ แปลว่า W3 เริ่มทำงานแล้ว

---

## Troubleshooting ล่วงหน้า
ถ้า Intensity ใช้ relation formula ไม่ได้:
1. เพิ่ม property แบบ **Rollup** ใน `PRX_PERCEPTION`
2. ดึงค่า **Confidence** จาก relation `TUF`
3. สร้าง formula ใหม่จากค่า rollup แทน

ถ้างง relation:
- `CIX_IDENTITY` -> เชื่อมไป `TUF_DECISION`
- `TUF_DECISION` -> เชื่อมไป `XIZ_LOGS`
- `TUF_DECISION` -> เชื่อมไป `PRX_PERCEPTION`

---

## หมายเหตุ
เอกสารนี้จัดรูปแบบใหม่จากสเปกต้นฉบับ เพื่อให้อ่านง่าย ใช้งานได้ทันที และรองรับการนำไปสร้างฐานข้อมูลบน Notion ตามลำดับความสัมพันธ์ของระบบ W3
