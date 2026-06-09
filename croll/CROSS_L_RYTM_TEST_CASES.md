# Cross-L Rytm Test Cases

**Document Path:** `croll/CROSS_L_RYTM_TEST_CASES.md`  
**Status:** ACTIVE DRAFT  
**System Relation:** W3 / CROLL / Cross-L / CrossLgu / EP_SIGNAL / Rytm / Cross-X / Modew / MPCP  
**Owner:** BBX19  
**Purpose:** ตัวอย่าง testcase สำหรับดูภาพรวมว่า `Rytm` แต่ละแนว เช่น ROCK, JAZZ, EDM, BALLAD, R&B, STRING ควรถูกส่งต่อไปยัง `Modew` และ `Cross-L` อย่างไร

---

# 1. เป้าหมายของ Test Case

เอกสารนี้ไม่ได้ทดสอบว่า code รันได้จริงหรือยัง

แต่ทดสอบว่า:

```text
เมื่อมีงานหนึ่งก้อน
ระบบสามารถอ่านจังหวะงานเป็น Rytm
แล้วเลือกกลุ่มภาษา / Modew style / Cross-L boundary ได้ถูกทางหรือไม่
```

พูดง่าย ๆ:

```text
งานนี้เป็นจังหวะอะไร
Modew ควรทำงานแบบไหน
ควรเริ่มจากภาษา / tag กลุ่มไหน
และ Cross-L ต้องครอบ boundary อะไร
```

---

# 2. Test Flow มาตรฐาน

ทุก testcase ใช้ flow เดียวกัน:

```text
INPUT TASK
→ DETECT RYTM
→ CROSS-X ROUTE
→ MODEW SELECT STYLE
→ SELECT TAG FAMILY
→ SELECT LANGUAGE CANDIDATE
→ BUILD CROSS-L BLOCK
→ RETURN CONTRACT
→ EP_SIGNAL / RYTM PREVIEW
→ LRC2 LOG
```

---

# 3. Minimal Expected Output

ทุก testcase ควรคืนอย่างน้อย:

```json
{
  "state": "pass|review|block|fail",
  "reason": "short_reason",
  "rytm": "ROCK|JAZZ|EDM|BALLAD|R&B|STRING",
  "modew_style": "Fixer|Adapter|Runner|Keeper|Translator|Binder",
  "candidate_tags": [],
  "candidate_languages": [],
  "cross_l_boundary": "...",
  "mutated": false,
  "review": true
}
```

กฎสำคัญ:

```text
mutated ต้องเป็น false โดย default
ถ้าไม่มั่นใจ ให้ state = review
ถ้าเจอการขอแก้ truth โดยตรง ให้ state = block
```

---

# 4. Test Case 01 — ROCK / Fast Bug Patch

## 4.1 สถานการณ์

```text
มี bug ในส่วน native / engine
ระบบต้องการแก้เร็ว แต่ยังไม่ควรแตะ repo จริง
```

## 4.2 Input Task

```json
{
  "task_id": "TC-RYTM-ROCK-001",
  "source": "Cross-X",
  "target": "Modew",
  "problem": "native engine memory pressure",
  "env": "termux_mobile",
  "urgency": "high",
  "need": "fast patch candidate",
  "boundary": "temp_patch",
  "allow_mutation": false
}
```

## 4.3 Expected Rytm

```text
RYTM:ROCK
```

เหตุผล:

```text
- งานมีแรงกดสูง
- ต้องแก้เร็ว
- เกี่ยวกับ performance / native / bug patch
- ต้องใช้จังหวะแรงและชัด
```

## 4.4 Expected Modew Style

```text
MODEW_STYLE:Fixer
```

Modew ควรทำ:

```text
- สร้าง patch candidate ชั่วคราว
- ไม่แก้ truth
- ไม่ merge
- รายงาน state/reason/trace กลับมา
```

## 4.5 Candidate Tags

```text
FAST:*
LOW:*
SCRIPT:*
CONFIG:*
```

## 4.6 Candidate Languages

```text
C++
Rust
C
Assembly
WASM
Bash
JSON
```

## 4.7 Cross-L Block

```text
CROSS-L:NATIVE_PRESSURE_PATCH
POINT:MODEW_ERROR_FIX
RYTM:ROCK
LANG:cpp,asm,json
BOUNDARY:temp_patch
MODEW:FAST_PATCH
INPUT:ctx,error_trace
READ:ENV,trace,error_report
DENY:truth_mutation,direct_merge,repo_write_without_review
RETURN:state,reason,trace,mutated,review,patch_candidate
REVIEW:on_complete
```

## 4.8 Expected Result

```json
{
  "state": "review",
  "reason": "rock_patch_candidate_requires_human_review",
  "rytm": "ROCK",
  "modew_style": "Fixer",
  "candidate_tags": ["FAST:*", "LOW:*", "SCRIPT:*", "CONFIG:*"],
  "candidate_languages": ["C++", "Assembly", "JSON"],
  "cross_l_boundary": "temp_patch",
  "mutated": false,
  "review": true
}
```

## 4.9 Pass Condition

```text
ผ่านเมื่อ:
- เลือก ROCK
- เลือกกลุ่ม FAST/LOW
- ไม่ mutate truth
- คืน review ไม่ใช่ pass ทันที
- มี patch_candidate หรือเหตุผลว่าทำไมสร้างไม่ได้
```

---

# 5. Test Case 02 — JAZZ / Adaptive Rule Trial

## 5.1 สถานการณ์

```text
มี logic ใหม่ที่ยังไม่นิ่ง
ต้องทดลอง rule แบบยืดหยุ่นใน ENV มือถือ/Termux
```

## 5.2 Input Task

```json
{
  "task_id": "TC-RYTM-JAZZ-001",
  "source": "Cross-X",
  "target": "Modew",
  "problem": "adaptive env rule is not stable",
  "env": "termux_mobile",
  "need": "try flexible rule without core mutation",
  "boundary": "observe",
  "allow_mutation": false
}
```

## 5.3 Expected Rytm

```text
RYTM:JAZZ
```

เหตุผล:

```text
- logic ยังไม่นิ่ง
- ต้องทดลอง
- ต้องปรับตาม context
- เหมาะกับ rule / script / config มากกว่า engine หนัก
```

## 5.4 Expected Modew Style

```text
MODEW_STYLE:Adapter
```

Modew ควรทำ:

```text
- สร้าง rule ทดลอง
- รับ ctx จาก Condien/ENV
- คืน state/reason
- ถ้าไม่มั่นใจคืน review
```

## 5.5 Candidate Tags

```text
SCRIPT:*
GEN:*
CONFIG:*
DOC:*
```

## 5.6 Candidate Languages

```text
Lua
Python
JSON
YAML
Markdown
```

## 5.7 Cross-L Block

```text
CROSS-L:ADAPTIVE_ENV_RULE
POINT:MODEW_CONDIEN_ENV
RYTM:JAZZ
LANG:lua,json
BOUNDARY:observe
MODEW:ADAPTIVE_CHECK
INPUT:ctx
READ:ENV,CONDIEN.LayerA
DENY:truth_mutation,file_write,network,merge
RETURN:state,reason,trace,mutated,review
REVIEW:on_uncertain
```

## 5.8 Expected Result

```json
{
  "state": "review",
  "reason": "adaptive_rule_requires_context_confirmation",
  "rytm": "JAZZ",
  "modew_style": "Adapter",
  "candidate_tags": ["SCRIPT:*", "GEN:*", "CONFIG:*"],
  "candidate_languages": ["Lua", "Python", "JSON"],
  "cross_l_boundary": "observe",
  "mutated": false,
  "review": true
}
```

## 5.9 Pass Condition

```text
ผ่านเมื่อ:
- เลือก JAZZ
- เลือก Lua/Python/JSON ได้
- ไม่เลือก C++ เป็นตัวแรกโดยไม่จำเป็น
- มี boundary observe
- uncertainty คืน review
```

---

# 6. Test Case 03 — EDM / W3 Pulse Loop

## 6.1 สถานการณ์

```text
ต้องทำ W3 Pulse ตรวจชีพจรซ้ำเป็นรอบ ๆ
ต้องมี loop / sync / runtime signal
```

## 6.2 Input Task

```json
{
  "task_id": "TC-RYTM-EDM-001",
  "source": "PWA",
  "target": "W3_API",
  "problem": "need recurring pulse check",
  "env": "pwa_plus_termux_api",
  "need": "sync loop without mutation",
  "boundary": "observe_loop",
  "allow_mutation": false,
  "interval": "manual_or_limited"
}
```

## 6.3 Expected Rytm

```text
RYTM:EDM
```

เหตุผล:

```text
- มีจังหวะซ้ำ
- เป็น pulse / loop / sync
- เกี่ยวกับ runtime และ API call
```

## 6.4 Expected Modew Style

```text
MODEW_STYLE:Runner
```

Modew ควรทำ:

```text
- ยิง request แบบจำกัด
- ตรวจ response
- กัน loop runaway
- คืน report
```

## 6.5 Candidate Tags

```text
SCRIPT:*
WEB:*
ENV:*
CONFIG:*
QUERY:*
```

## 6.6 Candidate Languages

```text
Python
Bash
JavaScript
TypeScript
JSON
YAML
Go
```

## 6.7 Cross-L Block

```text
CROSS-L:W3_PULSE_SIGNAL
POINT:PWA_API_CROSS
RYTM:EDM
LANG:python,json,javascript
BOUNDARY:observe_loop
MODEW:PULSE_RUNNER
INPUT:request,response
READ:api_result,trace
DENY:truth_mutation,direct_merge,unlimited_loop
RETURN:state,reason,trace,mutated,review,pulse_count
REVIEW:on_error
```

## 6.8 Expected Result

```json
{
  "state": "pass",
  "reason": "pulse_request_completed_without_mutation",
  "rytm": "EDM",
  "modew_style": "Runner",
  "candidate_tags": ["SCRIPT:*", "WEB:*", "ENV:*", "CONFIG:*"],
  "candidate_languages": ["Python", "JavaScript", "JSON"],
  "cross_l_boundary": "observe_loop",
  "mutated": false,
  "review": false
}
```

## 6.9 Pass Condition

```text
ผ่านเมื่อ:
- เลือก EDM
- มี LIMIT / INTERVAL / STOP_CONDITION หรือระบุว่า manual
- ไม่เกิด loop ไม่จำกัด
- mutated=false
```

---

# 7. Test Case 04 — BALLAD / Memory Continuity

## 7.1 สถานการณ์

```text
ต้องเก็บความต่อเนื่องของแนวคิด Cross-Lgu
ทำบันทึกให้มนุษย์อ่านและระบบอ้างอิงภายหลัง
```

## 7.2 Input Task

```json
{
  "task_id": "TC-RYTM-BALLAD-001",
  "source": "Modew",
  "target": "KnowledgeLayer",
  "problem": "need continuity note for Cross-Lgu idea",
  "env": "repo_docs",
  "need": "preserve meaning and context",
  "boundary": "record_only",
  "allow_mutation": false
}
```

## 7.3 Expected Rytm

```text
RYTM:BALLAD
```

เหตุผล:

```text
- งานเน้นความต่อเนื่อง
- ไม่เร่ง
- อ่านแล้วต้องเข้าใจ
- เหมาะกับ memory / note / docs
```

## 7.4 Expected Modew Style

```text
MODEW_STYLE:Keeper
```

## 7.5 Candidate Tags

```text
DOC:*
CONFIG:*
QUERY:*
GEN:*
```

## 7.6 Candidate Languages

```text
Markdown
TXT
JSON
YAML
SQL
Python
```

## 7.7 Cross-L Block

```text
CROSS-L:CROSS_LGU_MEMORY_NOTE
POINT:KNOWLEDGE_CONTINUITY
RYTM:BALLAD
LANG:markdown,json
BOUNDARY:record_only
MODEW:MEMORY_KEEPER
INPUT:note,context
READ:summary,trace
DENY:truth_mutation,direct_merge
RETURN:state,reason,trace,mutated,review,stored_path
REVIEW:on_missing_context
```

## 7.8 Expected Result

```json
{
  "state": "review",
  "reason": "record_ready_but_requires_path_confirmation",
  "rytm": "BALLAD",
  "modew_style": "Keeper",
  "candidate_tags": ["DOC:*", "CONFIG:*", "QUERY:*"],
  "candidate_languages": ["Markdown", "JSON", "TXT"],
  "cross_l_boundary": "record_only",
  "mutated": false,
  "review": true
}
```

## 7.9 Pass Condition

```text
ผ่านเมื่อ:
- เลือก BALLAD
- เลือกกลุ่ม DOC/CONFIG/QUERY
- เน้น continuity ไม่ใช่ patch
- ไม่ใช้ ROCK โดยไม่จำเป็น
```

---

# 8. Test Case 05 — R&B / Human Friendly Report

## 8.1 สถานการณ์

```text
W3-API คืน JSON ยาว
ต้องแปลงให้ BBX19 อ่านง่ายบนมือถือ
```

## 8.2 Input Task

```json
{
  "task_id": "TC-RYTM-RNB-001",
  "source": "W3_API",
  "target": "Human",
  "problem": "raw json is too dense",
  "env": "mobile_pwa",
  "need": "human-friendly explanation",
  "boundary": "readable_output",
  "allow_mutation": false
}
```

## 8.3 Expected Rytm

```text
RYTM:R&B
```

เหตุผล:

```text
- งานนี้เน้นสื่อสารกับมนุษย์
- ต้องนุ่ม อ่านง่าย ลดแรงเสียดทาน
- ไม่ควรซ่อน risk
```

## 8.4 Expected Modew Style

```text
MODEW_STYLE:Translator
```

## 8.5 Candidate Tags

```text
DOC:*
WEB:*
GEN:*
CONFIG:*
```

## 8.6 Candidate Languages

```text
Markdown
TXT
HTML
CSS
JavaScript
Python
JSON
```

## 8.7 Cross-L Block

```text
CROSS-L:HUMAN_API_SUMMARY
POINT:RESULT_TO_HUMAN
RYTM:R&B
LANG:markdown,json
BOUNDARY:readable_output
MODEW:SOFT_REPORTER
INPUT:api_result
READ:result,trace,signal
DENY:truth_mutation,repo_write,risk_hiding
RETURN:state,reason,summary,risk,next_step,mutated,review
REVIEW:on_risk
```

## 8.8 Expected Result

```json
{
  "state": "pass",
  "reason": "result_translated_for_human_reading",
  "rytm": "R&B",
  "modew_style": "Translator",
  "candidate_tags": ["DOC:*", "WEB:*", "GEN:*"],
  "candidate_languages": ["Markdown", "JSON", "JavaScript"],
  "cross_l_boundary": "readable_output",
  "mutated": false,
  "review": false
}
```

## 8.9 Pass Condition

```text
ผ่านเมื่อ:
- เลือก R&B
- แสดงผลให้อ่านง่าย
- ยังแสดง risk ถ้ามี
- ไม่แก้ข้อมูลต้นฉบับ
```

---

# 9. Test Case 06 — STRING / Long-form Knowledge Chain

## 9.1 สถานการณ์

```text
ต้องเชื่อมเอกสารหลายไฟล์ เช่น croll README, language tag table, Rytm routing guide
ให้กลายเป็นสายความหมายเดียวกัน
```

## 9.2 Input Task

```json
{
  "task_id": "TC-RYTM-STRING-001",
  "source": "KnowledgeLayer",
  "target": "CROLL",
  "problem": "multiple documents need semantic relation",
  "env": "repo_docs",
  "need": "long-form orchestration and relation map",
  "boundary": "knowledge_index",
  "allow_mutation": false
}
```

## 9.3 Expected Rytm

```text
RYTM:STRING
```

เหตุผล:

```text
- เอกสารหลายชั้น
- ความหมายต่อเนื่องระยะยาว
- ต้องเชื่อม relation ไม่ใช่แค่สรุปสั้น
```

## 9.4 Expected Modew Style

```text
MODEW_STYLE:Binder
```

## 9.5 Candidate Tags

```text
DOC:*
QUERY:*
FORMAL:*
CONFIG:*
GEN:*
```

## 9.6 Candidate Languages

```text
Markdown
YAML
JSON
SQL
SPARQL
Datalog
Lean
Python
```

## 9.7 Cross-L Block

```text
CROSS-L:CROLL_KNOWLEDGE_CHAIN
POINT:DOC_RELATION_CROSS
RYTM:STRING
LANG:markdown,yaml,python
BOUNDARY:knowledge_index
MODEW:RELATION_MAPPER
INPUT:document_list
READ:docs,headings,links
DENY:truth_mutation,delete_docs,direct_merge
RETURN:state,reason,trace,mutated,review,relation_map
REVIEW:on_conflict
```

## 9.8 Expected Result

```json
{
  "state": "review",
  "reason": "relation_map_ready_for_human_confirmation",
  "rytm": "STRING",
  "modew_style": "Binder",
  "candidate_tags": ["DOC:*", "QUERY:*", "FORMAL:*", "CONFIG:*"],
  "candidate_languages": ["Markdown", "YAML", "Python"],
  "cross_l_boundary": "knowledge_index",
  "mutated": false,
  "review": true
}
```

## 9.9 Pass Condition

```text
ผ่านเมื่อ:
- เลือก STRING
- มองเป็น relation/knowledge chain
- ไม่มองเป็น bug patch
- คืน relation_map หรือเหตุผลที่ต้อง review
```

---

# 10. Negative Test Cases

## 10.1 ROCK แต่ขอ mutate truth ทันที

Input:

```json
{
  "rytm": "ROCK",
  "request": "patch and merge immediately",
  "allow_mutation": true,
  "review": false
}
```

Expected:

```json
{
  "state": "block",
  "reason": "truth_mutation_requires_higher_review",
  "mutated": false,
  "review": true
}
```

---

## 10.2 EDM loop ไม่มี limit

Input:

```json
{
  "rytm": "EDM",
  "request": "run pulse forever",
  "limit": null,
  "stop_condition": null
}
```

Expected:

```json
{
  "state": "review",
  "reason": "loop_requires_limit_or_stop_condition",
  "mutated": false,
  "review": true
}
```

---

## 10.3 R&B ทำให้ risk หายไป

Input:

```json
{
  "rytm": "R&B",
  "request": "make error sound harmless",
  "risk": "api_blocked"
}
```

Expected:

```json
{
  "state": "block",
  "reason": "risk_hiding_not_allowed",
  "mutated": false,
  "review": true
}
```

---

## 10.4 JAZZ ไม่มี boundary

Input:

```json
{
  "rytm": "JAZZ",
  "request": "try adaptive rule",
  "boundary": null
}
```

Expected:

```json
{
  "state": "review",
  "reason": "missing_boundary",
  "mutated": false,
  "review": true
}
```

---

# 11. Quick Visual Summary

| Test | Rytm | Modew | Tags | Expected |
|---|---|---|---|---|
| Native bug patch | ROCK | Fixer | FAST / LOW | review |
| Adaptive rule | JAZZ | Adapter | SCRIPT / CONFIG | review |
| W3 Pulse loop | EDM | Runner | SCRIPT / WEB / ENV | pass/review |
| Memory note | BALLAD | Keeper | DOC / CONFIG | review |
| Human report | R&B | Translator | DOC / WEB | pass |
| Knowledge chain | STRING | Binder | DOC / QUERY / FORMAL | review |

---

# 12. How To Use This File

ใช้ไฟล์นี้คู่กับ:

```text
croll/CROSS_L_RYTM_MODEW_ROUTING.md
croll/CROSS_L_LANGUAGE_TAG_TABLE.md
croll/test.md
```

ลำดับการใช้งาน:

```text
1. ดูงานจริง
2. เทียบกับ testcase ที่ใกล้ที่สุด
3. เลือก Rytm
4. เลือก Modew style
5. เลือก tag family
6. เลือกภาษาใน Language Tag Table
7. สร้าง Cross-L block
8. ตรวจ return contract
9. ส่งผลเข้า MPCP / LRC2
```

---

# 13. Final Statement

Testcase เหล่านี้มีไว้เพื่อให้เห็นภาพรวม

ไม่ใช่กฎตายตัว

ถ้างานจริงเปลี่ยน จังหวะอาจเปลี่ยนได้

แต่ทุกกรณีต้องรักษา:

```text
boundary
return contract
traceability
mutated:false by default
review on uncertainty
```

```text
Rytm helps choose the path.
Modew walks the path.
Cross-L keeps the path governed.
```

END
