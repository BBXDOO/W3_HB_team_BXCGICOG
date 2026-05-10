# W3Lgu-Condien Profile

## 1. Purpose
เอกสารนี้กำหนด W3Lgu profile สำหรับ `Condien` เพื่อให้ Condien สามารถ:
- ถูกประกาศ (declare)
- ถูก bind เข้ากับ Modew และ Paper
- ถูก inspect และ trace
- ถูกสื่อสารข้าม layer/runtime
- ถูกส่งต่อในรูปแบบที่ subsystem อื่นอ่านได้

โดยยังคงหลักสำคัญว่า:

> Condien ไม่ใช่ syntax อย่างเดียว  
> แต่ต้องสามารถ represent ผ่าน W3Lgu ได้

---

## 2. Position of Condien
Condien ในระบบ mpcp คือ:
- adaptive meaning/state/context layer
- value/object/context carrier
- continuity-supporting layer
- layer-aware meaning support

ดังนั้น profile นี้จึงมีไว้เพื่อ represent:
- บทบาทของ Condien
- ขอบเขตของ Condien
- layer access
- continuity/rebase
- binding กับ Modew/Paper
- inspection state

---

## 3. Core Rule
W3Lgu-Condien profile มีหน้าที่ “สื่อสารและ bind Condien”  
ไม่ใช่ “แทน ontology ทั้งหมดของ Condien”

กล่าวคือ:
- profile นี้ใช้เป็นภาษากลางของ Condien
- แต่ไม่ควรทำให้คนเข้าใจว่า Condien มีอยู่แค่เท่าที่ field พูดถึง
- ความหมายเชิงระบบของ Condien ยังอยู่ใน design/model ของ Condien เอง

---

## 4. Core Field Groups

### 4.1 Identity / Role
- `CONDIEN`
- `ROLE`
- `POSITION`

### 4.2 Meaning / Context
- `MEANING_MODE`
- `CONTEXT_MODE`
- `ADAPT_SCOPE`

### 4.3 Layer / Access
- `LAYER`
- `LAYERS`
- `READ`
- `DENY`

### 4.4 Continuity / Rebase
- `CONTINUITY`
- `REBASE`
- `TRACE_LINK`

### 4.5 Governance / Boundary
- `BOUNDARY`
- `ENV`

### 4.6 Binding
- `MODEW`
- `PAPER`

---

## 5. Declaration Example
ตัวอย่างการประกาศ Condien เชิง profile:

```text
CONDIEN:CORE
ROLE:meaning_state_layer
POSITION:intra_modew
MEANING_MODE:bounded-adaptive
CONTEXT_MODE:dynamic
ADAPT_SCOPE:paper-bound,layer-bound
LAYERS:A,B,C,D,E
CONTINUITY:carry-forward
REBASE:bounded
BOUNDARY:rot-governed
ENV:preserve
```

ความหมาย:
- ประกาศ Condien ชื่อ `CORE`
- มีบทบาทเป็น meaning/state layer
- ทำงานในตำแหน่ง intra-modew
- adaptation ทำได้แต่ต้อง bounded
- context เป็นแบบ dynamic
- รองรับหลาย layer
- continuity แบบ carry-forward
- rebase ได้แบบ bounded
- อยู่ใต้ ROT boundary
- ต้อง preserve environment

---

## 6. Binding Example
ตัวอย่างการ bind Condien กับ Modew/Paper:

```text
MODEW:REPORT
CONDIEN:CORE
PAPER:daily_summary
READ:LAYER_B,LAYER_C
DENY:LAYER_D
TRACE_LINK:required
BOUNDARY:paper-strict
```

ความหมาย:
- Modew `REPORT` ใช้ Condien `CORE`
- ทำงานภายใต้ paper `daily_summary`
- อ่าน layer B และ C ได้
- ห้ามอ่าน D
- trace link ต้องมี
- boundary ในรอบนี้ strict ตาม paper

---

## 7. Inspection Example
ตัวอย่าง inspection/readability view:

```text
TIME:now,CONDIEN:CORE,LAYER:LAYER_B,STATE:active,TRACE:linked
```

inspection ใช้เพื่อ:
- มองสถานะเร็ว
- ดู layer ที่ active
- ดูสถานะ trace
- ไม่ใช่ truth replacement ของ result/governance

---

## 8. Rules
1. Condien representation ต้องไม่ข้าม ROT/Paper boundary
2. Layer access ต้อง explicit
3. Continuity/Rebase ต้อง explicit
4. Inspection = visibility, not truth override
5. W3Lgu-Condien profile ใช้กับ declaration, binding, inspection, และ controlled exchange
6. ห้ามใช้ profile นี้เพื่อ derive ความจริงย้อนหลังจาก result
7. ห้ามลด Condien ให้เหลือ plain storage syntax

---

## 9. Final Summary
W3Lgu-Condien profile เป็นภาษากลางสำหรับประกาศ bind และ inspect Condien  
โดยมีเป้าหมายเพื่อให้ Condien เชื่อมกับ subsystem อื่นได้  
แต่ยังรักษาสถานะของ Condien ในฐานะ meaning/state/context layer ไว้ครบ
