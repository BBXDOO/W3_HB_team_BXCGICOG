# W3_SENTINEL_PLAN_TH
## แผนต้นแบบ W3 Sentinel สำหรับ Security, Quality, Plugin และ External HUB Integration

> **สถานะเอกสาร:** draft / observe  
> **Runtime:** none  
> **Mutation:** false  
> **Source Truth:** GitHub repository  
> **Registry:** Airtable ใช้เป็น latest result registry เท่านั้น  
> **Final Authority:** BBX19  

---

# 1) จุดประสงค์

W3 Sentinel คือแนวคิดสำหรับสร้างชั้นกลางของ W3 ที่ทำหน้าที่รับผลตรวจ, สถานะ, คำขอ, และ event จากหลายแพลตฟอร์ม แล้วแปลงเป็นภาษากลางของ W3

ระบบนี้ไม่ได้เกิดมาเพื่อแทน CodeQL, OSV, Semgrep หรือ tool ภายนอกทันที แต่เกิดมาเพื่อทำให้ W3 ไม่ต้องแตกออกเป็นหลายภาษาเมื่อมีหลาย platform / plugin / HUB เข้ามาในอนาคต

```text
W3 Sentinel = Security + Quality + Plugin + HUB Connection Gateway
```

---

# 2) ปัญหาที่ต้องแก้

เมื่อ W3 โตขึ้น จะมีเครื่องมือและ HUB ภายนอกเพิ่มขึ้น เช่น GitHub, CodeQL, Airtable, Base44, WE PAPER, 3MOH:HOME, Codex, AI Studio, ClickUp, Notion และระบบอื่น ๆ

ปัญหาที่จะเกิดคือ:

```text
- alert หลายแหล่ง ภาษาไม่เหมือนกัน
- severity แต่ละ platform ไม่เท่ากัน
- result กระจัดกระจาย
- agent จำไม่ได้ว่าอะไรแก้แล้ว
- external hub อาจทำเกินหน้าที่
- plugin อาจข้าม boundary
- source truth กับ registry อาจปนกัน
```

ดังนั้น W3 ต้องมีชั้นกลางที่ทำหน้าที่แปล, ตรวจ boundary, ลงทะเบียนผลล่าสุด และส่งต่อภาระงานอย่างมีขอบเขต

---

# 3) หลักการหลัก

```text
1. GitHub = source truth
2. Airtable = latest result registry
3. W3 Sentinel = translator / gateway / coordinator
4. DTML = gatekeeper / scanner / security filter
5. Plugin = external capability หรือ tool เฉพาะทาง
6. HUB = พื้นที่ภายนอกที่มีหลาย gate หรือหลายบริการ
7. Rytm = จังหวะของ identity ก่อนเข้า gate
8. BBX19 = final authority
```

W3 Sentinel ไม่มีสิทธิ์แก้ source truth เอง เว้นแต่ได้รับคำสั่งหรืออยู่ในขอบเขตอำนาจที่กำหนดไว้

---

# 4) ขอบเขตของ W3 Sentinel

## 4.1 สิ่งที่ทำได้

```text
- รับผลจาก CodeQL / GitHub Actions / DTML / OSV / Semgrep
- รับ result หรือ status จาก Airtable / WE PAPER / Base44 / HUB ภายนอก
- แปลงข้อมูลเข้า W3 format กลาง
- ใส่ G-State และ Color State
- ตรวจ boundary ว่า action นั้นเกินสิทธิ์หรือไม่
- ส่ง next action ให้ BBX19 หรือ agent review
- บันทึกผลล่าสุดลง registry
- สร้าง security/quality summary
```

## 4.2 สิ่งที่ไม่ควรทำในระยะแรก

```text
- ไม่ auto-fix repo เอง
- ไม่ auto-dismiss alert เอง
- ไม่แทน CodeQL หรือ scanner ภายนอกทันที
- ไม่ให้ Airtable กลายเป็น source truth
- ไม่ให้ external hub mutate repo โดยไม่มี authority
```

---

# 5) โครงสร้างการทำงาน

```text
External Platform / Plugin / HUB
        ↓
Adapter
        ↓
W3 Sentinel Gateway
        ↓
Normalize เป็น W3 Result / Request / Event
        ↓
G-State + Color State + Boundary + Rytm Identity
        ↓
Registry / Log / Human Review / Next Action
```

---

# 6) ชนิดข้อมูลหลัก

W3 Sentinel ควรรองรับข้อมูลอย่างน้อย 4 แบบ:

```text
1. Security Result
   เช่น CodeQL alert, DTML finding, Semgrep result

2. Quality Result
   เช่น CI pass/fail, test report, schema validation

3. Plugin Event
   เช่น plugin ลงทะเบียน, plugin ส่งผล, plugin ขอ action

4. HUB Request / HUB Result
   เช่น WE PAPER move file, Airtable update status, Base44 graph sync
```

---

# 7) G-State สำหรับ Sentinel

```text
G0 = unknown
ยังไม่รู้ว่า event/result นี้คืออะไร

G1 = warning
มีสัญญาณเตือน ต้องตรวจ

G2 = contained
เข้าใจปัญหาแล้ว อยู่ในขอบเขตควบคุมหรือ Hospitication

G3 = fixed_waiting_rescan
แก้แล้ว รอระบบตรวจซ้ำ หรือรอผลยืนยัน

G4 = resolved
ผ่านการตรวจแล้ว / ปิด alert แล้ว / มี log แล้ว
```

---

# 8) Color State

```text
GREEN  = resolved / clean / stable
BLUE   = observe / tracking / active movement
YELLOW = warning / needs review
RED    = confirmed risk / block
PURPLE = cross-platform / relation-heavy
DARK   = unknown / no data
```

---

# 9) Plugin Registry Model

Plugin คือเครื่องมือหรือ capability ที่ระบบรู้จัก เช่น CodeQL, OSV, Semgrep, Airtable connector, Base44 connector, WE PAPER connector

ตัวอย่าง plugin manifest:

```yaml
plugin_id: PLUGIN.GITHUB.CODEQL
name: GitHub CodeQL
hub: HUB.GITHUB
type: security_scanner
access_mode: read_result
rytm: security-alert
boundary: external-observe
mutation_allowed: false
owner: BBX19
status: active
```

---

# 10) HUB Registry Model

HUB คือพื้นที่ภายนอกที่อาจมีหลายบริการหรือหลาย gate เช่น Base44, WE PAPER, Airtable, GitHub, 3MOH:HOME

ตัวอย่าง hub manifest:

```yaml
hub_id: HUB.BASE44.WE_PAPER
name: WE PAPER
role: external_document_surface
source_truth: false
allowed_actions:
  - read
  - organize
  - preview
  - link
forbidden_actions:
  - mutate_repo_without_approval
  - overwrite_source_truth
rytm_required: document-surface
status: observe
```

---

# 11) Gate Contract

ทุก HUB ควรมี gate เฉพาะ เพื่อไม่ให้ external app เข้าถึง W3 แบบไม่มีขอบเขต

ตัวอย่าง:

```yaml
gate_id: GATE.WEPAPER.FOLDER_TREE
hub: HUB.BASE44.WE_PAPER
purpose: manage_external_folder_tree
allowed_actions:
  - create_folder
  - create_subfolder
  - move_file
boundary:
  source_truth: false
  mutation_scope: external_surface_only
return:
  - state
  - reason
  - trace
  - updated_path
```

---

# 12) Rytm Identity

Rytm คือจังหวะของ identity ที่ทำให้ W3 รู้ว่าใครเข้ามา ขอเข้า gate ไหน และมีสิทธิ์แบบใด

ตัวอย่าง:

```yaml
rytm:
  identity: HUB.BASE44.WE_PAPER
  gate: GATE.WEPAPER.FOLDER_TREE
  intent: move_file_to_folder
  authority: external_surface
  mutation: external_only
  return_contract: required
```

---

# 13) ตัวอย่าง Flow

## 13.1 CodeQL Alert

```text
GitHub CodeQL
→ Adapter
→ W3 Sentinel
→ Security Result
→ G1/G2
→ Registry
→ แก้ใน repo เมื่อได้รับคำสั่ง
→ G3 waiting rescan
→ G4 resolved เมื่อ scan ผ่าน
```

## 13.2 WE PAPER Move File

```text
WE PAPER
→ Gate: folder_tree
→ Rytm: document-surface
→ Action: move_file
→ Boundary: external surface only
→ Result: updated path
→ Registry update
→ No GitHub mutation
```

## 13.3 Airtable Result Update

```text
Airtable
→ Gate: latest_result_registry
→ Action: update status
→ Boundary: result only
→ Source Truth: false
→ Allowed
```

---

# 14) โครงไฟล์ที่เสนอ

```text
tools/w3_sentinel/
├── README.md
├── schema/
│   ├── w3_result.schema.json
│   ├── plugin_manifest.schema.json
│   ├── hub_manifest.schema.json
│   ├── gate_contract.schema.json
│   └── rytm_identity.schema.json
├── registry/
│   ├── plugins.json
│   ├── hubs.json
│   ├── gates.json
│   └── latest_results.json
├── adapters/
│   ├── github_codeql_adapter.py
│   ├── github_actions_adapter.py
│   ├── dtml_report_adapter.py
│   ├── airtable_adapter.py
│   ├── base44_wepaper_adapter.py
│   └── manual_event_adapter.py
└── docs/
    └── internal_notes.md
```

คู่มือภาษาไทยต้องอยู่แยกใน `docs/w3_sentinel/`

---

# 15) แผนระยะ

## Phase 1: เอกสารและ schema กลาง

```text
- สร้าง blueprint
- สร้างคู่มือไทยใน docs/
- นิยาม Security Result / Plugin / HUB / Gate / Rytm
```

## Phase 2: Registry แบบ manual

```text
- เก็บผล alert รอบแรก
- ลง latest result registry
- ใช้ Airtable เป็น mirror เท่านั้น
```

## Phase 3: Adapter ขั้นต้น

```text
- อ่านผล CodeQL / GitHub Actions / DTML
- แปลงเป็น W3 Result format
```

## Phase 4: HUB / Plugin Support

```text
- เพิ่ม plugin registry
- เพิ่ม hub registry
- เพิ่ม gate contract
```

## Phase 5: Dashboard / Health Lens

```text
- สรุปผลเป็น markdown/html
- แสดง G-State / Color State / Next Action
```

---

# 16) กฎคู่มือไทย

ทุกระบบที่เกิดจากแผนนี้ต้องมีคู่มือภาษาไทยใน `docs/` แยกจาก code และ blueprint

```text
code        → tools/
blueprint   → blueprints/
manual TH   → docs/
registry    → registry หรือ Airtable latest result
source truth → GitHub
```

---

# 17) สรุป

W3 Sentinel คือ spine สำหรับรองรับอนาคตหลายแพลตฟอร์ม โดยไม่ให้ alert, plugin, HUB และ external app กระจัดกระจายจนระบบเสียแกน

```text
W3 Sentinel = ตัวแปลผล + gatekeeper + registry coordinator
ไม่ใช่ source truth
ไม่ใช่ final authority
ไม่ใช่ scanner แทนทุกอย่างตั้งแต่แรก
```

หน้าที่ที่สำคัญที่สุดคือทำให้ทุก platform กลับมาพูดภาษา W3 ได้:

```text
G-State
Color State
Boundary
Rytm Identity
Return Contract
Latest Result
```
