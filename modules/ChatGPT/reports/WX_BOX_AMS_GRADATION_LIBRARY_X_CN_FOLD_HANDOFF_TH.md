---
AM_TYPE: II
ROLE: CONTEXT_HANDOFF_AND_INTERPRETATION
GROUP: LEARN
DERIVED_FROM:
  - docs/governance/AMS.md
  - docs/box/AMS/AMS_README.txt
  - docs/box/AMS/Group_4.md
  - wx/README.md
  - wx/references/wx_box_cn_fold_recovery_anchor.md
  - wx/references/cn_fold_to_wx_box_mapping.md
  - BBX19/status/CN-Fold/README.md
status: evidence_based_snapshot
source_truth: GitHub
runtime: none
mutation: false
review_required: true
prepared_on: 2026-11-25
prepared_by: ChatGPT
authority: BBX19
---

# W3 Context Handoff — wx · BOX · AMS · Gradation · Library-X · CN-Fold

> **เปิดอ่านไฟล์นี้ก่อนเริ่มแชตใหม่** เพื่อรับบริบทที่ตรวจจากเอกสารในรีโป ณ 2026-11-25 (Asia/Bangkok), branch `refactor/v0.2`. นี่เป็น **บันทึกความเข้าใจและร่องรอยหลักฐาน** ไม่ใช่ข้อกำหนดใหม่ ไม่ใช่ source truth แทนเอกสารต้นทาง และไม่ใช่คำสั่งเปิด runtime.

## 0. อ่านภายใน 60 วินาที

1. W3 ให้ความสำคัญกับ **ความหมายต้นทาง (Core Meaning)** มากกว่าโครงสร้างที่เปลี่ยนได้; ทุกการดัดแปลงต้องตรวจย้อนที่มา (AMS).
2. `wx/` เป็นพื้นที่เครื่องมืออ้างอิง/แบบร่าง. `wx:BOX` คือ manifest/reference container ที่ทำให้ folder/node มีตัวตนเชิงบริบท; **ไม่ใช่ตัวรันงาน** และ **ไม่แก้ source truth**.
3. `CN-Fold` (Cross-Nodes Folder) คือแนวคิดยกระดับ folder เป็น node ที่มี host, boundary, relation, index, status; ทิศทางที่ได้รับการยืนยันใน recovery anchor คือ **พฤติกรรม CN-Fold ภายใน wx:BOX** ไม่ใช่ runtime แยก.
4. `AMS` คือการรักษาสายสัมพันธ์ ความหมาย → การประยุกต์ → การปฏิบัติด้วย AM:I/II/III. **`RAMS` เป็นรูปแบบ README ที่ใช้ AMS** ไม่ใช่ชื่อที่ใช้แทน AMS สำหรับไฟล์ Markdown ทุกชนิด.
5. `Gradation` คือรหัสตำแหน่งจากระดับพาธ ชนิด และลำดับของไฟล์/โฟลเดอร์; **ไม่ใช่สิทธิอำนาจหรือระดับความสำคัญ**.
6. `Library-WX` มีเอกสารรองรับอยู่จริงใน `BBX19/notes/LIBRARY_WX.md`; `Library-X` มีเพียงชื่อในแผนงานที่พบ ณ รอบค้นนี้. **ห้ามสรุปว่าเป็นสิ่งเดียวกัน** หรือแต่ง contract ของ Library-X.
7. งานที่เชื่อม BOX/CN-Fold ไปยัง Cross-L, MPCP, W3Lgu, W3-API ต้องอ่าน **recovery anchor** ก่อน. บาง adapter ถูกพักไว้เพราะการเชื่อมหลายแกนพร้อมกันชนกัน.

## 1. ขอบเขตและวิธีอ่านหลักฐาน

- **[ยืนยัน]** = ปรากฏโดยตรงในไฟล์ต้นทางที่อ้างอิง.
- **[สังเคราะห์]** = การเรียบเรียงความสัมพันธ์จากหลายต้นทาง ไม่ใช่ประโยคประกาศของเจ้าของ.
- **[ยังไม่ยืนยัน]** = พบชื่อ/แนวคิด แต่ไม่มีข้อมูลพอจะระบุ implementation, contract หรือสถานะใช้งาน.
- **[จากบทสนทนา]** = ประสบการณ์การสื่อสารกับเจ้าของงาน ไม่ใช้แทนการตรวจโค้ดหรือ Git history.
- ไม่ใช้คำว่า *active* หมายถึงเปิด runtime เว้นแต่ต้นทางระบุ; เอกสารบางชิ้น active เฉพาะฐานะ **reference/recovery**.
- Branch และ commit อาจเปลี่ยนภายหลัง; ตรวจ ref ปัจจุบันก่อนแก้ไขสิ่งใด.

## 2. wx และ BOX

**[ยืนยัน]** `wx/README.md`, `BBX19/notes/BOX.md` และ `wx/templates/box/wx_box_minimum.md` วางกรอบ wx:BOX เป็นกล่องอ้างอิงสำหรับอธิบาย/จัดหมวด/เชื่อมข้อมูล เช่น identity reference, template, registry, file index, relation, boundary, status และ source-truth pointer. BOX ไม่ใช่ identity ต้นทาง, ไม่ใช่ Paper, ไม่ใช่ ROT, ไม่ใช่ MPCP execution environment.

**ขอบเขตการทำงานปัจจุบันของ wx [ยืนยัน]:**
- `wx/registry/template_registry.json` เป็นรายการ template จริง; ตัว `BOX:WX_BOX_MINIMUM_V1` อยู่สถานะ **draft**, boundary `reference_only`, deny `truth_mutation, runtime_execute, source_write, auto_copy`.
- `wx/templates/box/wx_box_minimum.md` มี field หลัก: `box.id/name/type/status/owner`; `host.path/parent/scope`; `refs.source_truth/registry/template`; `relations.parent/children/linked_nodes`; `boundary.visibility/sensitivity/can_execute/can_mutate_source/requires_review`; `index.files/folders/notes`.
- `wx/index/by_box.md`, `wx/engine_index.py`, `wx/indexor.py`, `wx/portdc.py` ตามคู่มือ `docs/box/USAGE_TH.md` ใช้อ่าน/หา/เสนอแนะ/ส่งออกรายการอ้างอิงตามขอบเขต ไม่ใช่คำอนุญาตให้เขียน source.
- `CROLL` กับข้อเสนอ BOX ที่มีการกล่าวถึงยังเป็น **suggestion/opt-in, non-executing** ตามคู่มือ ไม่ถือว่าเป็นการทำงานปลายทางที่บังคับใช้.
- `wx/templates/box/USAGE_TH.md` แนะนำให้เริ่มใช้ template ก่อนงานสมบูรณ์ เพื่อบันทึกความคิดที่กำลังพัฒนา, **copy before use**, ไม่แก้ต้นแบบกลาง.
- `BBX19/notes/BOX.md` อธิบายโครงสร้างที่เสนอ: Library-WX, Engine-Index, Indexor, registry, Log-Info, PortDC และทิศทาง WHUB. ต้องอ่านสถานะรายส่วนก่อนเรียกทั้งหมดว่า implemented.

**สิ่งต้องไม่ทำ [ยืนยัน]:** BOX ไม่ execute, ไม่ grant authority, ไม่เปลี่ยน GitHub/source truth, ไม่ auto-copy, ไม่ข้าม human review, ไม่ยัด identity ทั้งชุดแทน reference, และไม่บังคับทุก folder ให้เป็น BOX.

## 3. CN-Fold และการประกบกับ wx:BOX

**[ยืนยัน]** `BBX19/status/CN-Fold/README.md` ระบุ CN-Fold = **Folder + Node + Host + Boundary + Index + Relation** (รวมสถานะและ source reference). บริบทสำคัญคือ folder ไม่ใช่แค่ที่เก็บไฟล์ แต่ตอบได้ว่า *คืออะไร, อยู่บน host ไหน, มี parent/child/linked node อะไร, เปิดเผยได้แค่ไหน, สถานะล่าสุดคืออะไร*.

**[ยืนยัน]** `wx/references/cn_fold_to_wx_box_mapping.md` อธิบายการแมป:
| แนวคิด CN-Fold | พื้นที่ใน wx:BOX |
|---|---|
| Folder/Node identity | `box.id`, `box.type` |
| Host | `host.path`, `host.scope` |
| Boundary | `boundary.*` |
| Index | `index.files`, `index.folders` |
| Relation | `relations.*` |
| Status | `box.status` |
| Source truth / registry / external surface | `refs.source_truth`, `refs.registry`, `refs.external_surface` |

**[ยืนยัน]** `wx/references/wx_box_cn_fold_recovery_anchor.md` มีสถานะ active/recovery-anchor และ owner approval BBX19. จุดยืนคือ `wx:BOX = manifest + reference container + folder/node context`; `CN-Fold = host + relation + boundary + status behavior`. เอกสาร/เทมเพลตที่ประกบกันเป็น reference-only, runtime none, mutation false. เอกสาร `wx/blueprints/system/wx_box_cn_fold_integration.md` เป็นทิศทางร่าง/สังเกต; อย่าเลื่อนสถานะเป็น production เอง.

**แยกจาก MPCP [ยืนยัน]:** BOX จัด reference/index/บริบทของ node ส่วน MPCP Blueprint มีหน้าที่เสนอรูปร่าง environment/workflow. ความใกล้เคียงไม่ใช่สิทธิให้กลืนหน้าที่กัน.

**บทเรียนจากการชนกัน [ยืนยันใน recovery anchor]:** มีปัญหาเมื่อพยายามมัด Cross-L dispatch, MPCP adapter, E-CS, W3Lgu runtime, BOX suggestion, W3-API และ CI พร้อมกัน; CROLL tests และ BOX/W3-API integration ล้ม. จึง **พัก** Cross-L→MPCP adapter standardization, E-CS chain ที่บังคับ runtime, dependency ของ W3Lgu operational runtime, BOX suggestion ที่บังคับ, และ response standard ที่ผูกหลายแกน. อย่าตีความว่า “ยกเลิกแนวคิด”; มันคือ **หยุดรอ contract ที่ชัด**.

**ลำดับปลอดภัยที่ anchor กำหนด:** return contract → adapter → execution → standardization. สัญญาตอบกลับที่เสนอมี `state: READY|REVIEW|STOP`, `result:null`, `trace:null`, `mutated:false`, `review:true`, `source:null`, `boundary:reference_only`. สถานะนี้เป็น **ข้อเสนอ minimum contract** ไม่ใช่คำยืนยันว่า implementation ทั้งระบบเสร็จแล้ว.

## 4. AMS, กลุ่มเอกสาร และ RAMS: สามสิ่งที่ต้องแยก

**AMS [ยืนยัน — `docs/governance/AMS.md`]:** Architecture Mapping Standard รักษาความหมายของต้นแบบเมื่อโครงสร้างเปลี่ยน. อ่านเป็นสามชั้น:
- `AM:I` **Core Meaning** — เหตุผล ตัวตน หลักปรัชญา ความหมายต้นทาง. ไม่กำหนด runtime.
- `AM:II` **Adaptation** — การแปลงแกนเดิมไปสู่บริบท/การออกแบบเฉพาะ ต้องอ้าง AM:I และไม่เปลี่ยนความหมายต้นทาง.
- `AM:III` **Operational** — workflow/runtime/service/process ที่ปฏิบัติได้ ต้องสืบกลับไปยัง AM:I หรือ AM:II, และไม่ล้มความหมายเดิม.
- metadata สำหรับการจัดชั้นเอกสาร: `AM_TYPE`, `ROLE`, `DERIVED_FROM`. **`DERIVED_FROM` ต้องเป็นที่มาทางความหมายจริง** ไม่ใช่เติมพาธที่มีอยู่เพื่อให้ผ่านรูปแบบ.

**สี่ Group [ยืนยัน — `docs/box/AMS/Group_4.md` และ `docs/box/AMS/AMS_README.txt`]:** `Build`, `Observe`, `Learn`, `Continue`. เป็นแกนบอก **วัตถุประสงค์/ลักษณะเอกสาร**, ส่วน `AM:I/II/III` เป็นชั้นความสัมพันธ์ทางสถาปัตยกรรม. ทั้งสองแกนใช้ประกอบกันได้; **ไม่ใช่ mapping แบบ 1:1**. BUILD ตัวอย่าง: I ต้นแบบ/คอนเซปต์, II ประยุกต์/ออกแบบ, III test/code. Observe เก็บสิ่งที่กำลังเฝ้าดู/ร่าง/ปัญหา, Learn เก็บองค์ความรู้/บันทึกบทเรียน, Continue มุ่งองค์ประกอบนำกลับมาใช้ซ้ำ. การนิยามเฉพาะรหัสของแต่ละ Group ต้องเปิด source อ่านก่อนใช้.

**RAMS เฉพาะ README [ยืนยัน — `docs/box/AMS/AMS_README.txt`]:**
1. `Head` สี่บรรทัดแรก: Name, AM/Group และระบบ, Log time/ID, รหัส Gradation `≡ … - RAMS`.
2. `Body` บรรทัดถัดไป อธิบายสิ่งที่อยู่ใน **ENV/โฟลเดอร์ของ README เอง**.
3. `Movement` แยก `M1` สิ่งในโฟลเดอร์เดียวกัน กับ `M2` ลิงก์เอกสารข้างนอกที่เกี่ยวข้อง.
4. `OWNER` และ `MAKER`.
5. README ไม่มีสิทธิแอบขยายคำอธิบายออกนอก boundary ของ folder ที่อยู่ ยกเว้นการอ้างอิง.
6. **เอกสาร `.md` ที่ไม่ใช่ README ใช้ AMS ตามชนิดเนื้อหา; อย่าฝืนใส่ Head/Body/Movement แบบ README เพียงเพราะถูกขอให้เป็น AMS.**

## 5. Gradation — รหัสที่ต้องคำนวณจากไฟล์จริง

**[ยืนยัน — `docs/governance/AMS.md`]** สัญลักษณ์ `≡`; ใช้สองรูปแบบตามพื้นที่:
- หัว README: `≡ <ระดับ>r<ลำดับ><ชื่อย่อ> - RAMS`
- แผนผัง: `≡ <ระดับ><ชนิด><ลำดับ><ชื่อย่อ> - <ระบบต้นทาง>`

กฎคำนวณ:
1. นับองค์ประกอบพาธจาก root ของ Git: รายการใต้ root = `A`, ลูกของมัน = `B`, ถัดไป = `C`, ... ไม่เดาจากความลึกตามภาพหน้าจอ.
2. ใน Head ของ README ใช้ type `r`; ในแผนผังใช้ `f` folder, `d` document, `c` code. README ในแผนผังนับเป็น `d`.
3. เลขลำดับเริ่ม 1 **ในโฟลเดอร์แม่และกลุ่มที่ถูกต้อง**; ไฟล์แบ่งกลุ่มตามนามสกุล (`.md` กับ `.py` แยกกัน). เรียงตามรายการ Git-tracked ด้วย `LC_ALL=C`; `__init__.py` ก็นับในกลุ่ม `.py`.
4. ชื่อย่อใช้อักษรตัวที่ 1 และ 3 ของ stem ชื่อไฟล์เป็นตัวเล็ก เช่น `README` → `ra`. ต้องนับเลขจากรายการจริง ณ commit/branch ที่จะเขียน.
5. ตัวอย่างใน governance: `w3_tool_store/screen_translator/README.md` ที่ head คือ `≡ Cr4ra - RAMS`; ในแผนผังเป็น `≡ Cd4ra - screen_translator`.
6. **รหัสไม่คงที่ตลอดกาล**: การเพิ่ม/ลบ/เปลี่ยนชื่อไฟล์อาจเปลี่ยนเลข ต้องเก็บพาธเต็มและ commit เพื่อย้อนตรวจ ห้ามสร้างลำดับจากการเดา.

## 6. Library-WX ไม่ใช่คำยืนยันของ Library-X

**[ยืนยัน]** `BBX19/notes/LIBRARY_WX.md` อธิบาย Library-WX ในฐานะโครงร่าง/แนวทางคลัง template, blueprint, index และบันทึกสะสมภายใต้กลไก BOX. องค์ประกอบที่มีจริงควรตรวจไฟล์ `wx/` และ registry ทีละชิ้น.

**[ตรวจพบชื่อ แต่ยังไม่ยืนยันสัญญา]** การค้น `Library-X`, `Library_X`, `LIBRARY_X` ใน GitHub code search รอบนี้:
- `docs/governance/DECLARATION_IV.md` เอ่ย `Library-X` ในรายการทิศทาง/สิ่งที่กำลังพัฒนา.
- `w3_tool_store/agent_workbench/tools/rams_readme_assistant/README.md` เตือน **ห้ามแก้ contract/schema ของ BOX, WX, CN-FOLD, Library-X**; หากเชื่อมต้องตรวจต้นทาง.
- ไม่พบ contract/API/schema/โฟลเดอร์ implementation ของ Library-X จากผลค้นที่เข้าถึง. **นี่ไม่ใช่การพิสูจน์ว่าไม่มีอยู่**; แต่ยังไม่มีหลักฐานพอจะอธิบายหน้าที่ภายใน.

**กฎสำหรับแชตใหม่:** ถ้าผู้ใช้ถาม Library-X ให้ตอบว่าทราบเพียงการอ้างชื่อและข้อห้ามแก้สัญญาโดยพลการ; ขอพาธ/ต้นทางหรือค้นเพิ่มก่อน. อย่าตอบว่า Library-X = Library-WX และอย่าผูกเข้ากับ BOX อัตโนมัติ.

## 7. ความเชื่อมโยงที่สังเคราะห์ได้ (ไม่ใช่สถาปัตยกรรมบังคับใหม่)

| สิ่ง | คำถามที่ตอบ | ไม่ใช่อะไร |
|---|---|---|
| AMS | เอกสารนี้รักษา/ประยุกต์/ปฏิบัติต่อความหมายใด? | runtime engine |
| 4 Groups | เอกสารนี้เกิดเพื่อ Build/Observe/Learn/Continue? | AM:I/II/III โดยอัตโนมัติ |
| RAMS | README ของ folder นี้อธิบาย ENV และทางไปต่ออย่างไร? | format บังคับทุก `.md` |
| Gradation | ตำแหน่งและชนิดของรายการนี้ใน Git ณ จุดเวลาหนึ่งคืออะไร? | สิทธิหรือ authority |
| wx:BOX | reference/container นี้ชี้ identity, host, boundary, index, status ไหน? | executable/system of record |
| CN-Fold | folder/node นี้มี relation และขอบเขตใด? | บังคับให้ทุก folder เป็น node |
| Library-WX | แบบร่างคลัง template/reference ภายในสาย wx มีอะไรบ้าง? | หลักฐานว่า Library-X ใช้งานแล้ว |
| Library-X | **ยังไม่ทราบจากหลักฐานที่เข้าถึง** | ชื่อเรียกอีกแบบของ Library-WX โดยไม่มีหลักฐาน |

**[สังเคราะห์]** AMS รักษาความหมายและ provenance ของคำอธิบาย, RAMS ช่วยให้ผู้อ่านเริ่มที่ ENV ถูกจุด, Gradation ช่วยชี้พาธ/ตำแหน่ง, BOX/CN-Fold เพิ่มบริบทของ folder/node, ส่วน Library-WX เป็นชุดเอกสาร/แม่แบบในสาย wx. ความสัมพันธ์นี้เป็น **แนวทางทำความเข้าใจ** ไม่ใช่ระบบที่ต่อ API แล้วครบ.

## 8. ประสบการณ์การทำงานร่วมกับเจ้าของ (จากบทสนทนา)

- ผู้ใช้ยืนยันหลายครั้งว่า **ห้ามมั่ว**. ภาพผัง, คำว่า `and`, ลูกศร และการแยกองค์ประกอบ **ต้องอ่านตามที่วาด**. ห้ามขยายสมมติฐานเกินข้อความจริง.
- เจ้าของแยก `AMS` กับ `RAMS` อย่างชัดเจน และเคยสั่งว่าเอกสาร Markdown ที่ **ไม่ใช่ README** ใน `protocol/mpcp/` ให้เป็น **AMS ไม่ใช่ RAMS**. นี่เป็นหลักความต่างสำคัญต่อการแก้งานต่อไป; อย่านำไปอ้างว่าได้ตรวจว่าทุกไฟล์ถูกต้องแล้ว.
- ความผิดพลาดที่ต้องป้องกัน: เพิ่ม metadata ให้ไฟล์แล้วสรุปว่าได้ “ศึกษา/ปฏิบัติตาม AMS ครบ” ทั้งที่ไม่ได้ตรวจประเภท, derivation, ความหมาย, boundary. อีกกรณีคือเอาส่วน `Head/Body/Movement` ของ README ไปใส่ non-README. **อย่าทำซ้ำ**; ถ้าต้องแก้ไขย้อนหลังให้ตรวจไฟล์จริงและขอคำสั่งงานเฉพาะ.
- ผู้ใช้ไม่ต้องการคำอธิบายที่กำกวม; ควรสื่อสารสั้น ตรง ระบุหลักฐาน พาธ สถานะ และข้อไม่รู้. ความเป็นมืออาชีพไม่เกี่ยวกับวุฒิการศึกษา.
- การอ้างสิทธิ: เจ้าของงาน/authority คือ BBX19 ตามไฟล์ส่วนที่ตรวจ; ChatGPT เป็นผู้จัดทำบันทึกนี้ ไม่ใช่ผู้อนุมัติ architecture ใหม่.

## 9. วิธีทำงานต่อสำหรับแชตใหม่

1. **อ่านต้นฉบับก่อนแก้**: `docs/governance/AMS.md`, `docs/box/AMS/AMS_README.txt`, `docs/box/AMS/Group_4.md`, `wx/README.md`, `wx/references/wx_box_cn_fold_recovery_anchor.md`, `BBX19/status/CN-Fold/README.md`.
2. ระบุโจทย์ว่าให้ *ศึกษา* / *ร่าง* / *แก้ไฟล์* / *รัน*; อย่านับการอนุญาตให้อ่านเป็นอนุญาตแก้ระบบอื่น.
3. ตรวจ branch, path, existing changes และ source-of-truth. ไม่เดาไฟล์/ID/ลำดับ Gradation; คำนวณจาก Git-tracked files.
4. เมื่อแตะ `.md`: ตรวจว่าเป็น README หรือ non-README, ชนิด AM, Group, semantic `DERIVED_FROM`, scope และคำศัพท์เฉพาะ ก่อนจัดรูปแบบ.
5. เมื่อแตะ BOX/CN-Fold: ตรวจ boundary และ recovery anchor; **reference-only** คือขอบเขตปัจจุบันของชุดนี้. อนุมัติและทดสอบก่อนเพิ่ม runtime/adapter.
6. เมื่อแตะ Library-X: หยุดการตีความที่ยังไม่มีหลักฐาน. สอบกลับคำจำกัดความจากผู้ใช้หรือเอกสารที่หาเจอ.
7. บันทึกผลเป็น **สิ่งที่ตรวจพบ / สิ่งที่เปลี่ยน / สิ่งที่ไม่ได้เปลี่ยน / สิ่งที่ยังไม่รู้** พร้อมลิงก์ไฟล์และ commit.
8. **อ่าน handoff นี้ใหม่ได้ แต่อย่าถือว่าเป็น memory โดยอัตโนมัติ**. แชตใหม่จะเข้าใจได้เมื่อมีการเปิดไฟล์/ระบุพาธนี้; การบันทึก GitHub ไม่รับประกันว่าระบบจะ preload เนื้อหาให้เอง.

## 10. Source map สำหรับยืนยันซ้ำ

ทั้งหมดเป็นพาธสัมพันธ์กับ `BBXDOO/W3_HB_team_BXCGICOG` branch `refactor/v0.2` ณ วันที่จัดทำ.

| แหล่งหลัก | ใช้ยืนยันอะไร |
|---|---|
| `docs/governance/AMS.md` | Core vs Structure, AM:I/II/III, metadata, Gradation |
| `docs/box/AMS/AMS_README.txt` | RAMS README Head/Body/Movement/OWNER/MAKER |
| `docs/box/AMS/Group_4.md` | Build/Observe/Learn/Continue |
| `wx/README.md` | หน้าที่/ข้อห้ามของ wx BOX |
| `BBX19/notes/BOX.md` | BOX Knowledge Infrastructure, ข้อเสนอสถาปัตยกรรม |
| `BBX19/notes/LIBRARY_WX.md` | Library-WX blueprint |
| `wx/registry/template_registry.json` | รายการเทมเพลตและสถานะ BOX draft |
| `wx/templates/box/wx_box_minimum.md` | field และ boundary ของตัวอย่าง BOX |
| `wx/templates/box/USAGE_TH.md` | วิธีใช้/copy before use |
| `docs/box/USAGE_TH.md` | read-only index/indexor/portdc |
| `wx/references/cn_fold_to_wx_box_mapping.md` | ตาราง CN-Fold → BOX |
| `wx/references/wx_box_cn_fold_recovery_anchor.md` | ทิศทางที่อนุมัติ, pause, guardrails, return contract |
| `wx/blueprints/system/wx_box_cn_fold_integration.md` | integration draft/observe |
| `BBX19/status/CN-Fold/README.md` | แนวคิด CN-Fold/สถานะ |
| `docs/governance/DECLARATION_IV.md` | กล่าวชื่อ Library-X ในภาพทิศทาง |
| `w3_tool_store/agent_workbench/tools/rams_readme_assistant/README.md` | ข้อห้ามแก้ contract BOX/WX/CN-FOLD/Library-X |

**ตัวบทสรุป:** เก็บความหมายต้นทาง ตรวจสถานะจริง รักษา boundary อ้างอิงเป็นพาธ ห้ามเติมช่องว่างด้วยการเดา. หากหลักฐานใหม่ขัดกับเอกสารนี้ ให้เชื่อต้นทางที่ใหม่และมี authority มากกว่า แล้วบันทึก revision ของ handoff.
