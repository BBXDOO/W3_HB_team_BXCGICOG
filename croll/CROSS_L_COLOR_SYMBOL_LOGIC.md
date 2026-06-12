# Cross-L Color & Symbol Logic Scaffold

**Document Path:** `croll/CROSS_L_COLOR_SYMBOL_LOGIC.md`  
**Status:** ACTIVE DRAFT / SCAFFOLD  
**System Relation:** W3 / CROLL / Cross-L / CrossLgu / EP_SIGNAL / Rytm / PRX / Cross-X / Modew / MPCP / LRC2  
**Owner:** BBX19  
**Purpose:** โครงเอกสารสำหรับอธิบายการใช้ `สี` และ `สัญลักษณ์` มาช่วยจัดโครงสร้างงานของ Cross-L เพื่อกันลืมและใช้วาง flow ต่อ

---

# 1. Core Statement

Cross-L ไม่ได้ใช้แค่ภาษา / สคริปต์ / config ในการจัดงาน

Cross-L สามารถใช้สัญญาณร่วมหลายชั้นเพื่ออ่านงานให้ชัดขึ้น:

```text
Rytm   = จังหวะงาน
Color  = สถานะ / ความเสี่ยง / อุณหภูมิงาน
Symbol = รูปทรง / ประเภท / ลักษณะการจัดวาง
Tag    = กลุ่มภาษา / เครื่องมือ
Modew  = หน่วยปฏิบัติงาน
```

ประโยคจำง่าย:

```text
Rytm tells how the work moves.
Color tells how the work feels/statuses.
Symbol tells what shape the work takes.
Tag tells what tool group to use.
Modew does the work.
Cross-L governs the fragment.
```

แบบไทย:

```text
Rytm = งานเคลื่อนแบบไหน
Color = งานอยู่สถานะไหน
Symbol = งานมีรูปทรงแบบไหน
Tag = ควรใช้เครื่องมือกลุ่มไหน
Modew = ใครลงมือทำ
Cross-L = กติกาครอบงาน
```

---

# 2. Why Color and Symbol Matter

ในงานจริง บางครั้งการอ่านจากภาษาอย่างเดียวไม่พอ

ตัวอย่าง:

```text
งานเดียวกันอาจใช้ Python ได้
แต่ถ้าเป็นสีแดง แปลว่าต้องระวัง
ถ้าเป็นสัญลักษณ์ ▲ แปลว่าเป็นงานแรง/เสี่ยง/ต้องยกขึ้นตรวจ
ถ้า Rytm เป็น ROCK แปลว่ามีแรงกดและต้องแก้เฉพาะจุด
```

ดังนั้น Cross-L ควรอ่านงานจากชุดสัญญาณร่วม:

```text
Rytm + Color + Symbol + Tag + Boundary
```

ไม่ใช่แค่:

```text
LANG:python
```

---

# 3. Layer Relationship

```text
EP_SIGNAL
→ Rytm
→ Color / Symbol
→ Cross-X
→ Modew
→ Cross-L / CrossCode
→ MPCP
→ LRC2
```

อธิบาย:

```text
1. EP_SIGNAL ให้โครงสร้างสัญญาณ
2. Rytm อ่านจังหวะของงาน
3. Color บอกสถานะ / ความเสี่ยง / ระดับแรงกด
4. Symbol บอกรูปทรงของงาน
5. Cross-X ระบุจุดตัด
6. Modew เลือกวิธีทำงาน
7. Cross-L ครอบภาษา / fragment / boundary
8. MPCP รับผลลัพธ์กลับเข้าระบบ
9. LRC2 บันทึก trace และ memory
```

---

# 4. Color Logic

> หมายเหตุ: ตารางนี้เป็น scaffold เริ่มต้น สามารถปรับตาม W3 spec ภายหลังได้

| Color | Meaning | Work Signal | Modew Behavior |
|---|---|---|---|
| RED | เสี่ยง / แรง / ต้องระวัง | error, pressure, conflict, mutation risk | หยุดคิดก่อน ลงมือแบบมี boundary, คืน review/block ได้ |
| YELLOW | ยังไม่นิ่ง / ต้องตรวจ | uncertainty, draft, missing context | ทดลองใน observe mode, ขอ context เพิ่ม, คืน review |
| GREEN | ผ่าน / ปลอดภัยระดับหนึ่ง | stable, pass, ready, low risk | ทำงานต่อได้ แต่ยัง log trace |
| BLUE | ข้อมูล / สัญญาณ / flow | signal, sync, trace, runtime, memory | ส่งต่อ / monitor / log / sync |
| WHITE | กลาง / ยังไม่จัดประเภท | neutral, blank, unclassified | จัดประเภทก่อน ไม่ควร execute ทันที |
| BLACK | ปิด / ห้าม / unknown critical | denied, blocked, hidden danger | block, escalate, require review |
| PURPLE | ความหมายลึก / semantic / philosophy | meaning, relation, high context | ส่งเข้า Binder/Keeper, ไม่รีบตัดสิน |
| ORANGE | warning + active | unstable but actionable | ทำแบบ staged / limited action |

---

# 5. Basic Symbol Logic

> หมายเหตุ: ใช้เป็นโครงก่อน อ้างอิงกับ PRX/W3 symbol logic ภายหลังได้

| Symbol | Name | Meaning | Use Case |
|---|---|---|---|
| ▲ | Triangle | แรงกด / ยกขึ้นตรวจ / จุดเสี่ยง | bug, conflict, urgent patch, warning |
| ● | Circle | วงจร / loop / continuity / pulse | runtime loop, sync, monitoring, memory pulse |
| ■ | Square | โครงสร้าง / stable block / container | config, schema, storage, stable unit |
| ◆ | Diamond | decision / cross point / adaptive interpretation | 0.5 decision, routing, review, flexible logic |
| ✚ | Cross | จุดตัด / รวมหลายปัจจัย | Cross-X, Cross-L, Modew+Condien+Paper |
| / | Slash | split / boundary / context relation | A/B relation, boundary crossing |
| ! | Alert | impact / danger / negative force | risk, error, mutation warning |
| ? | Question | missing context / uncertainty | ask review, request context |
| ✓ | Check | accepted / completed / pass | pass state, accepted packet |
| × | Block | reject / denied / unsafe | block, deny, stop |

---

# 6. Color + Symbol Combined Meaning

การใช้สีและสัญลักษณ์ร่วมกันทำให้สัญญาณชัดขึ้น

| Combination | Meaning | Suggested Action |
|---|---|---|
| RED + ▲ | เสี่ยงสูง / มีแรงกด / ต้องหยุดตรวจ | Modew:Fixer, boundary:temp/review, no truth mutation |
| RED + ! | error impact / อันตรายชัด | block หรือ review ทันที |
| YELLOW + ◆ | ยังไม่นิ่ง / ต้องตัดสินใจแบบ 0.5 | Modew:Adapter, observe mode |
| YELLOW + ? | context ไม่พอ | ขอข้อมูลเพิ่ม / review |
| GREEN + ■ | stable container / พร้อมเก็บ | Modew:Keeper, record/store |
| GREEN + ✓ | ผ่าน / accepted | ส่งต่อ MPCP / log LRC2 |
| BLUE + ● | pulse / sync / runtime loop | Modew:Runner, monitor, limit loop |
| BLUE + ◆ | signal routing / adaptive signal | Cross-X route, Modew select |
| PURPLE + ◆ | semantic decision / ความหมายลึก | Modew:Binder, relation mapping |
| BLACK + × | deny / unsafe / ห้ามทำ | block, escalate |
| WHITE + ? | ยังไม่จัดประเภท | classify ก่อน |
| ORANGE + ▲ | warning but actionable | staged action, limited run |

---

# 7. Relation with Rytm

สีและสัญลักษณ์ไม่ได้แทน Rytm แต่ช่วยเสริม Rytm

```text
Rytm = จังหวะงาน
Color = สถานะงาน
Symbol = รูปทรงงาน
```

ตัวอย่าง:

```text
ROCK + RED + ▲
= งานเร่ง แรง เสี่ยงสูง ต้องแก้เฉพาะจุดแบบมี boundary
```

```text
JAZZ + YELLOW + ◆
= งานยืดหยุ่น ยังไม่นิ่ง ต้องทดลองใน observe mode
```

```text
EDM + BLUE + ●
= งาน loop/sync/pulse ให้ runner ทำแบบมี limit
```

```text
BALLAD + GREEN + ■
= งาน memory/continuity พร้อมเก็บเป็น block
```

```text
R&B + BLUE + ●
= งานสื่อสารกับมนุษย์ผ่าน flow นุ่ม ๆ / UI / assistant response
```

```text
STRING + PURPLE + ◆
= งานความหมายหลายชั้น ต้อง map relation / semantic decision
```

---

# 8. Routing Logic Scaffold

## 8.1 Input Packet

```json
{
  "source": "Cross-X",
  "target": "Modew",
  "intent": "route_by_signal_shape",
  "rytm": "JAZZ",
  "color": "YELLOW",
  "symbol": "◆",
  "task": "adaptive_rule_check",
  "boundary": "observe",
  "allow_mutation": false
}
```

## 8.2 Expected Interpretation

```json
{
  "state": "review",
  "reason": "adaptive_uncertain_decision_point",
  "modew_style": "Adapter",
  "candidate_tags": ["SCRIPT:*", "GEN:*", "CONFIG:*"],
  "boundary": "observe",
  "mutated": false,
  "review": true
}
```

---

# 9. W3Lgu Minimal Form

```text
MEM:SOURCE:Cross-X,ENV:termux_mobile
PATCH:RYTM:JAZZ,COLOR:YELLOW,SYM:◆
LAW:BOUNDARY:observe,DENY:truth_mutation,merge
EVENT:MODEW:ADAPTIVE_CHECK,TASK:adaptive_rule_check
SIGNAL:STATE:review,REASON:adaptive_uncertain_decision_point
```

---

# 10. Example Cases

## 10.1 ROCK + RED + ▲

### Situation

```text
มี bug แรงใน native component
ต้องแก้เร็ว แต่ห้าม merge เอง
```

### Interpretation

```text
RYTM:ROCK
COLOR:RED
SYMBOL:▲
```

### Meaning

```text
- งานเร่ง
- มีความเสี่ยงสูง
- ต้องแก้เฉพาะจุด
- ต้องมี review
```

### Suggested Modew

```text
MODEW:FAST_PATCH
STYLE:Fixer
```

### Suggested Tags

```text
FAST:*
LOW:*
SCRIPT:*
CONFIG:*
```

### Suggested Cross-L Boundary

```text
BOUNDARY:temp_patch
DENY:truth_mutation,direct_merge
RETURN:state,reason,trace,mutated,review
```

---

## 10.2 JAZZ + YELLOW + ◆

### Situation

```text
logic ยังไม่นิ่ง ต้องทดลอง rule ชั่วคราว
```

### Interpretation

```text
RYTM:JAZZ
COLOR:YELLOW
SYMBOL:◆
```

### Meaning

```text
- งานยืดหยุ่น
- ยังไม่ควร commit
- ต้องใช้ decision 0.5 / review
```

### Suggested Modew

```text
MODEW:ADAPTIVE_CHECK
STYLE:Adapter
```

### Suggested Tags

```text
SCRIPT:*
GEN:*
CONFIG:*
DOC:*
```

---

## 10.3 EDM + BLUE + ●

### Situation

```text
W3 Pulse หรือ monitor loop
```

### Interpretation

```text
RYTM:EDM
COLOR:BLUE
SYMBOL:●
```

### Meaning

```text
- งานเป็น loop / pulse
- เกี่ยวกับ signal / runtime
- ต้องมี limit เพื่อกัน runaway
```

### Suggested Modew

```text
MODEW:PULSE_RUNNER
STYLE:Runner
```

### Required Safety

```text
LIMIT
INTERVAL
STOP_CONDITION
REVIEW_ON_ERROR
```

---

## 10.4 BALLAD + GREEN + ■

### Situation

```text
งานบันทึกความต่อเนื่อง / note / memory
```

### Interpretation

```text
RYTM:BALLAD
COLOR:GREEN
SYMBOL:■
```

### Meaning

```text
- งานค่อนข้างปลอดภัย
- เหมาะกับการเก็บเป็น block
- ใช้กับ docs / memory / knowledge
```

### Suggested Modew

```text
MODEW:MEMORY_KEEPER
STYLE:Keeper
```

---

## 10.5 R&B + BLUE + ●

### Situation

```text
ต้องแปลงผลลัพธ์เทคนิคให้มนุษย์อ่านง่ายบน PWA
```

### Interpretation

```text
RYTM:R&B
COLOR:BLUE
SYMBOL:●
```

### Meaning

```text
- เป็นงานสื่อสาร
- ต้อง flow นุ่ม
- ยังต้องแสดง risk ตามจริง
```

### Suggested Modew

```text
MODEW:SOFT_REPORTER
STYLE:Translator
```

### Safety

```text
ห้ามซ่อน error
ห้ามทำให้ risk ดูไม่สำคัญ
```

---

## 10.6 STRING + PURPLE + ◆

### Situation

```text
ต้องเชื่อมเอกสารหลายชุดให้เป็น relation map
```

### Interpretation

```text
RYTM:STRING
COLOR:PURPLE
SYMBOL:◆
```

### Meaning

```text
- ความหมายหลายชั้น
- ต้องตัดสิน relation
- ต้องใช้ Binder / Knowledge Mapper
```

### Suggested Modew

```text
MODEW:RELATION_MAPPER
STYLE:Binder
```

---

# 11. Decision Shortcut

จำแบบเร็ว:

```text
RED     = ระวัง / เสี่ยง / แรง
YELLOW  = ยังไม่นิ่ง / ต้อง review
GREEN   = ผ่าน / พร้อมเก็บ
BLUE    = signal / flow / runtime
PURPLE  = meaning / semantic / relation
BLACK   = deny / block
WHITE   = ยังไม่จัดประเภท
ORANGE  = warning แต่ทำแบบจำกัดได้
```

```text
▲ = pressure / risk / urgent
● = loop / pulse / continuity
■ = structure / container / stable block
◆ = decision / cross point / adaptive logic
✚ = cross point / merge factors
! = impact / danger
? = missing context
✓ = accepted
× = blocked
```

---

# 12. Cross-L Color Symbol Packet

รูปแบบ packet ขั้นต้น:

```json
{
  "source": "Cross-X",
  "target": "Modew",
  "intent": "select_work_shape",
  "rytm": "ROCK",
  "color": "RED",
  "symbol": "▲",
  "boundary": "temp_patch",
  "candidate_tags": ["FAST:*", "LOW:*"],
  "deny": ["truth_mutation", "direct_merge"],
  "return_contract": ["state", "reason", "trace", "mutated", "review"]
}
```

---

# 13. Safety Laws

## 13.1 Color is not final authority

```text
สีช่วยบอกสถานะ แต่ไม่ใช่คำตัดสินสูงสุด
```

ต้องดู:

```text
Paper
Condien
ENV
Boundary
Return Contract
Human Review
```

---

## 13.2 Symbol is not execution permission

```text
สัญลักษณ์บอกรูปทรงงาน
แต่ไม่ได้แปลว่าอนุญาตให้ execute ทันที
```

เช่น:

```text
GREEN + ■
```

แปลว่า stable block แต่ยังต้องดู boundary ก่อน write/store

---

## 13.3 RED must not auto-fix truth

```text
RED แปลว่าระวัง
ไม่ใช่ให้แก้อัตโนมัติ
```

ถ้า RED + ROCK + ▲:

```text
return review/block first
no direct merge
no truth mutation
```

---

## 13.4 BLUE loop must be limited

ถ้า BLUE + ● หรือ EDM + BLUE + ●:

```text
ต้องมี LIMIT / INTERVAL / STOP_CONDITION
```

---

## 13.5 R&B must not hide risk

ถ้าใช้ R&B เพื่อให้ข้อความอ่านง่าย:

```text
ต้องยังแสดง risk / next step / reason
```

---

# 14. Relation to Existing CROLL Documents

ใช้ร่วมกับ:

```text
croll/README.md
croll/test.md
croll/CROSS_L_LANGUAGE_TAG_TABLE.md
croll/CROSS_L_RYTM_MODEW_ROUTING.md
croll/CROSS_L_RYTM_TEST_CASES.md
```

บทบาทแต่ละไฟล์:

```text
README.md
= นิยาม Cross-L / CrossLgu / CrossCode

test.md
= แนวทางทดสอบ Cross-L fragment

CROSS_L_LANGUAGE_TAG_TABLE.md
= ตารางภาษา / tag / type

CROSS_L_RYTM_MODEW_ROUTING.md
= Rytm เลือกกลุ่มงาน / Modew style

CROSS_L_RYTM_TEST_CASES.md
= testcase ตามแนว Rytm

CROSS_L_COLOR_SYMBOL_LOGIC.md
= สี + สัญลักษณ์ ช่วยอ่านสถานะและรูปทรงงาน
```

---

# 15. Recommended Full Routing Order

ลำดับที่แนะนำเวลางานเข้ามา:

```text
1. อ่าน Paper / Brief
2. ระบุ Cross Point ด้วย Cross-X
3. อ่าน Rytm เพื่อดูจังหวะงาน
4. อ่าน Color เพื่อดูสถานะ/ความเสี่ยง
5. อ่าน Symbol เพื่อดูรูปทรงงาน
6. เลือก Modew style
7. เลือก Tag Family
8. เลือกภาษาใน Language Tag Table
9. สร้าง Cross-L block
10. ตรวจ boundary / deny / return contract
11. Run หรือ Preview ตามสิทธิ์
12. คืนผลเข้า MPCP
13. LRC2 บันทึก trace
```

---

# 16. Final Statement

สีและสัญลักษณ์ใน Cross-L ไม่ได้มีไว้ตกแต่ง

มันคือเครื่องมือช่วยอ่านงาน

```text
Color tells status.
Symbol tells shape.
Rytm tells movement.
Tag tells tool family.
Modew performs.
Cross-L governs.
```

แบบไทย:

```text
สีบอกสถานะ
สัญลักษณ์บอกรูปทรง
จังหวะบอกการเคลื่อน
แท็กบอกกลุ่มเครื่องมือ
Modew เป็นผู้ลงมือ
Cross-L เป็นกติกาครอบงาน
```

END
