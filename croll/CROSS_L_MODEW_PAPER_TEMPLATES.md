# Cross-L Modew Paper Templates

**Document Path:** `croll/CROSS_L_MODEW_PAPER_TEMPLATES.md`  
**Status:** ACTIVE DRAFT / SCAFFOLD  
**System Relation:** W3 / CROLL / Cross-L / CrossLgu / Paper / Condien / Rytm / Color / Symbol / Cross-X / Modew / MPCP / LRC2  
**Owner:** BBX19  
**Purpose:** โครงเอกสารสำหรับกำหนด Paper Template ที่ใช้กับ `Layer ของ Cross-L เท่านั้น` เพื่อให้ Trigger สามารถเรียกศักยภาพของ Modew ได้เร็ว ชัด และลดการลังเล

---

# 1. Scope Lock

เอกสารนี้ใช้สำหรับ:

```text
Layer ของ Cross-L เท่านั้น
```

ไม่ใช่กฎของ Paper ทุกชนิดใน W3

ไม่ใช่กฎของ Modew ทุกกรณี

ไม่ใช่กฎของ MPCP ทั้งระบบ

ไม่ใช่กฎของ W3Lgu ทั้งหมด

จุดประสงค์คือทำให้ `Cross-L` สามารถรับ Paper แล้วแตกเป็นชุดงานให้ `Modew` ได้เร็วขึ้น

---

# 2. Core Statement

Modew ไม่ได้ถูกออกแบบมาให้ฉลาดที่สุด

Modew ถูกออกแบบมาให้:

```text
- รับงานได้กว้าง
- ทำตามกรอบได้ดี
- ปรับบทบาทตามบริบทได้
- ทำงานตาม Paper ได้
- ใช้ Condien ตามสิทธิ์ได้
- คืนผลลัพธ์ที่ trace ได้
```

ดังนั้น Modew ควรมี `Paper Template` สำหรับงานของ Cross-L

เพราะ:

```text
Trigger ดึง template ที่ถูกงาน
Paper Template กำหนดขั้นตอน
Cross-L สร้าง workset
Modew ลงมือใน boundary
```

ประโยคจำง่าย:

```text
Modew does not need full intelligence.
Modew needs the right template at the right trigger.
```

แบบไทย:

```text
Modew ไม่จำเป็นต้องฉลาดมาก
แต่ต้องได้รับ template ที่ถูกต้องจาก trigger ที่ถูกงาน
```

---

# 3. Why This Exists

ถ้า Paper ที่ยิงเข้า Cross-L ไม่มี step ชัดเจน:

```text
Cross-L ต้องเดา
Modew ต้องเดา
Condien ต้องสร้าง context แบบกว้างเกินไป
ระบบลังเล
งานช้า
boundary ไม่ชัด
```

ดังนั้น Paper ของ Cross-L ควรมีโครงขั้นต่ำ:

```text
STEP 1: CLASSIFY
STEP 2: BUILD_WORKSET
STEP 3: DISPATCH
```

---

# 4. Benefit to Condien

ข้อดีสำคัญ:

```text
Condien สามารถสร้างสถานะข้อมูลเฉพาะได้เร็ว
เพราะ layer ชัดเจน
```

เมื่อ Paper ระบุ step ชัด:

```text
- Condien รู้ว่าต้องเตรียม context ชั้นไหน
- Cross-L รู้ว่าต้องอ่านข้อมูลใด
- Modew รู้ว่าต้องใช้ข้อมูลไหน
- ไม่ต้องเปิด context ทั้งระบบ
- ลดการดึงข้อมูลเกินจำเป็น
- ลด semantic drift
- ลดการลังเลก่อน execution
```

ตัวอย่าง:

```text
RYTM:JAZZ
COLOR:YELLOW
SYMBOL:◆
BOUNDARY:observe
READ:CONDIEN.LayerA,ENV
```

Condien จะรู้ทันทีว่า:

```text
สร้าง context สำหรับ adaptive rule เท่านั้น
ไม่ต้องสร้าง full system context
ไม่ต้องเปิด truth layer
ไม่ต้องเปิด write layer
```

---

# 5. Core Flow

```text
Trigger
→ Select Paper Template
→ Paper STEP 1 / 2 / 3
→ Cross-L Build Workset
→ Condien Prepare Scoped State
→ Modew Execute Bounded Work
→ Return Contract
→ MPCP Validate
→ LRC2 Log
```

อธิบาย:

```text
1. Trigger เห็นจังหวะ / สี / สัญลักษณ์ / ประเภทงาน
2. Trigger เลือก Paper Template
3. Paper บอก STEP 1/2/3 ให้ Cross-L
4. Cross-L สร้างชุดงานเบื้องต้น
5. Condien สร้างสถานะข้อมูลเฉพาะตาม layer
6. Modew ทำงานตามชุดงาน
7. ผลลัพธ์ถูกคืนผ่าน return contract
8. MPCP รับ/ตรวจผล
9. LRC2 บันทึก trace
```

---

# 6. Paper Template Minimal Structure

Paper สำหรับ Cross-L ควรมีรูปแบบขั้นต่ำ:

```text
PAPER:<paper_id>
SCOPE:CROSS_L_ONLY
TARGET:<target>
INTENT:<intent>
ENV:<env>
BOUNDARY:<boundary>

STEP1:CLASSIFY
RYTM:<rytm>
COLOR:<color>
SYMBOL:<symbol>
WORK_TYPE:<work_type>

STEP2:BUILD_WORKSET
TAG_GROUP:<tag_group>
LANG_CANDIDATE:<languages>
READ:<condien_layers_or_context>
RETURN:<return_contract>

STEP3:DISPATCH
MODEW:<modew_name>
DENY:<denied_actions>
REVIEW:<review_policy>
```

---

# 7. Required Fields

| Field | Required | Meaning |
|---|---|---|
| `SCOPE:CROSS_L_ONLY` | yes | ยืนยันว่า template นี้ใช้กับ Cross-L layer เท่านั้น |
| `TARGET` | yes | เป้าหมายงาน |
| `INTENT` | yes | เจตนางาน |
| `ENV` | yes | สภาพแวดล้อม |
| `BOUNDARY` | yes | ขอบเขตการทำงาน |
| `RYTM` | recommended | จังหวะงาน |
| `COLOR` | optional/recommended | สถานะ/ความเสี่ยง |
| `SYMBOL` | optional/recommended | รูปทรงงาน |
| `TAG_GROUP` | yes | กลุ่มภาษา/เครื่องมือ |
| `LANG_CANDIDATE` | yes | ภาษาที่ควรมองก่อน |
| `READ` | yes | Condien/context ที่อ่านได้ |
| `DENY` | yes | สิ่งที่ห้ามทำ |
| `RETURN` | yes | รูปแบบผลลัพธ์ที่ต้องคืน |
| `MODEW` | yes | Modew ที่รับงาน |
| `REVIEW` | yes | เงื่อนไข review |

---

# 8. Template 01 — MODEW_FAST_PATCH_PAPER

ใช้เมื่อ:

```text
งานเป็น bug / pressure / patch / urgent / performance issue
```

Trigger ที่มักเกี่ยวข้อง:

```text
RYTM:ROCK
COLOR:RED or ORANGE
SYMBOL:▲ or !
```

Template:

```text
PAPER:MODEW_FAST_PATCH_PAPER
SCOPE:CROSS_L_ONLY
TARGET:<target_component>
INTENT:create_fast_patch_candidate
ENV:<env>
BOUNDARY:temp_patch

STEP1:CLASSIFY
RYTM:ROCK
COLOR:RED
SYMBOL:▲
WORK_TYPE:FAST_PATCH

STEP2:BUILD_WORKSET
TAG_GROUP:FAST,LOW,SCRIPT,CONFIG
LANG_CANDIDATE:cpp,rust,c,asm,bash,json,wasm
READ:ENV,trace,error_report,CONDIEN.LayerA
RETURN:state,reason,trace,mutated,review,patch_candidate

STEP3:DISPATCH
MODEW:FAST_PATCH
DENY:truth_mutation,direct_merge,repo_write_without_review
REVIEW:on_complete
```

Condien expectation:

```text
Condien ควรสร้าง context เฉพาะ error/trace/env
ไม่ต้องเปิด knowledge layer ทั้งหมด
```

---

# 9. Template 02 — MODEW_ADAPTIVE_RULE_PAPER

ใช้เมื่อ:

```text
logic ยังไม่นิ่ง / rule ต้องทดลอง / ต้องปรับตาม context
```

Trigger:

```text
RYTM:JAZZ
COLOR:YELLOW
SYMBOL:◆ or ?
```

Template:

```text
PAPER:MODEW_ADAPTIVE_RULE_PAPER
SCOPE:CROSS_L_ONLY
TARGET:<rule_target>
INTENT:test_adaptive_rule
ENV:<env>
BOUNDARY:observe

STEP1:CLASSIFY
RYTM:JAZZ
COLOR:YELLOW
SYMBOL:◆
WORK_TYPE:ADAPTIVE_RULE

STEP2:BUILD_WORKSET
TAG_GROUP:SCRIPT,GEN,CONFIG,DOC
LANG_CANDIDATE:lua,python,json,yaml,markdown
READ:ENV,CONDIEN.LayerA,CONDIEN.LayerC
RETURN:state,reason,trace,mutated,review

STEP3:DISPATCH
MODEW:ADAPTIVE_CHECK
DENY:truth_mutation,file_write,network,merge
REVIEW:on_uncertain
```

Condien expectation:

```text
Condien เตรียม state เฉพาะ context ที่จำเป็นกับ rule
ไม่ต้องสร้าง full runtime memory
```

---

# 10. Template 03 — MODEW_PULSE_RUNNER_PAPER

ใช้เมื่อ:

```text
งานเป็น loop / pulse / sync / monitoring / runtime check
```

Trigger:

```text
RYTM:EDM
COLOR:BLUE
SYMBOL:●
```

Template:

```text
PAPER:MODEW_PULSE_RUNNER_PAPER
SCOPE:CROSS_L_ONLY
TARGET:<pulse_target>
INTENT:run_limited_pulse_check
ENV:<env>
BOUNDARY:observe_loop

STEP1:CLASSIFY
RYTM:EDM
COLOR:BLUE
SYMBOL:●
WORK_TYPE:RUNTIME_PULSE

STEP2:BUILD_WORKSET
TAG_GROUP:SCRIPT,WEB,ENV,CONFIG,QUERY
LANG_CANDIDATE:python,bash,javascript,typescript,json,yaml,go
READ:api_result,trace,ENV,CONDIEN.LayerA
RETURN:state,reason,trace,mutated,review,pulse_count

STEP3:DISPATCH
MODEW:PULSE_RUNNER
DENY:truth_mutation,direct_merge,unlimited_loop,log_flood
REVIEW:on_error
LIMIT:required
STOP_CONDITION:required
```

Condien expectation:

```text
Condien สร้าง state แบบ runtime/pulse เท่านั้น
ต้องมี interval/limit/stop_condition เพื่อกัน runaway
```

---

# 11. Template 04 — MODEW_MEMORY_KEEPER_PAPER

ใช้เมื่อ:

```text
งานเป็น memory / continuity / note / record / knowledge preserve
```

Trigger:

```text
RYTM:BALLAD
COLOR:GREEN or BLUE
SYMBOL:■ or ●
```

Template:

```text
PAPER:MODEW_MEMORY_KEEPER_PAPER
SCOPE:CROSS_L_ONLY
TARGET:<memory_target>
INTENT:preserve_continuity_note
ENV:<env>
BOUNDARY:record_only

STEP1:CLASSIFY
RYTM:BALLAD
COLOR:GREEN
SYMBOL:■
WORK_TYPE:MEMORY_CONTINUITY

STEP2:BUILD_WORKSET
TAG_GROUP:DOC,CONFIG,QUERY,GEN
LANG_CANDIDATE:markdown,txt,json,yaml,sql,python
READ:summary,trace,CONDIEN.LayerB,CONDIEN.LayerC
RETURN:state,reason,trace,mutated,review,stored_path

STEP3:DISPATCH
MODEW:MEMORY_KEEPER
DENY:truth_mutation,direct_merge,delete_docs
REVIEW:on_missing_context
```

Condien expectation:

```text
Condien เตรียม context เพื่อ continuity และ summary
ไม่ต้องเปิด execution state
```

---

# 12. Template 05 — MODEW_HUMAN_REPORT_PAPER

ใช้เมื่อ:

```text
ต้องแปลงผลลัพธ์เทคนิคให้มนุษย์อ่านง่าย
```

Trigger:

```text
RYTM:R&B
COLOR:BLUE or GREEN
SYMBOL:● or ✓
```

Template:

```text
PAPER:MODEW_HUMAN_REPORT_PAPER
SCOPE:CROSS_L_ONLY
TARGET:<human_target>
INTENT:translate_result_for_human
ENV:<env>
BOUNDARY:readable_output

STEP1:CLASSIFY
RYTM:R&B
COLOR:BLUE
SYMBOL:●
WORK_TYPE:HUMAN_REPORT

STEP2:BUILD_WORKSET
TAG_GROUP:DOC,WEB,GEN,CONFIG
LANG_CANDIDATE:markdown,txt,html,css,javascript,python,json
READ:result,trace,signal,CONDIEN.LayerC
RETURN:state,reason,summary,risk,next_step,mutated,review

STEP3:DISPATCH
MODEW:SOFT_REPORTER
DENY:truth_mutation,repo_write,risk_hiding
REVIEW:on_risk
```

Condien expectation:

```text
Condien เตรียม result/trace/risk เท่านั้น
ไม่ต้องเปิด raw internal ทั้งหมดถ้าไม่จำเป็น
```

---

# 13. Template 06 — MODEW_RELATION_MAPPER_PAPER

ใช้เมื่อ:

```text
ต้องเชื่อมเอกสารหลายไฟล์ / relation / semantic chain / long-form knowledge
```

Trigger:

```text
RYTM:STRING
COLOR:PURPLE
SYMBOL:◆ or ✚
```

Template:

```text
PAPER:MODEW_RELATION_MAPPER_PAPER
SCOPE:CROSS_L_ONLY
TARGET:<knowledge_target>
INTENT:create_relation_map
ENV:<env>
BOUNDARY:knowledge_index

STEP1:CLASSIFY
RYTM:STRING
COLOR:PURPLE
SYMBOL:◆
WORK_TYPE:KNOWLEDGE_CHAIN

STEP2:BUILD_WORKSET
TAG_GROUP:DOC,QUERY,FORMAL,CONFIG,GEN
LANG_CANDIDATE:markdown,yaml,json,sql,sparql,datalog,lean,python
READ:docs,headings,links,CONDIEN.LayerC,CONDIEN.LayerD
RETURN:state,reason,trace,mutated,review,relation_map

STEP3:DISPATCH
MODEW:RELATION_MAPPER
DENY:truth_mutation,delete_docs,direct_merge
REVIEW:on_conflict
```

Condien expectation:

```text
Condien เตรียม semantic relation context
ไม่ใช่ runtime execution context
```

---

# 14. Trigger → Template Table

| Trigger | Template | Modew Style |
|---|---|---|
| `ROCK + RED + ▲` | `MODEW_FAST_PATCH_PAPER` | Fixer |
| `JAZZ + YELLOW + ◆` | `MODEW_ADAPTIVE_RULE_PAPER` | Adapter |
| `EDM + BLUE + ●` | `MODEW_PULSE_RUNNER_PAPER` | Runner |
| `BALLAD + GREEN + ■` | `MODEW_MEMORY_KEEPER_PAPER` | Keeper |
| `R&B + BLUE + ●` | `MODEW_HUMAN_REPORT_PAPER` | Translator |
| `STRING + PURPLE + ◆` | `MODEW_RELATION_MAPPER_PAPER` | Binder |

---

# 15. Safety Rule

## 15.1 Template is not permission

Paper Template ไม่ใช่สิทธิ์ให้ execute ทันที

มันเป็น:

```text
ใบจัดรูปงานสำหรับ Cross-L layer
```

ยังต้องผ่าน:

```text
Boundary
Deny
Return Contract
Review Rule
MPCP validation
LRC2 log
```

---

## 15.2 Cross-L only

ทุก template ในไฟล์นี้ต้องจำกัด scope:

```text
SCOPE:CROSS_L_ONLY
```

ถ้า Paper ไม่ได้ยิงเข้า Cross-L:

```text
ไม่จำเป็นต้องใช้ STEP1/2/3
ไม่จำเป็นต้องรู้ template นี้
ไม่ควรถูกบังคับใช้
```

---

## 15.3 Condien should be scoped

Condien ไม่ควรเปิด context กว้างเกินงาน

ควรสร้าง state เฉพาะตาม:

```text
RYTM
COLOR
SYMBOL
WORK_TYPE
BOUNDARY
READ
```

---

# 16. Minimal Runtime Algorithm

```text
1. Receive Paper
2. Check SCOPE == CROSS_L_ONLY
3. Read STEP1 classify
4. Match trigger to template
5. Build workset from STEP2
6. Ask Condien for scoped state only
7. Dispatch to Modew from STEP3
8. Validate return contract
9. Return to MPCP
10. Log to LRC2
```

---

# 17. Final Statement

Paper Template ของ Modew มีไว้เพื่อให้ Cross-L ทำงานเร็วขึ้น ไม่ใช่เพื่อเพิ่มความซับซ้อนให้ทุกระบบ

```text
Only Cross-L layer needs this process.
Other layers should not hesitate because of it.
```

แบบไทย:

```text
กระบวนการนี้มีไว้สำหรับ layer ของ Cross-L เท่านั้น
ส่วนที่ไม่เกี่ยวข้องไม่ต้องรู้
เพื่อให้ระบบอื่นไม่ลังเล
```

และข้อดีสำคัญคือ:

```text
Condien สร้างสถานะข้อมูลเฉพาะได้เร็วขึ้น
เพราะ layer ชัดเจน
```

END
