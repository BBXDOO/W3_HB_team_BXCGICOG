# W3_NODE_RELATIONS_TABLE_TH
## ตารางความสัมพันธ์ระหว่างโหนดภายในระบบ W3 ฉบับภาษาไทย
### สำหรับใช้งานภายใน เพื่อทำความเข้าใจการเชื่อมโยงเชิงหน้าที่ และใช้ต่อยอดเป็น network map / integration blueprint

> **สถานะเอกสาร:** ใช้งานภายใน  
> **วัตถุประสงค์หลัก:** ใช้บันทึกและจัดระเบียบความสัมพันธ์ระหว่าง node ต่าง ๆ ในระบบ W3  
> **เป้าหมาย:** ช่วยให้สามารถมองเห็น dependency, governance flow, memory flow, protocol flow และ execution flow ได้อย่างเป็นระบบ  
> **หมายเหตุ:** ตารางนี้เป็น “working model” เพื่อใช้พัฒนาและ refine ต่อ ไม่ใช่ statement สาธารณะหรือ contract ภายนอก

---

# สารบัญ

1. บทนำ
2. วัตถุประสงค์ของเอกสารนี้
3. วิธีอ่าน relation table
4. ประเภทของความสัมพันธ์ที่ใช้ในเอกสาร
5. ระดับความเข้มของความสัมพันธ์
6. ตาราง node หลักของระบบ
7. ตารางความสัมพันธ์ระดับโครงสร้างใหญ่
8. ตารางความสัมพันธ์ของ core nodes
9. ตารางความสัมพันธ์ของ protocol nodes
10. ตารางความสัมพันธ์ของ module / agent nodes
11. ตารางความสัมพันธ์ของ docs / knowledge nodes
12. ตารางความสัมพันธ์ของ tools / validation nodes
13. ตารางความสัมพันธ์ของ memory / logs / outcomes nodes
14. ความสัมพันธ์ที่ควรจับตาเป็นพิเศษ
15. ความสัมพันธ์ที่ยังไม่ควรถูกเปิดเผยออกภายนอก
16. ความสัมพันธ์ที่อาจพัฒนาเป็น external contract ได้ในอนาคต
17. วิธีใช้ตารางนี้ในการสร้าง network graph
18. วิธีใช้ตารางนี้ในการเตรียม integration plan
19. แม่แบบเติมข้อมูลเพิ่มเติม
20. บทสรุป

---

# 1) บทนำ

หลังจากมอง W3 ในฐานะ “ชุดของ node ภายในระบบ” แล้ว  
ขั้นถัดไปที่สำคัญคือการบันทึกว่า node ต่าง ๆ **สัมพันธ์กันอย่างไร**

เพราะในมุมมองแบบเครือข่าย ระบบจะมีความหมายก็ต่อเมื่อเรารู้ว่า:

- node ไหนพึ่ง node ไหน
- node ไหนกำกับ node ไหน
- node ไหนสร้างข้อมูลให้ node ไหน
- node ไหนบันทึกผลจาก node ไหน
- node ไหนทำหน้าที่ตีความ node อื่น
- node ไหนเป็นสะพานเชื่อมข้ามชั้น
- node ไหนคือ candidate สำหรับเชื่อมออกภายนอก

เอกสารนี้จึงทำหน้าที่เป็น “relation map ในรูปแบบตาราง”  
เพื่อใช้เป็นฐานก่อนจะกลายเป็นแผนภาพเครือข่ายในภายหลัง

---

# 2) วัตถุประสงค์ของเอกสารนี้

1. บันทึกความสัมพันธ์ระหว่าง node ต่าง ๆ ใน W3
2. จัดหมวดความสัมพันธ์ให้อ่านง่าย
3. ใช้ดู dependency และ flow ภายในระบบ
4. ใช้รองรับการออกแบบ network map
5. ใช้ประกอบ boundary model และ public surface plan
6. ใช้เป็นฐานสำหรับ external integration blueprint ในอนาคต

---

# 3) วิธีอ่าน relation table

ในเอกสารนี้ ความสัมพันธ์จะถูกเขียนในรูปตารางดังนี้

| Source Node | Relation | Target Node | Strength | ความหมาย |
|---|---|---|---|---|

### คำอธิบาย
- **Source Node** = จุดต้นทาง
- **Relation** = ประเภทความสัมพันธ์
- **Target Node** = จุดปลายทาง
- **Strength** = ระดับความสำคัญหรือความแนบแน่นของความสัมพันธ์
- **ความหมาย** = คำอธิบายสั้น ๆ

---

# 4) ประเภทของความสัมพันธ์ที่ใช้ในเอกสาร

เพื่อให้ใช้ซ้ำได้ เอกสารนี้กำหนด relation type หลักไว้ดังนี้

| Relation | ความหมาย |
|---|---|
| `depends_on` | พึ่งพาเพื่อทำงาน |
| `governs` | กำกับดูแลหรือควบคุม |
| `loads` | โหลดหรือดึงเข้ามาใช้งาน |
| `routes_to` | ส่งต่อหรือ route ไปยังอีก node |
| `logs_to` | บันทึกผลหรือ event ไปยัง node ปลายทาง |
| `stores_in` | เก็บข้อมูลไว้ที่ node ปลายทาง |
| `documents` | อธิบายหรือบันทึกความรู้เกี่ยวกับอีก node |
| `interprets` | ตีความหรือให้ความหมาย |
| `validates` | ตรวจสอบความถูกต้อง |
| `reports_on` | สรุปหรือรายงานเกี่ยวกับ |
| `supports` | สนับสนุนการทำงาน |
| `exposes_candidate_for` | มีศักยภาพเป็นจุดเปิดเชื่อมในอนาคต |
| `feeds` | ป้อนข้อมูลให้ |
| `reflects` | สะท้อนผลหรือสภาวะของ |
| `coordinates` | ประสานงานหลาย node |

---

# 5) ระดับความเข้มของความสัมพันธ์

| ระดับ | ความหมาย |
|---|---|
| H | สูงมาก / critical |
| M | ปานกลาง |
| L | ต่ำ / เชิงอ้อม / สนับสนุน |

---

# 6) ตาราง node หลักของระบบ

ตารางนี้ใช้เป็น reference ก่อนดู relation tables

| Node | ประเภท |
|---|---|
| `core/runtime` | Core |
| `core/memory` | Memory |
| `core/governance` | Governance |
| `core/module-loader` | Core |
| `core/events` | Core/Event |
| `core/logs` | Evidence |
| `core/adapters` | Interface |
| `core/vault` | Evidence/Persistence |
| `modules/*` | Agent / Module |
| `protocol/mpcp` | Protocol |
| `protocol/EP_SIGNAL` | Protocol |
| `w3lgu` | Semantic / Protocol |
| `docs` | Documentation |
| `knowledge` | Knowledge |
| `architecture` | Architecture |
| `tools` | Utility |
| `src` | Execution |
| `logs` | Evidence |
| `outcomes` | Outcome / Ledger |

---

# 7) ตารางความสัมพันธ์ระดับโครงสร้างใหญ่

| Source Node | Relation | Target Node | Strength | ความหมาย |
|---|---|---|---|---|
| `protocol/*` | `interprets` | `core/*` | H | โปรโตคอลและ semantic layer ให้กรอบความหมายแก่แกนระบบ |
| `core/*` | `coordinates` | `modules/*` | H | core ทำหน้าที่ประสานและควบคุม module |
| `modules/*` | `logs_to` | `logs/` | H | ผลการทำงานของโมดูลควรถูกบันทึก |
| `modules/*` | `stores_in` | `outcomes/` | M/H | ผลลัพธ์บางส่วนอาจถูกเก็บใน outcome layer |
| `docs/` | `documents` | `core/*` | H | docs อธิบายโครงสร้างและการทำงานของแกนระบบ |
| `knowledge/` | `reflects` | `system behavior` | M/H | knowledge สะสมการตีความและความต่อเนื่องของระบบ |
| `tools/` | `supports` | `core/*` | H | tools สนับสนุน runtime / validation / audit |
| `tools/` | `validates` | `modules/*` | H | เครื่องมือบางตัวตรวจสอบโมดูล |
| `architecture/` | `documents` | `protocol/*` | H | architecture ช่วยอธิบาย layer เชิงโครงสร้าง |
| `core/governance` | `governs` | `modules/*` | H | governance กำกับโมดูล |
| `core/governance` | `governs` | `tools/*` | M/H | governance กำกับการใช้เครื่องมือภายใน |
| `core/memory` | `supports` | `runtime / agents` | H | memory สนับสนุนการต่อเนื่องของระบบ |

---

# 8) ตารางความสัมพันธ์ของ core nodes

## 8.1 ความสัมพันธ์ภายใน core

| Source Node | Relation | Target Node | Strength | ความหมาย |
|---|---|---|---|---|
| `core/runtime` | `depends_on` | `core/module-loader` | H | runtime ต้องรู้จัก module และวิธีโหลด |
| `core/runtime` | `depends_on` | `core/events` | H | runtime พึ่งระบบ event |
| `core/runtime` | `logs_to` | `core/logs` | H | runtime ต้องบันทึกเหตุการณ์ภายใน |
| `core/runtime` | `stores_in` | `core/memory` | M/H | state หรือ context อาจถูกเก็บใน memory |
| `core/module-loader` | `loads` | `modules/*` | H | module-loader โหลด registry และ module |
| `core/module-loader` | `depends_on` | `core/vault / identity data` | M | identity/registry อาจต้องใช้ข้อมูลกำกับ |
| `core/events` | `feeds` | `core/runtime` | H | events เป็น input flow ของ runtime |
| `core/governance` | `governs` | `core/runtime` | H | runtime ต้องอยู่ภายใต้กฎ |
| `core/governance` | `governs` | `core/module-loader` | H | module loading อาจถูกจำกัดด้วย policy |
| `core/logs` | `stores_in` | `evidence trail` | H | logs คือหลักฐานการทำงาน |
| `core/memory` | `supports` | `modules/*` | H | modules พึ่ง memory เพื่อบริบทต่อเนื่อง |
| `core/adapters` | `routes_to` | `external-facing candidates` | M | adapters อาจเป็น bridge layer ในอนาคต |

## 8.2 core relation ที่สำคัญมาก
- `core/runtime -> core/module-loader`
- `core/runtime -> core/events`
- `core/runtime -> core/logs`
- `core/governance -> core/runtime`
- `core/memory -> modules/*`

ความสัมพันธ์ 5 ชุดนี้ควรถูกมองเป็น “แกนในสุด” ของเครือข่ายภายใน

---

# 9) ตารางความสัมพันธ์ของ protocol nodes

## 9.1 Protocol → Core

| Source Node | Relation | Target Node | Strength | ความหมาย |
|---|---|---|---|---|
| `protocol/mpcp` | `interprets` | `core/runtime` | H | MPCP ให้กรอบ orchestration / flow |
| `protocol/mpcp` | `supports` | `core/events` | H | event flow อาจผูกกับ logic orchestration |
| `protocol/EP_SIGNAL` | `interprets` | `core/events` | H | signal layer มีผลต่อการตีความ event |
| `protocol/w3db` | `supports` | `src/w3db` | H | protocol/data model เชื่อมสู่ implementation |
| `w3lgu` | `interprets` | `protocol/*` | M/H | w3lgu อาจเป็นชั้นความหมายที่กว้างกว่า |
| `w3lgu` | `supports` | `core/runtime` | M/H | semantic layer ช่วยตีความการปฏิบัติการ |

## 9.2 Protocol → Modules

| Source Node | Relation | Target Node | Strength | ความหมาย |
|---|---|---|---|---|
| `protocol/mpcp` | `coordinates` | `modules/*` | H | โมดูลอาจถูกรวมด้วย orchestration logic |
| `w3lgu` | `interprets` | `modules/*` | M/H | ภาษากลางช่วย map role/meaning ของโมดูล |
| `protocol/EP_SIGNAL` | `feeds` | `signal-aware modules` | M | บางโมดูลอาจใช้ logic จาก signal layer |

---

# 10) ตารางความสัมพันธ์ของ module / agent nodes

## 10.1 Modules → Core

| Source Node | Relation | Target Node | Strength | ความหมาย |
|---|---|---|---|---|
| `modules/*` | `depends_on` | `core/runtime` | H | โมดูลต้องพึ่ง runtime หรือ execution orchestration |
| `modules/*` | `depends_on` | `core/module-loader` | H | โมดูลต้องอยู่ใน registry/load structure |
| `modules/*` | `logs_to` | `core/logs` | M/H | ผลการทำงานบางส่วนควรเข้าสู่ระบบ log กลาง |
| `modules/*` | `stores_in` | `core/memory` | M | context / state / summaries อาจถูกเก็บใน memory |
| `modules/*` | `governed_by` | `core/governance` | H | การทำงานต้องอยู่ภายใต้ policy |

> หมายเหตุ: `governed_by` ในการใช้งานจริงอาจแทนด้วย `core/governance -> governs -> modules/*`

## 10.2 ความสัมพันธ์ระหว่าง modules เชิงบทบาท

ตารางนี้เป็นการตีความเบื้องต้นจากชื่อและโครงสร้าง

| Source Node | Relation | Target Node | Strength | ความหมาย |
|---|---|---|---|---|
| `modules/ChatGPT` | `supports` | `design / interaction layers` | M | มี notes, prototypes, ux-sim, flow-lab |
| `modules/Gemini` | `supports` | `analysis / validation layers` | M/H | มี analysis-lab, logic-check, risk-scan |
| `modules/Grok` | `supports` | `insight / interpretation / risk layers` | M/H | มี insight-vault, interpret-lab, risk mitigation |
| `modules/DeepSeek` | `supports` | `exploration / observation / studio layers` | M/H | มี studio, observation notes, pattern-lab |
| `modules/Copilot-Gm` | `supports` | `governance / workspace support` | M | มี governance, workspace, onboarding |
| `modules/W3Agent` | `supports` | `automation / response workflows` | M/H | มี auto responder tooling |

---

# 11) ตารางความสัมพันธ์ของ docs / knowledge nodes

## 11.1 Docs → System

| Source Node | Relation | Target Node | Strength | ความหมาย |
|---|---|---|---|---|
| `docs/` | `documents` | `core/*` | H | เอกสารอธิบายแกนระบบ |
| `docs/` | `documents` | `modules/*` | H | เอกสารช่วยทำความเข้าใจโมดูล |
| `docs/` | `documents` | `protocol/*` | H | เอกสารสรุป protocol และโครงสร้าง |
| `architecture/` | `documents` | `system map` | H | architecture เป็นมุมมองเชิงโครงสร้างสูง |
| `knowledge/` | `reflects` | `system evolution` | H | knowledge สะสมเรื่องราวและการเติบโต |
| `reports/` | `reports_on` | `system state` | H | รายงานต่าง ๆ สะท้อนสถานะหรือผลประเมิน |

## 11.2 Docs ↔ Governance

| Source Node | Relation | Target Node | Strength | ความหมาย |
|---|---|---|---|---|
| `docs/review` | `reports_on` | `governance / completion / audit state` | H | review docs เป็น evidence เชิงการกำกับ |
| `core/governance` | `documents` | `policy expectations` | H | governance docs อธิบายกติกา |
| `docs/governance` | `supports` | `core/governance` | M/H | documentation layer ขยายความนโยบาย |

---

# 12) ตารางความสัมพันธ์ของ tools / validation nodes

## 12.1 Tools → Nodes

| Source Node | Relation | Target Node | Strength | ความหมาย |
|---|---|---|---|---|
| `tools/validate_modules.py` | `validates` | `modules/*/module.json` | H | ตรวจ module manifest |
| `tools/validate_metadata.py` | `validates` | `markdown/governance metadata` | H | ตรวจ metadata policy |
| `tools/validate_json_schemas.py` | `validates` | `schema/json files` | H | ตรวจ schema validity |
| `tools/validate_runtime_log.py` | `validates` | `runtime logs` | M/H | ตรวจ log structure |
| `tools/w3_agent_ci.py` | `coordinates` | `validation tools` | H | เป็นตัว orchestrate การตรวจ CI |
| `tools/run_audit.py` | `reports_on` | `system state` | M/H | ใช้ตรวจหรือ audit สถานะ |
| `tools/smoke_test.py` | `validates` | `basic execution readiness` | M | ตรวจ readiness เบื้องต้น |

## 12.2 Tools ↔ Governance

| Source Node | Relation | Target Node | Strength | ความหมาย |
|---|---|---|---|---|
| `core/governance/rules` | `governs` | `tools/w3_agent_ci.py` | H | CI ผูกกับ ruleset |
| `tools/*` | `supports` | `governance enforcement` | H | tools คือกลไกบังคับใช้เชิงปฏิบัติ |

---

# 13) ตารางความสัมพันธ์ของ memory / logs / outcomes nodes

## 13.1 Memory/Logs Flow

| Source Node | Relation | Target Node | Strength | ความหมาย |
|---|---|---|---|---|
| `core/runtime` | `logs_to` | `core/logs` | H | runtime สร้าง internal traces |
| `modules/*` | `logs_to` | `logs/` | H | โมดูลมีร่องรอยการทำงาน |
| `modules/*` | `stores_in` | `outcomes/` | M/H | บางผลลัพธ์อาจกลายเป็น outcome |
| `core/memory` | `stores_in` | `memory_store / queue` | H | บริบทต่อเนื่องถูกเก็บไว้ |
| `reports/` | `reflects` | `logs/outcomes/system state` | H | รายงานสรุปจากหลักฐาน |
| `knowledge/SESSION_LOG*` | `reflects` | `interaction history` | M/H | บันทึกการทำงานหรือการสนทนา |

## 13.2 Evidence Relations

| Source Node | Relation | Target Node | Strength | ความหมาย |
|---|---|---|---|---|
| `logs/` | `supports` | `audit / review / debugging` | H | log ช่วยตรวจสอบ |
| `outcomes/` | `supports` | `historical continuity` | H | outcome เป็นร่องรอยผลลัพธ์ |
| `core/logs` | `supports` | `governance validation` | M/H | log ช่วยตรวจสอบภายใน |
| `reports/` | `reports_on` | `logs / outcomes / modules` | H | รายงานเชื่อมหลักฐานสู่ความเข้าใจ |

---

# 14) ความสัมพันธ์ที่ควรจับตาเป็นพิเศษ

ความสัมพันธ์ต่อไปนี้ควรถูกมองว่าเป็น “critical relations” ของระบบ

| Source Node | Relation | Target Node | เหตุผล |
|---|---|---|---|
| `core/runtime` | `depends_on` | `core/module-loader` | สำคัญต่อการรันระบบ |
| `core/runtime` | `depends_on` | `core/events` | สำคัญต่อ flow |
| `core/governance` | `governs` | `core/runtime` | สำคัญต่อความปลอดภัยและทิศทาง |
| `protocol/mpcp` | `coordinates` | `modules/*` | สำคัญต่อ orchestration |
| `modules/*` | `logs_to` | `logs/core logs` | สำคัญต่อ traceability |
| `core/memory` | `supports` | `runtime/modules` | สำคัญต่อ continuity |
| `tools/w3_agent_ci.py` | `coordinates` | `validation tools` | สำคัญต่อ quality control |

---

# 15) ความสัมพันธ์ที่ยังไม่ควรถูกเปิดเผยออกภายนอก

ความสัมพันธ์ต่อไปนี้มีแนวโน้มเป็น “internal relations” ที่ไม่ควร externalize ตรง ๆ

- `core/runtime -> core/memory`
- `core/runtime -> core/logs`
- `core/module-loader -> identity/registry internals`
- `modules/* -> internal logs/outcomes`
- `governance -> internal enforcement flows`
- `review/report -> internal operational evidence`
- `knowledge/session logs -> internal context history`

เหตุผลหลัก:
- เข้าใจยากหากไม่มีบริบท
- มีผลต่อ internal architecture
- อาจสะท้อน prototype หรือ internal state
- ยังไม่ควรถูกเข้าใจเป็น public contract

---

# 16) ความสัมพันธ์ที่อาจพัฒนาเป็น external contract ได้ในอนาคต

บาง relation มีศักยภาพกลายเป็น public-facing contract ได้ หากถูกจัดทำใหม่

| Candidate Relation | แนวทางพัฒนา |
|---|---|
| `public docs -> architecture overview` | ทำเป็น public onboarding |
| `public protocol summary -> external integrators` | rewrite เป็น protocol guide |
| `safe examples -> public usage flow` | สร้าง example package |
| `selected adapters -> integration gateway` | สร้าง external interface layer |
| `module summaries -> public capability profile` | ทำเป็น profile แบบคัดแล้ว |

---

# 17) วิธีใช้ตารางนี้ในการสร้าง network graph

## ขั้นตอนที่แนะนำ

### ขั้นที่ 1 — สร้าง graph ระดับ cluster
ใช้ node กลุ่มใหญ่ก่อน:
- Core
- Modules
- Protocol
- Docs
- Governance
- Memory/Logs
- Tools
- Public candidates

### ขั้นที่ 2 — เพิ่ม relation จากตารางนี้
เช่น:
- governs
- depends_on
- logs_to
- documents
- validates

### ขั้นที่ 3 — แยกสีตาม boundary
- B0 = สีแดง/เข้ม
- B1 = สีส้ม
- B2 = สีฟ้า
- B3 = สีเขียว

### ขั้นที่ 4 — ทำ 2 แผนภาพ
1. **Internal Functional Graph**
2. **Future External Exposure Graph**

---

# 18) วิธีใช้ตารางนี้ในการเตรียม integration plan

ตาราง relation นี้มีประโยชน์มากเวลาเตรียมแผนเชื่อมภายนอก เพราะช่วยให้ตอบได้ว่า:

- จุดเชื่อมควรมาจาก node ใด
- node นั้นพึ่งพาอะไรบ้าง
- ถ้าเปิด node หนึ่ง จะลากอะไรออกไปด้วย
- ต้องมี governance หรือ logging รองรับจุดไหน
- relation ไหนเป็น internal-only และ relation ไหนปรับเป็น interface ได้

## หลักสำคัญ
อย่าออกแบบ integration จาก “ไฟล์ที่อยากเปิด”  
แต่ให้ออกแบบจาก “relation ที่ปลอดภัยต่อการเปิด”

---

# 19) แม่แบบเติมข้อมูลเพิ่มเติม

หากต้องการขยายเอกสารนี้ต่อ ให้ใช้ template ต่อไปนี้

## 19.1 Relation Template

| Source Node | Relation | Target Node | Strength | Boundary | Notes |
|---|---|---|---|---|---|

## 19.2 ตัวอย่าง
| Source Node | Relation | Target Node | Strength | Boundary | Notes |
|---|---|---|---|---|---|
| `core/runtime` | `logs_to` | `core/logs` | H | Internal | เก็บ execution traces |
| `tools/validate_modules.py` | `validates` | `modules/*/module.json` | H | Internal | enforce manifest consistency |

---

# 20) บทสรุป

เอกสารนี้มีหน้าที่เปลี่ยนความเข้าใจจาก:
- “มีโฟลเดอร์อะไรบ้าง”
ไปสู่
- “อะไรเชื่อมกับอะไร และเพราะอะไร”

ซึ่งเป็นก้าวสำคัญมากสำหรับการพัฒนา W3 ต่อในฐานะระบบเครือข่าย

แก่นสำคัญของ relation model นี้คือ:
1. core เป็นแกนควบคุม
2. protocol เป็นแกนความหมาย
3. modules เป็นแกนปฏิบัติการ
4. tools เป็นแกนสนับสนุนและตรวจสอบ
5. logs / memory / outcomes เป็นแกนหลักฐานและความต่อเนื่อง
6. docs / knowledge / architecture เป็นแกนการอธิบายระบบ

เมื่อรวม relation table กับ node map และ boundary model แล้ว  
คุณจะมีฐานสำคัญมากพอสำหรับการสร้าง:

- internal network graph
- public surface plan
- external network blueprint

---

## ภาคผนวก A: relation สำคัญ 10 อันดับแรก

1. `core/runtime -> depends_on -> core/module-loader`
2. `core/runtime -> depends_on -> core/events`
3. `core/runtime -> logs_to -> core/logs`
4. `core/governance -> governs -> core/runtime`
5. `core/governance -> governs -> modules/*`
6. `core/memory -> supports -> modules/*`
7. `protocol/mpcp -> coordinates -> modules/*`
8. `tools/w3_agent_ci.py -> coordinates -> validation tools`
9. `docs/ -> documents -> core/protocol/modules`
10. `reports/ -> reports_on -> system state`

---

## ภาคผนวก B: เอกสารถัดไปที่ควรทำ

หลังเอกสารนี้ เอกสารที่ควรทำต่อคือ:

1. `W3_PUBLIC_SURFACE_PLAN_TH.md`  
   เพื่อกำหนดว่าควรเปิดอะไรออกภายนอกได้บ้าง

2. `W3_EXTERNAL_NETWORK_BLUEPRINT_TH.md`  
   เพื่อออกแบบภาพรวมการเชื่อมโยงภายนอก

3. `W3_GRAPH_MODEL_SCHEMA_TH.md`  
   เพื่อทำ schema สำหรับเก็บ node/relation เป็นข้อมูลโครงสร้าง

---