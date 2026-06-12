# CROSS_L_TABLE_X_MATRIX

**Document Path:** `croll/CROSS_L_TABLE_X_MATRIX.md`  
**Status:** ACTIVE DRAFT / BLUEPRINT  
**System Relation:** W3 / W3Lgu / CROLL / Cross-L / CrossLgu / Table-X / PX / Rytm / Color / Symbol / Modew / Condien / MPCP / LRC2  
**Owner:** BBX19  
**Purpose:** ตาราง Matrix สำหรับให้ `Cross-L` อ้างอิงตำแหน่งงานด้วย `PX` แล้วสร้าง workset เบื้องต้นได้เร็ว ก่อนส่งให้ `Modew`

---

# 1. Core Statement

`Table-X` คือ matrix อ้างอิงของ Cross-L

หน้าที่หลักคือ:

```text
Rytm + Work Type
→ PX Reference
→ Tag Group
→ Lang Candidate
→ Modew Style
→ Boundary
→ Deny
→ Return Contract
```

พูดง่าย ๆ:

```text
Table-X = ตารางเลือกชุดงาน
PX = ตัวชี้ cell ในตาราง
Cross-L = อ่าน cell แล้วสร้าง workset
Modew = รับ workset ไปทำ
```

---

# 2. Scope Lock

เอกสารนี้ใช้สำหรับ:

```text
Layer ของ Cross-L เท่านั้น
```

ไม่ใช่กฎของทุกระบบใน W3

ไม่ใช่ parser ที่ต้องใช้ทันที

ไม่ใช่ authority สำหรับ execute โดยตรง

เป็น blueprint สำหรับให้ Cross-L ลดการลังเลก่อนแตกงานให้ Modew

---

# 3. Why Markdown First

เริ่มจาก Markdown ก่อน เพราะ:

```text
- อ่านง่ายบนมือถือ
- แก้ใน GitHub ง่าย
- ใช้เป็น blueprint ได้ทันที
- ยังไม่ต้องพึ่ง parser ซับซ้อน
- ค่อยแปลงเป็น JSON / W3Lgu native syntax ภายหลัง
```

---

# 4. PX Rule

รูปแบบ PX:

```text
PX:[row,col]
```

ตัวอย่าง:

```text
PX:[1,1] = ROCK / FAST_PATCH
PX:[2,1] = JAZZ / ADAPTIVE_RULE
PX:[3,1] = EDM / PULSE_LOOP
```

ความหมาย:

```text
row = Rytm row / work pattern row
col = work type column / variation column
```

ใน version แรกนี้ใช้ `col = 1` เป็น main/default work type ของแต่ละ Rytm ก่อน

---

# 5. Table-X Matrix v0.1

| PX | Rytm | Work Type | Color | Symbol | Tag Group | Lang Candidate | Modew Style | Boundary | Default Review | Deny | Return Contract |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [1,1] | ROCK | FAST_PATCH | RED | ▲ | FAST, LOW, SCRIPT, CONFIG | C++, Rust, C, Assembly, WASM, Bash, JSON | Fixer | temp_patch | on_complete | truth_mutation, direct_merge, repo_write_without_review | state, reason, trace, mutated, review, patch_candidate |
| [2,1] | JAZZ | ADAPTIVE_RULE | YELLOW | ◆ | SCRIPT, GEN, CONFIG, DOC | Lua, Python, JSON, YAML, Markdown | Adapter | observe | on_uncertain | truth_mutation, file_write, network, merge | state, reason, trace, mutated, review |
| [3,1] | EDM | PULSE_LOOP | BLUE | ● | SCRIPT, WEB, ENV, CONFIG, QUERY | Python, Bash, JavaScript, TypeScript, JSON, YAML, Go | Runner | observe_loop | on_error | truth_mutation, direct_merge, unlimited_loop, log_flood | state, reason, trace, mutated, review, pulse_count, limit, stop_condition |
| [4,1] | BALLAD | MEMORY_NOTE | GREEN | ■ | DOC, CONFIG, QUERY, GEN | Markdown, TXT, JSON, YAML, SQL, Python | Keeper | record_only | on_missing_context | truth_mutation, direct_merge, delete_docs | state, reason, trace, mutated, review, stored_path |
| [5,1] | R&B | HUMAN_REPORT | BLUE | ● | DOC, WEB, GEN, CONFIG | Markdown, TXT, HTML, CSS, JavaScript, Python, JSON | Translator | readable_output | on_risk | truth_mutation, repo_write, risk_hiding | state, reason, summary, risk, next_step, mutated, review |
| [6,1] | STRING | KNOWLEDGE_CHAIN | PURPLE | ◆ | DOC, QUERY, FORMAL, CONFIG, GEN | Markdown, YAML, JSON, SQL, SPARQL, Datalog, Lean, Python | Binder | knowledge_index | on_conflict | truth_mutation, delete_docs, direct_merge | state, reason, trace, mutated, review, relation_map |

---

# 6. Field Meaning

## 6.1 PX

```text
PX = Pointer Position
```

ใช้ชี้ตำแหน่ง cell ใน Table-X

ตัวอย่าง:

```text
PX:[1,1]
```

หมายถึง:

```text
แถว ROCK
คอลัมน์ FAST_PATCH/default
```

---

## 6.2 Rytm

Rytm คือจังหวะงาน

```text
ROCK   = งานแรง / เร็ว / patch / pressure
JAZZ   = งานยืดหยุ่น / logic ทดลอง
EDM    = งาน loop / pulse / runtime sync
BALLAD = งาน memory / continuity
R&B    = งานสื่อสารกับมนุษย์
STRING = งาน relation / knowledge chain
```

---

## 6.3 Work Type

Work Type คือประเภทงานที่ Cross-L จะใช้สร้าง workset

ตัวอย่าง:

```text
FAST_PATCH
ADAPTIVE_RULE
PULSE_LOOP
MEMORY_NOTE
HUMAN_REPORT
KNOWLEDGE_CHAIN
```

---

## 6.4 Color

Color บอกสถานะ / ความเสี่ยง / อุณหภูมิงาน

```text
RED     = เสี่ยง / เร่ง / แรง
YELLOW  = ยังไม่นิ่ง / ต้อง review
BLUE    = signal / flow / runtime
GREEN   = ผ่าน / พร้อมเก็บ
PURPLE  = semantic / relation / meaning
```

---

## 6.5 Symbol

Symbol บอกรูปทรงของงาน

```text
▲ = pressure / risk / urgent
◆ = decision / cross point / adaptive logic
● = loop / pulse / continuity
■ = structure / stable block
```

---

## 6.6 Tag Group

Tag Group คือกลุ่มภาษา / เครื่องมือที่ Cross-L ควรมองก่อน

ตัวอย่าง:

```text
FAST, LOW, SCRIPT, CONFIG
```

แปลว่า:

```text
งานนี้ควรมองเครื่องมือสายเร็ว / low-level / script / config ก่อน
```

---

## 6.7 Lang Candidate

Lang Candidate คือภาษาหรือรูปแบบที่ Modew/Cross-L อาจใช้สร้าง CrossCode หรือ work fragment

ยังไม่ใช่คำสั่งให้ใช้ทุกตัว

เป็นแค่ candidate list

---

## 6.8 Modew Style

Modew Style คือบทบาทของ Modew ในงานนั้น

```text
Fixer      = แก้เฉพาะจุด
Adapter    = ปรับ logic ตามบริบท
Runner     = รัน loop / pulse / sync
Keeper     = เก็บความต่อเนื่อง
Translator = แปลผลให้มนุษย์เข้าใจ
Binder     = เชื่อม relation / knowledge chain
```

---

## 6.9 Boundary

Boundary คือขอบเขตเริ่มต้นของงาน

```text
temp_patch
observe
observe_loop
record_only
readable_output
knowledge_index
```

Boundary สำคัญกว่า language

เพราะภาษาไม่ใช่ authority

---

## 6.10 Default Review

Default Review คือเงื่อนไขที่ควรส่งให้มนุษย์หรือ layer สูงกว่าตรวจ

ตัวอย่าง:

```text
on_complete
on_uncertain
on_error
on_missing_context
on_risk
on_conflict
```

---

## 6.11 Deny

Deny คือสิ่งที่ห้ามทำโดย default

เช่น:

```text
truth_mutation
direct_merge
repo_write_without_review
unlimited_loop
risk_hiding
```

---

## 6.12 Return Contract

Return Contract คือผลลัพธ์ขั้นต่ำที่ Modew ต้องคืน

เช่น:

```text
state
reason
trace
mutated
review
```

กฎสำคัญ:

```text
mutated:false by default
review:true on uncertainty
```

---

# 7. Table-X Usage Flow

```text
1. Paper เข้ามาที่ Cross-L
2. Cross-L อ่าน Rytm / Work Type / Color / Symbol
3. Cross-L หา PX ใน Table-X
4. Cross-L อ่าน cell นั้น
5. Cross-L สร้าง workset
6. Condien สร้าง scoped state ตาม READ/Boundary
7. Modew รับ workset
8. Modew ทำงานตาม boundary
9. Return Contract กลับ MPCP
10. LRC2 บันทึก trace
```

---

# 8. Workset Example from PX

## 8.1 PX:[1,1]

```text
PX:[1,1]
RYTM:ROCK
WORK_TYPE:FAST_PATCH
```

Cross-L สร้าง workset:

```json
{
  "px": "[1,1]",
  "rytm": "ROCK",
  "work_type": "FAST_PATCH",
  "color": "RED",
  "symbol": "▲",
  "tag_group": ["FAST", "LOW", "SCRIPT", "CONFIG"],
  "lang_candidate": ["C++", "Rust", "C", "Assembly", "WASM", "Bash", "JSON"],
  "modew_style": "Fixer",
  "boundary": "temp_patch",
  "default_review": "on_complete",
  "deny": ["truth_mutation", "direct_merge", "repo_write_without_review"],
  "return_contract": ["state", "reason", "trace", "mutated", "review", "patch_candidate"]
}
```

---

## 8.2 PX:[2,1]

```text
PX:[2,1]
RYTM:JAZZ
WORK_TYPE:ADAPTIVE_RULE
```

Cross-L สร้าง workset:

```json
{
  "px": "[2,1]",
  "rytm": "JAZZ",
  "work_type": "ADAPTIVE_RULE",
  "color": "YELLOW",
  "symbol": "◆",
  "tag_group": ["SCRIPT", "GEN", "CONFIG", "DOC"],
  "lang_candidate": ["Lua", "Python", "JSON", "YAML", "Markdown"],
  "modew_style": "Adapter",
  "boundary": "observe",
  "default_review": "on_uncertain",
  "deny": ["truth_mutation", "file_write", "network", "merge"],
  "return_contract": ["state", "reason", "trace", "mutated", "review"]
}
```

---

# 9. W3Lgu Native Draft

ยังไม่ใช่ parser final

ใช้เป็น draft syntax เพื่อเชื่อมกับ W3Lgu / PX system

```text
TABLE:CROSS_L_ROUTING

PX:1,1; ROW:ROCK; COL:FAST_PATCH.
CELL:TAG_GROUP=FAST,LOW,SCRIPT,CONFIG; LANG=C++,Rust,C,Assembly,WASM,Bash,JSON; MODEW=Fixer; BOUNDARY=temp_patch; REVIEW=on_complete.
DENY:truth_mutation,direct_merge,repo_write_without_review.
RETURN:state,reason,trace,mutated,review,patch_candidate.

PX:2,1; ROW:JAZZ; COL:ADAPTIVE_RULE.
CELL:TAG_GROUP=SCRIPT,GEN,CONFIG,DOC; LANG=Lua,Python,JSON,YAML,Markdown; MODEW=Adapter; BOUNDARY=observe; REVIEW=on_uncertain.
DENY:truth_mutation,file_write,network,merge.
RETURN:state,reason,trace,mutated,review.
```

---

# 10. Future JSON Schema Direction

ในอนาคต Table-X สามารถแปลงเป็น JSON ได้ เช่น:

```json
{
  "table": "CROSS_L_ROUTING",
  "version": "0.1",
  "scope": "CROSS_L_ONLY",
  "cells": [
    {
      "px": [1, 1],
      "rytm": "ROCK",
      "work_type": "FAST_PATCH",
      "color": "RED",
      "symbol": "▲",
      "tag_group": ["FAST", "LOW", "SCRIPT", "CONFIG"],
      "lang_candidate": ["C++", "Rust", "C", "Assembly", "WASM", "Bash", "JSON"],
      "modew_style": "Fixer",
      "boundary": "temp_patch",
      "default_review": "on_complete",
      "deny": ["truth_mutation", "direct_merge", "repo_write_without_review"],
      "return_contract": ["state", "reason", "trace", "mutated", "review", "patch_candidate"]
    }
  ]
}
```

---

# 11. Relation to Existing CROLL Files

ใช้คู่กับ:

```text
croll/README.md
croll/test.md
croll/CROSS_L_LANGUAGE_TAG_TABLE.md
croll/CROSS_L_RYTM_MODEW_ROUTING.md
croll/CROSS_L_RYTM_TEST_CASES.md
croll/CROSS_L_COLOR_SYMBOL_LOGIC.md
croll/CROSS_L_MODEW_PAPER_TEMPLATES.md
```

บทบาทของไฟล์นี้:

```text
CROSS_L_TABLE_X_MATRIX.md
= ตารางรวมเพื่อเลือก workset จาก PX
```

---

# 12. Safety Laws

## 12.1 PX is reference, not permission

```text
PX ใช้ชี้ตำแหน่งงาน
ไม่ได้ให้สิทธิ์ execute โดยตรง
```

ยังต้องดู:

```text
Boundary
Deny
Return Contract
Review
MPCP validation
```

---

## 12.2 Language is not authority

```text
ภาษาเป็นเครื่องมือ
ไม่ใช่อำนาจ
```

แม้ cell จะบอกว่าใช้ C++ หรือ Assembly ได้
ก็ยังต้องอยู่ใน boundary

---

## 12.3 Table-X should stay light

```text
Table-X ต้องเบา เร็ว ง่าย
```

อย่าใส่รายละเอียดจนกลายเป็นระบบใหญ่เกินไป

ถ้ารายละเอียดมาก ให้แยกไป Paper Template หรือ Test Case

---

# 13. Final Statement

Table-X มีไว้ให้ Cross-L เลือกงานเร็วขึ้น

```text
Paper gives intent.
Table-X gives position.
Cross-L builds the workset.
Condien prepares scoped state.
Modew executes bounded work.
MPCP receives the result.
LRC2 remembers the trace.
```

แบบไทย:

```text
Paper ให้เจตนา
Table-X ให้ตำแหน่ง
Cross-L จัดชุดงาน
Condien เตรียมสถานะเฉพาะ
Modew ลงมือในขอบเขต
MPCP รับคืนค่า
LRC2 จำร่องรอย
```

END
