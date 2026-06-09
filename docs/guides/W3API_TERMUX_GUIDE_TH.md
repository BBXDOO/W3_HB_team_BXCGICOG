# คู่มือใช้งาน W3-API ผ่าน Termux

**Path:** `docs/guides/W3API_TERMUX_GUIDE_TH.md`  
**Status:** Active Draft / คู่มือเบื้องต้น  
**Worker:** Cast  
**Paired Worker:** ChatGPT  
**Related Issue:** #242  
**Scope:** ใช้งาน `tools/w3api.py` และ `/w3/cross` แบบ gateway / report / review

---

# 1. จุดประสงค์

คู่มือนี้อธิบายวิธีใช้ Termux เพื่อเรียก W3-API ผ่านไฟล์:

```text
tools/w3api.py
```

เป้าหมายคือให้ผู้ใช้สามารถ:

- เปิด gateway หรือ server ที่รองรับ `/w3/cross`
- ตรวจ health
- ส่ง brief เข้า W3-API
- เปลี่ยน target / focus / mode
- อ่านผลลัพธ์เบื้องต้น
- ใช้เป็นทางเข้าของ workflow แบบ Issue / Worker / Report ต่อไป

---

# 2. ภาพรวมแบบง่าย

```text
Termux
→ tools/w3api.py หรือ curl
→ W3-API Gateway
→ /w3/cross
→ runtime engine
→ module ที่รับผิดชอบ
→ memory / report / signal
→ ผลลัพธ์กลับมา
```

ความหมายแบบบ้าน W3:

```text
Termux = มือถือ/พื้นที่สั่งงาน
W3-API = หน้าประตู
engine = โต๊ะรับงาน / คนจัดคิว
module = คนทำงานเฉพาะทาง
memory = สมุดบันทึกกลาง
output = รายงานกลับ
```

---

# 3. เข้าโฟลเดอร์ repo

ตัวอย่าง:

```bash
cd ~/W3_HB_team_BXCGICOG
```

ตรวจว่าอยู่ใน repo:

```bash
pwd
ls
```

ควรเห็นไฟล์หรือโฟลเดอร์ เช่น:

```text
README.md
core/
tools/
docs/
w3_api/
```

---

# 4. เปิด Gateway / Server

ถ้ามีไฟล์ simple gateway ในเครื่อง ให้เปิดตามคำสั่งที่ระบบแจ้งไว้ เช่น:

```bash
python W3_API_SERVER_SIMPLE.py
```

หรือถ้าใช้ FastAPI app:

```bash
uvicorn w3_api.main:app --host 127.0.0.1 --port 8000
```

> หมายเหตุ: ชื่อ server อาจต่างกันตามเวอร์ชันของ repo/branch ที่ใช้งานจริง ให้ใช้ไฟล์ gateway ที่มีอยู่ในเครื่องเป็นหลัก

เมื่อ server ทำงาน ควรเปิดค้างไว้ใน session หนึ่ง แล้วใช้ session อื่นส่งคำสั่งผ่าน Termux

---

# 5. ตรวจ Health

ใช้ helper:

```bash
python tools/w3api.py health
```

หรือใช้ curl:

```bash
curl http://127.0.0.1:8000/health
```

ถ้าพร้อมใช้งาน ควรได้ผลลัพธ์ลักษณะ JSON หรือข้อความที่บอกว่า server online

ถ้า error ให้ตรวจว่า:

```text
- server เปิดอยู่หรือไม่
- port ใช่ 8000 หรือไม่
- path /health มีใน server เวอร์ชันนั้นหรือไม่
```

---

# 6. ส่ง Brief แบบง่ายด้วย tools/w3api.py

รูปแบบพื้นฐาน:

```bash
python tools/w3api.py <intent> <target> <focus>
```

ตัวอย่าง:

```bash
python tools/w3api.py review REDR memory
```

ความหมาย:

```text
intent = review
 target = REDR
 focus  = memory
```

แปลแบบ W3:

```text
ขอให้ระบบ review โมดูล REDR โดยโฟกัสเรื่อง memory
```

---

# 7. ตัวอย่างคำสั่งที่ใช้บ่อย

## 7.1 รีวิว REDR เรื่อง memory

```bash
python tools/w3api.py review REDR memory
```

ใช้เมื่อต้องการดูว่า REDR มีประวัติ/ความจำ/แนวโน้มอย่างไร

## 7.2 รีวิว DTML เรื่อง law

```bash
python tools/w3api.py review DTML law
```

ใช้เมื่อต้องการดูด้านกฎ การตัดสิน และ boundary

## 7.3 รีวิว W3 ทั้งระบบ

```bash
python tools/w3api.py review W3 system
```

ใช้เมื่อต้องการดูภาพรวม cross-system health

## 7.4 ออกแบบ W3 แบบทั่วไป

```bash
python tools/w3api.py design W3 general
```

ใช้เมื่อ brief เป็นงานออกแบบ/แนวคิด

---

# 8. ส่ง Brief ด้วย curl

ถ้าต้องการส่ง JSON เอง:

```bash
curl -X POST http://127.0.0.1:8000/w3/cross \
  -H "Content-Type: application/json" \
  -d '{"source":"BBX19","intent":"review","target":"REDR","focus":"memory","mode":"cross"}'
```

ตัวอย่างเปลี่ยน target:

```bash
curl -X POST http://127.0.0.1:8000/w3/cross \
  -H "Content-Type: application/json" \
  -d '{"source":"BBX19","intent":"review","target":"DTML","focus":"law","mode":"cross"}'
```

ตัวอย่าง review ระบบ:

```bash
curl -X POST http://127.0.0.1:8000/w3/cross \
  -H "Content-Type: application/json" \
  -d '{"source":"BBX19","intent":"review","target":"W3","focus":"system","mode":"cross"}'
```

---

# 9. การเปลี่ยน Section / Target / Focus

ให้คิดแบบนี้:

```text
intent = งานที่ต้องการให้ทำ
 target = โมดูลหรือพื้นที่ที่จะดู
 focus  = หัวข้อย่อยที่อยากเน้น
 mode   = รูปแบบการทำงาน
```

ตัวอย่าง mapping:

| ต้องการ | intent | target | focus |
|---|---|---|---|
| ตรวจ REDR เรื่องความจำ | review | REDR | memory |
| ตรวจ REDR เรื่องความเสี่ยง | review | REDR | risk |
| ตรวจ DTML เรื่องกฎ | review | DTML | law |
| ตรวจ PSP2 เรื่อง route | review | PSP2 | route |
| ตรวจ W3 ทั้งระบบ | review | W3 | system |
| ให้ออกแบบ flow | design | W3 | flow |
| ให้ดูสัญญาณ | review | W3 | signal |

---

# 10. วิธีอ่านผลลัพธ์

ผลลัพธ์มักมีส่วนสำคัญ เช่น:

```text
id
status
cross
runtime
w3lgu
signal
```

## 10.1 status

```text
accepted / SUCCESS = รับงานและทำงานได้
FAILED = งานพังหรือ route ไม่สำเร็จ
```

## 10.2 runtime.module

บอกว่าโมดูลไหนทำงาน เช่น:

```text
LRC2
REDR
DTML
ChatGPT
Cast
```

## 10.3 runtime.output

คือรายงานหลักที่ต้องอ่าน

ตัวอย่างอาจมี:

```text
health=HEALTHY
confidence=HIGH
trend=FORMING
memory total=...
experience=...
```

## 10.4 mutated:false

สำคัญมาก

```text
mutated:false = ตรวจ/รายงาน แต่ยังไม่แก้ truth หรือไฟล์จริง
```

## 10.5 gateway:true

หมายความว่างานเข้ามาผ่าน gateway

```text
gateway:true = งานนี้มาจาก W3-API gateway
```

---

# 11. ตัวอย่างการอ่าน output แบบง่าย

ถ้าได้ผลแบบนี้:

```text
module: LRC2
task: review
health: HEALTHY
confidence: HIGH
trend: FORMING
memory: 9
```

ให้อ่านว่า:

```text
ระบบส่งงาน review ไปให้ LRC2
LRC2 ตรวจจากความจำและประวัติ
สถานะสุขภาพดี
ความมั่นใจสูง
แนวโน้มกำลังก่อตัว
มี record memory ที่เกี่ยวข้อง 9 รายการ
```

---

# 12. การส่ง Brief แบบ W3

เวลาจะส่งงาน ให้คิดเป็น 5 ช่อง:

```text
source = ใครส่ง
intent = ต้องการทำอะไร
target = ให้ดูอะไร
focus  = เน้นเรื่องอะไร
mode   = ทำในโหมดไหน
```

ตัวอย่าง:

```json
{
  "source": "BBX19",
  "intent": "review",
  "target": "REDR",
  "focus": "memory",
  "mode": "cross"
}
```

---

# 13. ตัวอย่าง Brief สำหรับงานเอกสาร

ถ้าจะให้ระบบดูเอกสารในอนาคต อาจใช้รูปแบบนี้:

```json
{
  "source": "BBX19",
  "intent": "document",
  "target": "docs/guides/W3API_TERMUX_GUIDE_TH.md",
  "focus": "guide",
  "mode": "cross"
}
```

หรือ:

```json
{
  "source": "BBX19",
  "intent": "review",
  "target": "docs",
  "focus": "manifesto",
  "mode": "cross"
}
```

> หมายเหตุ: การอ่านไฟล์ repo จริงขึ้นอยู่กับ gateway/runtime ว่ามี repo reader แล้วหรือไม่ ถ้าไม่มี ระบบอาจ review จาก memory/target pattern แทน

---

# 14. การใช้ร่วมกับ Issue

Issue ใช้เป็นใบบรีฟงานได้

ขั้นต่ำของ Issue:

```md
## Worker
Cast

## Worker Room
Cast/

## Target
tools/w3api.py

## Task
จัดทำคู่มือใช้งาน Termux สำหรับ w3api.py

## Scope
report-file-allowed

## Output
docs/guides/W3API_TERMUX_GUIDE_TH.md

## Do Not
ห้ามแก้ core/runtime/
```

จากนั้น Worker หรือ Agent จะใช้ Issue เป็นแหล่ง brief แล้วทำ report หรือสร้างไฟล์ตาม scope

---

# 15. ข้อควรระวัง

```text
1. อย่าส่ง write/merge ถ้ายังไม่ตั้งใจให้แก้ไฟล์จริง
2. เริ่มจาก review/report ก่อนเสมอ
3. อ่าน mutated:false ทุกครั้ง
4. ถ้า server ไม่ตอบ ให้เช็คว่า gateway เปิดอยู่ไหม
5. ถ้า output แปลก ให้ตรวจ target/focus ว่าสะกดถูกไหม
6. อย่าเปิด secrets หรือ token ใน payload
7. ถ้าใช้ curl บนมือถือ ระวัง quote JSON ให้ถูก
```

---

# 16. คำสั่งสั้นสำหรับใช้งานจริง

```bash
# เข้า repo
cd ~/W3_HB_team_BXCGICOG

# เปิด server ถ้ามี simple gateway
python W3_API_SERVER_SIMPLE.py

# ตรวจ health
python tools/w3api.py health

# review REDR memory
python tools/w3api.py review REDR memory

# review DTML law
python tools/w3api.py review DTML law

# review W3 system
python tools/w3api.py review W3 system
```

---

# 17. สรุป

`tools/w3api.py` คือ helper สำหรับส่งคำสั่งจาก Termux เข้า W3-API

W3-API ทำหน้าที่เป็นประตูรับงาน

runtime จะเลือก module ที่เหมาะสม ทำงาน ตรวจ memory และคืน report กลับมา

หลักที่ต้องจำ:

```text
ส่ง brief ให้ชัด
อ่าน output ให้เป็น
เริ่มจาก read/review/report
อย่า mutate truth โดยไม่ตั้งใจ
```

END
