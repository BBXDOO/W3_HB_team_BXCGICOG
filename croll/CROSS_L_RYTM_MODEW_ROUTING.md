# Cross-L Rytm Modew Routing Guide

**Document Path:** `croll/CROSS_L_RYTM_MODEW_ROUTING.md`  
**Status:** ACTIVE DRAFT  
**System Relation:** W3 / CROLL / Cross-L / CrossLgu / EP_SIGNAL / Rytm / Cross-X / Modew / MPCP  
**Owner:** BBX19  
**Purpose:** เอกสารอธิบายการใช้ `EP_SIGNAL:Rytm` เป็นจังหวะสัญญาณเพื่อช่วย `Cross-X` ส่งงานให้ `Modew` เลือกกลุ่มภาษา / เครื่องมือ / CrossCode ได้ถูกงาน

---

# 1. บทนำ

เอกสารนี้จัดทำเพื่ออธิบายว่า `Rytm` สามารถช่วยระบบ `Cross-L / CrossLgu` ได้อย่างไร

โดยเฉพาะในกรณีที่ W3 ต้องเลือกว่า:

```text
งานนี้ควรใช้ภาษาอะไร
สคริปต์แบบไหน
config แบบไหน
หรือควรให้ Modew ใช้เครื่องมือชนิดใดก่อน
```

แนวคิดสำคัญคือ:

```text
Rytm ไม่ได้บอกแค่ว่าสัญญาณคืออะไร
แต่บอกว่า “งานนี้เคลื่อนด้วยจังหวะแบบไหน”
```

เมื่อรู้จังหวะของงานแล้ว `Cross-X` สามารถใช้จังหวะนั้นส่งต่อให้ `Modew` เลือกกลุ่มภาษาได้ง่ายขึ้น

---

# 2. แกนความหมาย

## 2.1 EP_SIGNAL

`EP_SIGNAL` คือชั้นเข้ารหัสโครงสร้างของสัญญาณ

หน้าที่หลัก:

```text
- ย่อ binary / pulse ให้เป็นรูปแบบอ่านได้
- รักษาโครงสร้างสัญญาณ
- ทำให้สัญญาณ reversible เมื่อเป็นไปได้
- ใช้เป็นรากของ signal packet
```

พูดง่าย ๆ:

```text
EP_SIGNAL = โครงกระดูกของสัญญาณ
```

---

## 2.2 Rytm

`Rytm` คือชั้นจังหวะพฤติกรรมของสัญญาณ

หน้าที่หลัก:

```text
- ดูว่าสัญญาณเคลื่อนอย่างไร
- ดูแรงกด / ความนุ่ม / ความเร็ว / ความซ้ำ / ความยืดหยุ่น
- ใช้บอกลักษณะงานเชิงพฤติกรรม
- ช่วยให้ระบบรู้ว่างานนี้ควรเข้าทางไหน
```

พูดง่าย ๆ:

```text
Rytm = จังหวะการเคลื่อนของงาน
```

---

## 2.3 Cross-X

`Cross-X` คือจุดประสานหรือจุดตัดของหลายปัจจัย

เช่น:

```text
Modew + Condien + Paper + ENV + Boundary
```

หน้าที่หลัก:

```text
- เห็นว่าตรงนี้เป็น cross point
- ดูว่ามีปัจจัยอะไรต้องมารวมกัน
- ส่งงานไปยังหน่วยที่เหมาะสม
```

พูดง่าย ๆ:

```text
Cross-X = จุดตัด / จุดส่งงาน
```

---

## 2.4 Modew

`Modew` คือหน่วยรับงานของ MPCP

Modew ไม่จำเป็นต้องฉลาดที่สุด แต่ต้อง:

```text
- รับงานได้กว้าง
- ปรับ property ได้
- เปลี่ยน argument ได้
- ใช้ Paper กำกับได้
- ใช้ Condien เป็นบริบทได้
- เลือกเครื่องมือหรือภาษาให้ตรงงานได้
```

พูดง่าย ๆ:

```text
Modew = คนงานหน้างานของระบบ
```

---

## 2.5 Cross-L / CrossLgu

`Cross-L` คือชั้นกำกับ code fragment / logic fragment จากหลายภาษา

หน้าที่หลัก:

```text
- บอกว่า fragment นี้ใช้ภาษาอะไร
- อยู่ใน boundary ไหน
- อ่านอะไรได้
- ห้ามแตะอะไร
- ต้องคืนค่าอะไร
- ต้องส่งต่อให้ระบบไหน
```

พูดง่าย ๆ:

```text
Cross-L = กติกาของโค้ดหลายภาษาในจุดตัด
```

---

# 3. Flow หลัก

โครง flow ที่ต้องจำ:

```text
EP_SIGNAL
→ Rytm
→ Cross-X
→ Modew
→ Cross-L / CrossCode
→ MPCP
→ LRC2
```

อธิบายทีละชั้น:

```text
1. EP_SIGNAL ให้โครงสร้างสัญญาณ
2. Rytm อ่านจังหวะพฤติกรรมของสัญญาณ
3. Cross-X ใช้จังหวะนั้นดูว่าเป็นงานประเภทไหน
4. Modew เลือกกลุ่มภาษา / เครื่องมือ / วิธีแก้ตามจังหวะงาน
5. Cross-L ประกาศ boundary และ return contract ของ CrossCode
6. MPCP รับผลลัพธ์กลับเข้าระบบ
7. LRC2 บันทึก trace / memory / continuity
```

---

# 4. หลักคิดสำคัญ

```text
Rytm ไม่ใช่ตัวตัดสินสุดท้าย
Rytm เป็นตัวช่วยบอก “จังหวะงาน”
```

ดังนั้น Rytm ไม่ควรกลายเป็น authority แข็ง ๆ

มันควรเป็น:

```text
temporary classifier
```

แปลว่า:

```text
ตัวช่วยจัดประเภทชั่วคราว
เพื่อให้ Modew เริ่มเลือกภาษา/เครื่องมือได้ถูกทาง
```

ถ้า Rytm บอกว่าเป็น `ROCK` ไม่ได้แปลว่าต้องใช้ C++ เสมอ

แต่แปลว่า:

```text
งานนี้มีแรงกด / เร็ว / กระแทก / ต้องการการลงมือชัด
ควรเริ่มมองกลุ่ม FAST / LOW / PATCH ก่อน
```

---

# 5. Rytm Behavioral Taxonomy

ตารางนี้ใช้เป็นจุดเริ่มต้นสำหรับ `Rytm → Modew Selection`

---

## 5.1 BALLAD

### ความหมาย

```text
BALLAD = จังหวะนุ่ม ยาว ต่อเนื่อง สะท้อนคิด
```

### ลักษณะ

```text
- smooth continuity
- emotional stability
- reflective pacing
- soft transition
- long sustain
```

### ใช้กับงานแบบไหน

```text
- memory flow
- continuity systems
- reflection documents
- human-safe communication
- long-term notes
- knowledge preservation
```

### กลุ่มภาษา / tag ที่เหมาะ

| Tag Family | ตัวอย่าง | เหตุผล |
|---|---|---|
| `DOC:*` | `DOC:MD`, `DOC:TXT` | ใช้เขียนความหมาย / บันทึก / paper |
| `CONFIG:*` | `CONFIG:JSON`, `CONFIG:YML` | เก็บสถานะ / context แบบอ่านได้ |
| `QUERY:*` | `QUERY:SQL` | ใช้กับ memory / storage |
| `GEN:*` | `GEN:PY` | ใช้คุม flow เบา ๆ และจัดข้อมูล |

### ตัวอย่าง Modew

```text
MODEW:MEMORY_SUMMARY
MODEW:KNOWLEDGE_KEEPER
MODEW:CONTINUITY_REPORT
```

### ตัวอย่าง Cross-L

```text
CROSS-L:MEMORY_NOTE
RYTM:BALLAD
LANG:markdown,json
BOUNDARY:record_only
RETURN:state,reason,trace,mutated,review
```

---

## 5.2 ROCK

### ความหมาย

```text
ROCK = จังหวะแรง เร็ว กระแทก มีแรงกด ใช้กับงานที่ต้องลงมือชัด
```

### ลักษณะ

```text
- aggressive transition
- strong execution pressure
- operational momentum
- sharp pulse bursts
- high urgency
```

### ใช้กับงานแบบไหน

```text
- bug patch
- conflict resolution
- rapid deployment
- emergency fix
- performance pressure
- low-level correction
```

### กลุ่มภาษา / tag ที่เหมาะ

| Tag Family | ตัวอย่าง | เหตุผล |
|---|---|---|
| `FAST:*` | `FAST:CPP`, `FAST:RS` | งานเร็ว / engine / performance |
| `LOW:*` | `LOW:C`, `LOW:ASM` | แก้ใกล้ระบบ / memory / hardware behavior |
| `SCRIPT:*` | `SCRIPT:BASH` | สั่งงานเร็วใน ENV |
| `ENV:*` | `ENV:DOCKER`, `ENV:ENV` | คุมสภาพแวดล้อม runtime |
| `CONFIG:*` | `CONFIG:JSON` | เก็บ patch packet / result contract |

### ตัวอย่าง Modew

```text
MODEW:FIELD_FIX
MODEW:FAST_PATCH
MODEW:ERROR_BREAKER
MODEW:LOW_LEVEL_CHECK
```

### ตัวอย่าง Cross-L

```text
CROSS-L:FAST_PATCH
RYTM:ROCK
LANG:cpp,asm,json
BOUNDARY:temp_patch
DENY:truth_mutation,direct_merge
RETURN:state,reason,trace,mutated,review
```

---

## 5.3 JAZZ

### ความหมาย

```text
JAZZ = จังหวะยืดหยุ่น ด้นสด ปรับตามบริบท เหมาะกับ logic ที่ยังไม่นิ่ง
```

### ลักษณะ

```text
- adaptive irregularity
- contextual improvisation
- dynamic interpretation
- non-fixed cadence
- exploratory logic
```

### ใช้กับงานแบบไหน

```text
- experimental runtime
- AI collaboration
- flexible orchestration
- rule draft
- context-sensitive behavior
- logic ที่ยังต้องทดลอง
```

### กลุ่มภาษา / tag ที่เหมาะ

| Tag Family | ตัวอย่าง | เหตุผล |
|---|---|---|
| `SCRIPT:*` | `SCRIPT:LUA`, `SCRIPT:PY` | logic เบา แก้เร็ว ทดลองง่าย |
| `CONFIG:*` | `CONFIG:JSON`, `CONFIG:YML` | เก็บ rule object / behavior config |
| `GEN:*` | `GEN:PY`, `GEN:JS` | คุม flow / ทดลอง runtime |
| `DOC:*` | `DOC:MD` | เก็บเหตุผล / paper / note |

### ตัวอย่าง Modew

```text
MODEW:RULE_TRIAL
MODEW:ADAPTIVE_CHECK
MODEW:CONTEXT_PLAYER
MODEW:EXPERIMENT_RUNNER
```

### ตัวอย่าง Cross-L

```text
CROSS-L:ADAPTIVE_RULE
RYTM:JAZZ
LANG:lua,json,python
BOUNDARY:observe
READ:CONDIEN.LayerA,ENV
DENY:truth_mutation,file_write,merge
RETURN:state,reason,trace,mutated,review
```

---

## 5.4 STRING

### ความหมาย

```text
STRING = จังหวะชั้นซ้อน เรียงตัว สง่างาม ต่อเนื่องระยะยาว
```

### ลักษณะ

```text
- layered continuity
- harmonic structure
- elegant transition
- long-form orchestration
- semantic memory
```

### ใช้กับงานแบบไหน

```text
- semantic memory
- long-form orchestration
- civilization-scale continuity
- knowledge architecture
- multi-document relation
- philosophy / governance chain
```

### กลุ่มภาษา / tag ที่เหมาะ

| Tag Family | ตัวอย่าง | เหตุผล |
|---|---|---|
| `DOC:*` | `DOC:MD`, `DOC:RST`, `DOC:ADOC` | เอกสารยาว / philosophy / governance |
| `QUERY:*` | `QUERY:SQL`, `QUERY:SPARQL` | memory / relation / knowledge graph |
| `CONFIG:*` | `CONFIG:YML`, `CONFIG:JSON` | โครง relation / index |
| `FORMAL:*` | `FORMAL:LEAN`, `FORMAL:DATALOG` | logic formal / proof / rule relation |
| `GEN:*` | `GEN:PY` | parser / indexer / organizer |

### ตัวอย่าง Modew

```text
MODEW:KNOWLEDGE_ARCHIVIST
MODEW:RELATION_MAPPER
MODEW:PHILOSOPHY_BINDER
MODEW:LONG_MEMORY_ORCHESTRATOR
```

### ตัวอย่าง Cross-L

```text
CROSS-L:KNOWLEDGE_CHAIN
RYTM:STRING
LANG:markdown,yaml,sql,python
BOUNDARY:knowledge_index
RETURN:state,reason,trace,mutated,review
```

---

## 5.5 EDM

### ความหมาย

```text
EDM = จังหวะซ้ำ ชัด sync สูง เหมาะกับ loop / runtime / stream
```

### ลักษณะ

```text
- synchronized repetition
- energetic pulse cycles
- repetitive signal reinforcement
- runtime synchronization
- active operational streams
```

### ใช้กับงานแบบไหน

```text
- runtime loop
- repeated execution
- sync task
- stream monitoring
- health pulse
- event dispatch
- automation cycle
```

### กลุ่มภาษา / tag ที่เหมาะ

| Tag Family | ตัวอย่าง | เหตุผล |
|---|---|---|
| `SCRIPT:*` | `SCRIPT:BASH`, `SCRIPT:PY` | automation / loop / runner |
| `WEB:*` | `WEB:JS`, `WEB:TS` | event loop / UI runtime |
| `GEN:*` | `GEN:GO`, `GEN:PY` | service / runtime / worker |
| `ENV:*` | `ENV:DOCKER`, `ENV:K8S` | runtime environment / deployment |
| `CONFIG:*` | `CONFIG:JSON`, `CONFIG:YML` | job config / sync packet |
| `QUERY:*` | `QUERY:LOGQL`, `QUERY:PROMQL` | log / metric monitoring |

### ตัวอย่าง Modew

```text
MODEW:PULSE_RUNNER
MODEW:SYNC_WORKER
MODEW:LOOP_MONITOR
MODEW:EVENT_DISPATCHER
```

### ตัวอย่าง Cross-L

```text
CROSS-L:W3_PULSE_LOOP
RYTM:EDM
LANG:python,bash,json
BOUNDARY:observe_loop
DENY:truth_mutation,direct_merge
RETURN:state,reason,trace,mutated,review
```

---

## 5.6 R&B

### ความหมาย

```text
R&B = จังหวะนุ่ม ประสานมนุษย์-ระบบ ลดแรงเสียดทานของการสื่อสาร
```

### ลักษณะ

```text
- emotional smoothing
- soft transition
- interpersonal cadence
- adaptive communication
- low-friction interaction
```

### ใช้กับงานแบบไหน

```text
- human-agent interaction
- assistant response
- UI message
- gentle warning
- onboarding
- explanation layer
- communication buffer
```

### กลุ่มภาษา / tag ที่เหมาะ

| Tag Family | ตัวอย่าง | เหตุผล |
|---|---|---|
| `DOC:*` | `DOC:MD`, `DOC:TXT` | ข้อความอธิบาย / note / guide |
| `WEB:*` | `WEB:HTML`, `WEB:CSS`, `WEB:JS` | UI / PWA / display |
| `GEN:*` | `GEN:PY`, `GEN:JS` | สรุป / transform / assistant glue |
| `CONFIG:*` | `CONFIG:JSON` | response packet / UI config |

### ตัวอย่าง Modew

```text
MODEW:HUMAN_BRIDGE
MODEW:SOFT_REPORTER
MODEW:COMMUNICATION_BUFFER
MODEW:UI_TRANSLATOR
```

### ตัวอย่าง Cross-L

```text
CROSS-L:HUMAN_SAFE_REPORT
RYTM:R&B
LANG:markdown,json,javascript
BOUNDARY:readable_output
RETURN:state,reason,summary,mutated,review
```

---

# 6. Rytm → Language Tag Routing Table

ตารางนี้ใช้เป็นตัวช่วยจำเร็ว

| Rytm | งานเด่น | Tag หลัก | ภาษา/รูปแบบที่ควรมองก่อน |
|---|---|---|---|
| BALLAD | memory / continuity / reflection | `DOC:*`, `CONFIG:*`, `QUERY:*` | Markdown, TXT, JSON, YAML, SQL, Python |
| ROCK | patch / pressure / speed / conflict | `FAST:*`, `LOW:*`, `SCRIPT:*` | C++, Rust, C, Assembly, Bash, JSON, WASM |
| JAZZ | adaptive logic / experiment / AI collaboration | `SCRIPT:*`, `GEN:*`, `CONFIG:*` | Lua, Python, JSON, YAML, JavaScript, Markdown |
| STRING | long-form orchestration / semantic memory | `DOC:*`, `QUERY:*`, `FORMAL:*` | Markdown, YAML, SQL, SPARQL, Datalog, Lean, Python |
| EDM | loop / runtime / sync / stream | `SCRIPT:*`, `WEB:*`, `ENV:*` | Bash, Python, JavaScript, TypeScript, Go, Dockerfile, YAML |
| R&B | human-agent communication / UI / soft report | `DOC:*`, `WEB:*`, `GEN:*` | Markdown, TXT, HTML, CSS, JavaScript, Python, JSON |

---

# 7. Rytm → Modew Routing Table

| Rytm | Modew Style | Modew Should Do |
|---|---|---|
| BALLAD | Keeper / Reporter | เก็บความต่อเนื่อง สรุปแบบนุ่ม อ่านง่าย |
| ROCK | Fixer / Breaker | แก้ปัญหาแรง เร็ว เฉพาะจุด ระวัง boundary |
| JAZZ | Adapter / Player | ทดลอง logic ยืดหยุ่น ดึง context มาช่วย |
| STRING | Binder / Architect | เชื่อมเอกสาร ความหมาย ความจำระยะยาว |
| EDM | Runner / Synchronizer | ทำ loop, pulse, monitor, sync |
| R&B | Translator / Buffer | ทำข้อความให้มนุษย์เข้าใจ ลดแรงเสียดทาน |

---

# 8. Practical Flow Example

## 8.1 งานแก้ bug เร่งด่วน

```text
ERROR: memory pressure in native part
ENV: linux/mobile bridge
Rytm: ROCK
```

Cross-X ส่งให้ Modew:

```text
MODEW:FAST_PATCH
RYTM:ROCK
LANG_GROUP:FAST,LOW
CANDIDATE:CPP,RS,C,ASM,WASM
BOUNDARY:temp_patch
```

Cross-L block:

```text
CROSS-L:NATIVE_PRESSURE_PATCH
POINT:MODEW_ERROR_FIX
RYTM:ROCK
LANG:cpp,asm
BOUNDARY:temp_patch
DENY:truth_mutation,direct_merge
RETURN:state,reason,trace,mutated,review
```

ความหมาย:

```text
งานนี้ไม่ควรเริ่มจาก Markdown หรือ UI
ควรเริ่มจากสาย FAST/LOW เพราะจังหวะงานเป็น ROCK
```

---

## 8.2 งาน logic ชั่วคราวที่ยังไม่นิ่ง

```text
TASK: test adaptive rule
ENV: Termux / W3_API
Rytm: JAZZ
```

Modew:

```text
MODEW:RULE_TRIAL
RYTM:JAZZ
LANG_GROUP:SCRIPT,CONFIG
CANDIDATE:LUA,PY,JSON,YML
BOUNDARY:observe
```

Cross-L block:

```text
CROSS-L:ADAPTIVE_ENV_RULE
POINT:MODEW_CONDIEN_ENV
RYTM:JAZZ
LANG:lua,json
BOUNDARY:observe
READ:ENV,CONDIEN.LayerA
DENY:truth_mutation,file_write,network,merge
RETURN:state,reason,trace,mutated,review
```

ความหมาย:

```text
งานนี้ต้องด้นสดและปรับตาม context
Lua / Python / JSON rule จึงเหมาะกว่า C++ หรือ Assembly
```

---

## 8.3 งาน W3 Pulse / health loop

```text
TASK: W3 Pulse
ENV: PWA + W3_API
Rytm: EDM
```

Modew:

```text
MODEW:PULSE_RUNNER
RYTM:EDM
LANG_GROUP:SCRIPT,WEB,CONFIG
CANDIDATE:PY,JS,TS,JSON,BASH
BOUNDARY:observe_loop
```

Cross-L block:

```text
CROSS-L:W3_PULSE_SIGNAL
POINT:PWA_API_CROSS
RYTM:EDM
LANG:python,json,javascript
BOUNDARY:observe_only
DENY:truth_mutation,direct_merge
RETURN:state,reason,trace,mutated,review
```

ความหมาย:

```text
งานนี้เป็น loop / pulse / sync
จึงควรใช้กลุ่ม runtime + script + web + config
```

---

## 8.4 งานสรุปให้มนุษย์อ่าน

```text
TASK: explain API result
ENV: PWA / Chat / Report
Rytm: R&B
```

Modew:

```text
MODEW:SOFT_REPORTER
RYTM:R&B
LANG_GROUP:DOC,WEB,GEN
CANDIDATE:MD,TXT,HTML,JS,PY,JSON
BOUNDARY:readable_output
```

Cross-L block:

```text
CROSS-L:HUMAN_API_SUMMARY
POINT:RESULT_TO_HUMAN
RYTM:R&B
LANG:markdown,json
BOUNDARY:readable_output
READ:result,trace
DENY:truth_mutation,repo_write
RETURN:state,reason,summary,mutated,review
```

ความหมาย:

```text
งานนี้ไม่ใช่แก้ระบบ แต่ต้องแปลผลให้อ่านง่าย
จึงควรใช้ R&B มากกว่า ROCK
```

---

# 9. Suggested Routing Packet

รูปแบบ packet ขั้นต้นสำหรับส่งจาก Cross-X ไป Modew:

```json
{
  "source": "Cross-X",
  "target": "Modew",
  "intent": "select_language_group",
  "rytm": "JAZZ",
  "cross_point": "MODEW_CONDIEN_ENV",
  "task": "adaptive_rule_check",
  "env": "termux_mobile",
  "boundary": "observe",
  "candidate_tags": ["SCRIPT:*", "GEN:*", "CONFIG:*"],
  "candidate_languages": ["Lua", "Python", "JSON", "YAML"],
  "return_contract": ["state", "reason", "trace", "mutated", "review"]
}
```

---

# 10. Minimal W3Lgu Form

รูปแบบย่อแบบ W3Lgu:

```text
MEM:SOURCE:Cross-X,ENV:termux_mobile
PATCH:RYTM:JAZZ,LANG_GROUP:SCRIPT,GEN,CONFIG
LAW:BOUNDARY:observe,DENY:truth_mutation,merge
EVENT:MODEW:ADAPTIVE_CHECK,TASK:adaptive_rule_check
SIGNAL:RETURN:state,reason,trace,mutated,review
```

---

# 11. Safety Laws

## 11.1 Rytm is not authority

```text
Rytm ช่วยเลือกทางเริ่มต้น
แต่ไม่ใช่คำตัดสินสูงสุด
```

Modew ยังต้องดู:

```text
- Paper
- Condien
- ENV
- Boundary
- Return Contract
- Human Review Policy
```

---

## 11.2 ROCK does not mean unsafe

`ROCK` แปลว่างานมีแรงกดหรือความเร่ง

ไม่ได้แปลว่าอนุญาตให้แก้ truth ได้

ยังต้องมี:

```text
DENY:truth_mutation,direct_merge
RETURN:state,reason,trace,mutated,review
```

---

## 11.3 JAZZ does not mean random

`JAZZ` แปลว่ายืดหยุ่นและ adaptive

ไม่ได้แปลว่าทำอะไรก็ได้

ต้องมี:

```text
BOUNDARY
READ
DENY
RETURN
```

---

## 11.4 EDM loop must not become runaway

งาน `EDM` มักเป็น loop / runtime / sync

ต้องระวัง:

```text
- infinite loop
- repeated API call
- battery drain
- log flood
- network pressure
```

ควรมี:

```text
LIMIT
INTERVAL
STOP_CONDITION
REVIEW_ON_ERROR
```

---

## 11.5 R&B must not hide risk

`R&B` ทำให้ข้อความนุ่มและอ่านง่าย

แต่ห้ามทำให้ error ดูไม่สำคัญ

ถ้ามี risk ต้องยังแสดง:

```text
state
reason
risk
next_step
```

---

# 12. Decision Rule แบบสั้น

ถ้าจำไม่ได้ ให้ใช้กฎนี้:

```text
งานหนัก / เร็ว / bug / patch        → ROCK
งานยืดหยุ่น / logic / ทดลอง         → JAZZ
งาน loop / sync / runtime            → EDM
งาน memory / continuity / reflection → BALLAD
งานมนุษย์อ่าน / UI / สื่อสารนุ่ม     → R&B
งานเอกสารยาว / ความหมายหลายชั้น      → STRING
```

---

# 13. Cross-L Tag Selection Shortcut

```text
ROCK   → FAST / LOW / SCRIPT
JAZZ   → SCRIPT / GEN / CONFIG
EDM    → SCRIPT / WEB / ENV / CONFIG
BALLAD → DOC / CONFIG / QUERY
R&B    → DOC / WEB / GEN
STRING → DOC / QUERY / FORMAL / CONFIG
```

---

# 14. Modew Selection Shortcut

```text
ROCK   → Fixer
JAZZ   → Adapter
EDM    → Runner
BALLAD → Keeper
R&B    → Translator
STRING → Binder
```

---

# 15. Relation to CROSS_L_LANGUAGE_TAG_TABLE

ไฟล์นี้ต้องใช้ร่วมกับ:

```text
croll/CROSS_L_LANGUAGE_TAG_TABLE.md
```

ไฟล์ `CROSS_L_LANGUAGE_TAG_TABLE.md` บอกว่า:

```text
ภาษาอะไรอยู่กลุ่มไหน
มี tag อะไร
ใช้ทำอะไร
```

ไฟล์นี้บอกว่า:

```text
จังหวะงานแบบไหน
ควรเลือกกลุ่มภาษาแบบไหน
และ Modew ควรเริ่มจากบทบาทใด
```

ดังนั้นสองไฟล์ทำงานคู่กัน:

```text
Rytm Routing Guide
→ เลือกกลุ่ม tag
→ เปิด Language Tag Table
→ เลือกภาษาจริง
→ สร้าง Cross-L block
```

---

# 16. Recommended Use in W3 Flow

สำหรับงานจริงให้วาง flow แบบนี้:

```text
1. Paper ระบุเป้าหมายงาน
2. Cross-X ระบุ cross point
3. Rytm ระบุจังหวะงาน
4. Modew เลือก style การทำงาน
5. เปิด Language Tag Table เพื่อเลือกภาษา
6. สร้าง Cross-L block
7. CrossCode ทำงานใน boundary
8. คืน return contract
9. EP_SIGNAL / Rytm ทำ preview signal
10. LRC2 บันทึก
```

---

# 17. Final Statement

Rytm ไม่ได้มีไว้ทำให้สัญญาณดูสวย

Rytm มีไว้ให้ระบบเข้าใจ “จังหวะของงาน”

เมื่อ Cross-X รู้จังหวะของงาน
Modew จะเลือกเครื่องมือได้ถูกขึ้น
Cross-L จะประกาศ boundary ได้ชัดขึ้น
และ MPCP จะรับคืนค่าได้เป็นระบบมากขึ้น

```text
EP_SIGNAL gives structure.
Rytm gives movement.
Cross-X finds the cross point.
Modew chooses the work style.
Cross-L governs the fragment.
MPCP receives the governed result.
LRC2 remembers the trace.
```

END
