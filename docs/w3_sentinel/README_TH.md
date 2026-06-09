# คู่มือภาษาไทย: W3 Sentinel

> **สถานะ:** draft / observe  
> **ตำแหน่งคู่มือ:** `docs/w3_sentinel/README_TH.md`  
> **Blueprint อ้างอิง:** `blueprints/security/W3_SENTINEL_PLAN_TH.md`  
> **Runtime:** none  
> **Mutation:** false  
> **Final Authority:** BBX19  

---

## 1. W3 Sentinel คืออะไร

W3 Sentinel คือแนวคิดระบบกลางของ W3 สำหรับรับผลตรวจ, alert, status, request และ event จากหลายแพลตฟอร์ม แล้วแปลงกลับมาเป็นภาษากลางของ W3

```text
W3 Sentinel = ศูนย์แปลผลและจัดสถานะจากหลาย HUB / plugin / scanner
```

มันไม่ใช่ตัวแทน CodeQL, OSV, Semgrep หรือ scanner ภายนอกทันที แต่เป็นชั้นกลางที่ช่วยให้ W3 อ่านผลจากทุกที่ด้วยรูปแบบเดียวกัน

---

## 2. ทำไมต้องมี

เมื่อ W3 เริ่มใช้หลายระบบ เช่น GitHub, CodeQL, Airtable, Base44, WE PAPER, 3MOH:HOME, Codex, AI Studio หรือ app ภายนอกอื่น ๆ ผลลัพธ์และคำเตือนจะเริ่มกระจาย

ปัญหาที่จะเจอ:

```text
- แต่ละ platform ใช้ภาษาไม่เหมือนกัน
- alert เยอะขึ้น
- status กระจัดกระจาย
- ไม่รู้ว่าอันไหนแก้แล้ว
- ไม่รู้ว่าอันไหนรอ scan ใหม่
- ไม่รู้ว่า HUB ไหนมีสิทธิ์ทำอะไร
- source truth กับ latest result อาจปนกัน
```

---

## 3. หลักคิดสำคัญ

```text
GitHub = source truth
Airtable = latest result registry
W3 Sentinel = translator / coordinator / gateway
DTML = gatekeeper / scanner
HUB = พื้นที่ภายนอก
Plugin = เครื่องมือหรือความสามารถเฉพาะทาง
Rytm = จังหวะของ identity
BBX19 = final authority
```

กฎสำคัญ:

```text
W3 Sentinel ไม่แก้ source truth เอง
W3 Sentinel ไม่เป็น final authority
W3 Sentinel แปลผล ตรวจขอบเขต และส่งต่อให้ระบบหรือ BBX19 ตัดสิน
```

---

## 4. สิ่งที่ W3 Sentinel ควรรับได้

ระยะแรก:

```text
- CodeQL alerts
- GitHub Actions results
- DTML security scanner report
- manual review note
```

ระยะต่อไป:

```text
- OSV dependency result
- Semgrep result
- Airtable status
- WE PAPER / Base44 event
- w3api pulse
- Plugin connection request
- HUB gate result
```

---

## 5. รูปแบบภาษากลาง

ผลลัพธ์ควรถูกแปลงให้อยู่ในรูปแบบประมาณนี้:

```yaml
id: SEC.GH.CODEQL.0003
source: GitHub CodeQL
platform: GitHub
type: clear_text_storage
severity: high
cwe: CWE-312
file: tools/dtml_security_scanner.py
line: 324
g_state: G3
color: YELLOW
status: fixed_waiting_rescan
boundary: repo_security
mutation: true
owner: BBX19
next_action: wait_for_rescan
result: secret_context_removed_from_report
```

จุดสำคัญคือไม่ว่า source จะมาจากไหน สุดท้ายต้องแปลเป็น:

```text
G-State
Color State
Boundary
Status
Next Action
Owner
Result
```

---

## 6. G-State สำหรับ W3 Sentinel

```text
G0 = unknown
G1 = warning
G2 = contained
G3 = fixed_waiting_rescan
G4 = resolved
```

ตัวอย่าง:

```text
Alert ใหม่เข้า → G1
อ่านแล้วเข้าใจ → G2
แก้ commit แล้ว → G3
GitHub ปิด alert → G4
```

---

## 7. Color State

```text
GREEN  = resolved / clean / stable
BLUE   = observe / tracking / active movement
YELLOW = warning / needs review
RED    = confirmed risk / block
PURPLE = cross-platform / relation-heavy
DARK   = unknown / no data
```

---

## 8. Plugin / HUB / Gate / Rytm

Plugin คือเครื่องมือหรือความสามารถที่เชื่อมเข้ามาช่วย W3 เช่น CodeQL, OSV, Semgrep, Airtable connector, Base44 connector หรือ WE PAPER connector

HUB คือพื้นที่ภายนอกที่มีหลายบริการหรือหลาย gate เช่น GitHub, Airtable, Base44 / WE PAPER, 3MOH:HOME, Google AI Studio, ClickUp หรือ Notion

Gate คือประตูของ HUB แต่ละตัว ใช้จำกัดว่า action ใดทำได้หรือไม่ได้

Rytm คือจังหวะของ identity ก่อนเข้าประตู ทุก HUB หรือ plugin ควรบอกว่า:

```text
ฉันคือใคร
มาจาก HUB ไหน
ขอเข้า Gate ไหน
ตั้งใจทำอะไร
แตะ source truth หรือไม่
ต้องคืนค่าอะไร
```

---

## 9. ตัวอย่าง Flow

### CodeQL Alert

```text
GitHub CodeQL
→ W3 Sentinel
→ แปลงเป็น Security Result
→ ใส่ G-State / Color State
→ บันทึก latest result
→ แก้ repo เมื่อได้รับมอบหมาย
→ รอ scan ใหม่
→ update เป็น resolved
```

### WE PAPER Move File

```text
WE PAPER
→ Gate: folder_tree
→ Rytm: document-surface
→ Move file ภายใน external surface
→ Return result
→ บันทึก latest result
→ ไม่แก้ GitHub repo
```

---

## 10. คู่มือไทยต้องมีทุกงาน

กฎของ W3:

```text
ทุกระบบที่สร้างต้องมีคู่มือภาษาไทยใน docs/
ทุก plugin ต้องมีคำอธิบายและ boundary
ทุก HUB ต้องมี gate model
ทุก action ต้องมี result/log
```

โครงแนะนำ:

```text
docs/w3_sentinel/
├── README_TH.md
├── USAGE_TH.md
├── SECURITY_RESULT_SCHEMA_TH.md
├── PLUGIN_REGISTRY_TH.md
├── HUB_GATE_MODEL_TH.md
├── RYTM_IDENTITY_TH.md
└── EXAMPLES_TH.md
```

---

## 11. สิ่งที่ยังไม่ทำในระยะแรก

```text
- ยังไม่ auto-fix
- ยังไม่ auto-dismiss
- ยังไม่แทน scanner ภายนอก
- ยังไม่ให้ external HUB แตะ source truth
- ยังไม่เปิด public เป็น contract จริง
```

---

## 12. สรุป

W3 Sentinel คือ spine สำหรับจัดการผลตรวจ, plugin, HUB และ external app ในอนาคต

```text
หน้าที่หลัก = แปลผล + ตรวจ boundary + จัด G-State + บันทึก latest result
```

ไม่ใช่ source truth, ไม่ใช่ final authority, และไม่ใช่ scanner แทนทุกอย่างในทันที
