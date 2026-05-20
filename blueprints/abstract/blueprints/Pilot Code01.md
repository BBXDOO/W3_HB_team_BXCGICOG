เอกสารสรุป Pilot Code สำหรับ Semantic Router และ Layer Separation Enforcement

รหัสเอกสาร: W3-PILOT-SEM-SEP-V1
วันที่: 2026-05-20
ผู้จัดทำ: DeepSeek (ในนามทีมพัฒนา W3MPCP)
สถานะ: ฉบับร่างเสนอเพื่อการอ้างอิงและบันทึกความคืบหน้า

เอกสารนี้สรุปแนวคิด รายละเอียด และการใช้งานของชุด Pilot Code จำนวน 2 ชุด ซึ่งเป็นส่วนหนึ่งของแผนพัฒนา Agent Alignment v2 และ Semantic Coordination Foundation สำหรับระบบ W3/MPCP โดยอ้างอิงตามข้อเสนอที่ได้รับความเห็นชอบจากทีม (GO AHEAD)

---

สารบัญ

1. Pilot ที่ 1: Layer Separation Enforcement
2. Pilot ที่ 2: Semantic Router

---

1. Pilot ที่ 1: Layer Separation Enforcement

1.1 คืออะไร

Layer Separation Enforcement คือชุดสคริปต์และกลไก CI/pre-commit ที่ตรวจสอบการละเมิดขอบเขตระหว่างชั้นทางสถาปัตยกรรมของ W3 (Layer A–F, W3Lgu, MPCP runtime, Condien, PRX) โดยอัตโนมัติ โดยมีจุดประสงค์เพื่อป้องกัน concept drift และ การกลืนกันของ layer ที่อาจทำให้ระบบสูญเสียความชัดเจนและความสามารถในการขยายในระยะยาว

1.2 วัตถุประสงค์

· ป้องกันการ import หรือการเรียกใช้ฟังก์ชันข้าม layer อย่างไม่เหมาะสม (เช่น การเรียกใช้ runtime executor จากโมดูลภาษา W3Lgu)
· สร้างมาตรฐาน forbidden import patterns ที่ทีมยอมรับร่วมกัน และสามารถปรับปรุงได้
· บันทึกการละเมิด (violation) ลงใน W3DB (FBD, XIZ) เพื่อการวิเคราะห์และปรับปรุงกระบวนการ
· ใช้เป็นข้อมูลป้อนกลับให้กับ CI/CD (GitHub Actions) และ pre-commit hook เพื่อให้ทีมตรวจสอบได้ทันทีก่อน merge

1.3 ความสามารถ

ความสามารถ รายละเอียด
การสแกน imports ต้องห้าม ค้นหา pattern from mpcp.runtime import ... ในโมดูลภาษา (w3lgu/, core/w3lgu/) หรือ pattern ที่กำหนดใน WHB
การอ่านกฎจาก WHB อ่านกฎ layer separation จากตาราง WHB ใน W3DB (เช่น IF module_path matches "w3lgu/*" AND import_contains "runtime.executor" THEN action=fail_ci)
การบันทึกผลลง W3DB เมื่อพบ violation ให้สร้าง FBD (failure point), XIZ (action log), และ TUF (state snapshot) พร้อม link ตาม relation flow
การแสดงผลผ่าน PRX สรุปผลการตรวจสอบเป็นสัญลักษณ์/สี (▲ สีแดง = fail, ● สีเหลือง = warning, ■ สีเขียว = pass) ตาม W3Lgu-Signal
การ integate กับ CI สามารถคืนค่ารหัสออก (exit code) ที่ไม่เป็นศูนย์ เมื่อพบ violation ทำให้ pipeline หยุดหรือแจ้งเตือน

1.4 โครงสร้างและความสัมพันธ์

· ไฟล์หลัก: scripts/enforce_layer_separation.py
· การเรียกใช้: สามารถรันผ่าน command line, pre-commit hook, หรือ GitHub Actions workflow
· การเชื่อมต่อกับ W3DB:
  · อ่านกฎจาก WHB (domain="layer_separation")
  · บันทึก violation แต่ละครั้งเป็น FBD และ XIZ
  · สร้าง TUF snapshot หลังการสแกน
  · สร้าง PRX สรุปผล
· ความสัมพันธ์กับ layer อื่น:
  · ใช้ mpcp.runtime.contract เพื่อตรวจสอบความถูกต้องของ state (ถ้าต้องการ)
  · ไม่มีการเรียกใช้ w3lgu parser โดยตรง (รักษา separation)

1.5 การใช้งาน

```bash
# รายงาน violation (ไม่บันทึก W3DB)
python scripts/enforce_layer_separation.py --dry-run

# บันทึก violation ลง W3DB (ต้องมี store เริ่มต้น)
python scripts/enforce_layer_separation.py --w3db-store

# ใช้เป็น pre-commit hook
# เพิ่มใน .pre-commit-config.yaml:
#   - repo: local
#     hooks:
#       - id: layer-separation
#         name: Check layer separation
#         entry: python scripts/enforce_layer_separation.py --ci-mode
#         language: system
#         files: \.py$
```

1.6 ข้อสังเกต (ข้อควรระวัง)

· กฎที่อ่านจาก WHB ต้องได้รับความเห็นชอบจากทีม governance ก่อนนำมาใช้ใน CI
· การสแกนอาจช้าเมื่อ repo มีขนาดใหญ่ ควรพิจารณาแยกการสแกนเฉพาะไฟล์ที่เปลี่ยนแปลง (incremental)
· การบันทึก W3DB ทุก violation อาจทำให้ store เติบโตเร็ว ควรตั้งค่า max_store_size และมี cleanup policy
· Pilot นี้อยู่ในระดับ proof by minimal ยังไม่ครอบคลุม dynamic import หรือการเรียกใช้ผ่าน eval/exec

1.7 อื่นๆ (แนวทางพัฒนาในอนาคต)

· เพิ่มความสามารถในการตรวจสอบการใช้ function call แทนการตรวจเฉพาะ import
· สร้าง dashboard แสดงสถิติ violation จาก W3DB
· รองรับการ auto-fix บางกรณี (เช่น เปลี่ยน import path ใหม่) โดยขออนุญาตผู้ใช้

---

2. Pilot ที่ 2: Semantic Router

2.1 คืออะไร

Semantic Router คือกลไกในการจัดส่งงาน (task dispatch) ไปยัง agent ที่เหมาะสม โดยไม่ได้อาศัยการ hardcode ชื่อโมดูล แต่ใช้ บทบาท (role) และ แนวคิด (concept) ที่ประกาศใน metadata ของ agent (mpcp_role, mpcp_concepts) รวมถึงบริบทและความต้องการของงาน เพื่อตัดสินใจ route แบบยืดหยุ่น

2.2 วัตถุประสงค์

· เปลี่ยนจากการ dispatch แบบ procedural (switch case หรือ if-elif ตามชื่อโมดูล) ไปสู่การ dispatch แบบ semantic coordination
· ลดการพึ่งพาชื่อโมดูลตายตัว ทำให้เพิ่ม agent ใหม่หรือปรับเปลี่ยน role ได้โดยไม่ต้องแก้ไข core dispatcher
· สร้างรากฐานสำหรับความสามารถในอนาคต เช่น capability discovery, cross-agent handoff, และ load balancing
· บันทึกการ route และผลลัพธ์ลง W3DB เพื่อการ trace และปรับปรุง routing logic

2.3 ความสามารถ

ความสามารถ รายละเอียด
การอ่าน metadata ของ agent อ่าน mpcp_role, mpcp_concepts จาก registry (AGENT_TABLE)
การ route ตาม role รับ required_role (เช่น "validation", "governance") → คืน agent ที่มีบทบาทตรงกัน
การ route ตาม concept keywords รับ list keywords → คำนวณคะแนนความเกี่ยวข้องกับ mpcp_concepts ของแต่ละ agent (ปัจจุบันใช้การจับคู่แบบคำ)
Fallback เมื่อไม่มี agent เหมาะสม คืน FallbackAgent หรือ raise exception ตาม parameter
การบันทึกผลลง W3DB ทุก routing action บันทึกเป็น XIZ (action, result, reason) รวมถึง TUF สำหรับ session state

2.4 โครงสร้างและความสัมพันธ์

· ไฟล์หลัก: core/semantic_router.py
· การพึ่งพา:
  · core.runtime.agents.registry.get_agent, AGENT_TABLE
  · src.w3db.store, src.w3db.crud.xiz (สำหรับบันทึก log)
· ความสัมพันธ์กับ W3DB:
  · เมื่อ route สำเร็จ → สร้าง XIZ (result=agent_name, confidence=0.9)
  · เมื่อ route ไม่สำเร็จ → สร้าง XIZ + FBD (confidence=0.2)
  · สร้าง TUF สำหรับ routing session (เก็บ current_route, last_agent)
· ความสัมพันธ์กับ Condien: อนาคตอาจอ่าน Condien layer เพื่อปรับ routing ตามบริบท

2.5 การใช้งาน

```python
from core.semantic_router import route_task

# route โดย role
agent = route_task(
    task_description="ตรวจสอบความถูกต้องของเอกสาร",
    required_role="validation",
    store=store  # optional
)

# route โดย concept keywords
agent = route_task(
    task_description="ออกแบบสถาปัตยกรรม flow",
    concept_keywords=["flow", "design", "architecture"],
    store=store
)

# route สำเร็จ → agent จะเป็น instance เช่น GeminiAgent หรือ ChatGPTAgent
# route ไม่สำเร็จ → raise NoSuitableAgentError หรือคืน FallbackAgent
```

2.6 ข้อสังเกต (ข้อควรระวัง)

· การจับคู่ concept keywords ใน v1 ยังเป็นแบบคำต่อคำ (string matching) อาจเกิด false positive หรือ false negative ได้ในสถานการณ์ที่มีความหมายใกล้เคียง
· ยังไม่มีการคำนึงถึงน้ำหนัก (weight) หรือความสำคัญของแต่ละ concept
· ไม่มีกลไก learning หรือปรับปรุง routing อัตโนมัติจาก feedback (ต้องทำ manual tuning metadata)
· การบันทึก W3DB ทุก routing action อาจเพิ่ม overhead เล็กน้อย ควรเปิดเป็น optional หรือใช้ sampling

2.7 อื่นๆ (แนวทางพัฒนาในอนาคต)

· ใช้ inspect_mpcp() เพื่อเพิ่มความแม่นยำในการจับคู่ concept กับเอกสาร
· รองรับการ route แบบหลาย agent (handoff หรือ parallel)
· สร้าง scoring model จากความสำเร็จในอดีต (บันทึกจาก XIZ) เพื่อปรับลำดับความเหมาะสม
· ผสานกับ Condien layer เพื่อให้ routing รับรู้ context ปัจจุบัน (เช่น session state, user preference)

---

บทสรุปและความคืบหน้าโดยรวม

Pilot code ทั้งสองชุดอยู่ในระหว่างการพัฒนา (implementation phase) โดยใช้หลัก proof by minimal และ visible impact first ตามที่ทีมแนะนำ คาดว่าจะมี draft PR ภายใน 48–72 ชั่วโมงนับจากได้รับ GO AHEAD

เอกสารนี้ใช้เป็น reference สำหรับการทบทวน ปรับปรุง และบันทึกการเปลี่ยนแปลง ในรอบการพัฒนาถัดไป หากมีข้อแก้ไขหรือข้อเสนอเพิ่มเติมโปรดแจ้งให้ทีมทราบผ่านช่องทาง discussion หรือ PR ที่เกี่ยวข้อง

ขอบคุณทีมที่สนับสนุนและผลักดันให้เกิด semantic layer ในระบบ W3 อย่างเป็นรูปธรรมครับ
(DeepSeek – ในนามผู้จัดทำ pilot และเอกสารประกอบ)
