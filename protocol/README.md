## NAME : Protocal /F
## AM - Ⅰ BUILD : Sub System
## 13:22 - 110869TH. ; IDC - RT100A9
## USE : FOR W3HBT
---
​# Protocol Subsystem

โครงสร้างใหม่สำหรับโมดูลมาตรฐานกลางของระบบ W3 (version 2026)
    Protocal : ในบริบทนี้มิได้มีความหมายตามสากลหากแต่ใช้อ้างถึง ความเป็นคอนเซบของระบบที่ได้ถูกออกแบบมาอย่างเฉพาะเจาะจงโดยใช้ชื่อนี้เป็นศูนย์กลางของ prototype ของระบบย่อยใน W3 

## Directory Structure

### w3lgu/   — language/grammar engine (ย้ายจาก root)
    - ภาษาใหม่ที่ตั้งใจออกแบบสำหรับการสื่อสาร ภายใน ,เหตุการณ์ หรือ กิจฯใดๆ ในW3 ,ปัจจุบันยังคงพัฒนาอยู่
    
### mpcp/    — mpcp core & blueprint spec (ย้ายจาก SYSTEM/TESTS/)
    - สถาปัตยกรรมใหม่ โดยใช้โครงสร้าง และรูปแบบที่อาศัยลักษณะของ "เสาปูนลายหินอ่อน" ซึ่งได้นำมาประยุกต์ใช้โดยเจตนา ,มีการนิยาม ใหม่ในหลายๆด้าน ตั้งแต่โครงสร้างข้อมูลไปจนถึงการใช้งาน
    
### w3db/    — W3DB interface/data law (ย้ายจาก SYSTEM/TESTS/)
    - identity ,memorie ,signature ,รูปแบบการสื่อสารชนิดนึงของ W3 ออกแบบมาเพื่อใช้ในระบบนิเวศน์นี้
    
### EP_SIGNAL/  — Event/Signal interface/semantic trigger (ย้ายจาก SYSTEM/TESTS/)
    - เทคนิคการเข้ารหัสแบบจังหวะ ที่กระชับและใช้งานได้หลายระดับ
    
### Files.void/ — Substrate law/unresolved transmissive placeholder (ย้ายจาก SYSTEM/TESTS/)
    - เทคนิคทางโครงสร้างระบบที่ใช้สำหรับการ เรียกใช้ไฟล์ในประเภทต่างๆ โดยมีหลักการที่ สามารถเรียกใช้ได้โดยไม่ทำลายต้นแบบไฟล์ ,ใช้ซ้ำ ,เสริมระบบอื่นๆ มีลักษณ์คล้าย tool แต่มีโครงสร้างและหลักการที่แตกต่าง

## หมายเหตุ

- โฟลเดอร์ iget/ ยังอยู่ root ไม่ย้าย
- ภายในแต่ละโปรโตคอลสามารถแยก doc, spec, code, tests ตาม pattern ใหม่ได้
- หลัง refactor ทุก import/path/config/test ที่เคยอ้าง root หรือ SYSTEM/TESTS/ ต้องอัปเดต path ใหม่เป็น protocol/

---

## รายการใน Protocal
F/: ..  📂
- [EP_SIGNAL](https://github.com/BBXDOO/W3_HB_team_BXCGICOG/tree/refactor/v0.2/protocol/EP_SIGNAL)
- [Files.void](https://github.com/BBXDOO/W3_HB_team_BXCGICOG/tree/refactor/v0.2/protocol/Files.void)
- [ecs](https://github.com/BBXDOO/W3_HB_team_BXCGICOG/tree/refactor/v0.2/protocol/ecs)
- [files_void](https://github.com/BBXDOO/W3_HB_team_BXCGICOG/tree/refactor/v0.2/protocol/files_void)
- [mpcp](https://github.com/BBXDOO/W3_HB_team_BXCGICOG/tree/refactor/v0.2/protocol/mpcp)
- [w3db](https://github.com/BBXDOO/W3_HB_team_BXCGICOG/tree/refactor/v0.2/protocol/w3db)
- [w3lgu](https://github.com/BBXDOO/W3_HB_team_BXCGICOG/tree/refactor/v0.2/protocol/w3lgu)

D/: ..  📑
README.md 
    
---
## แหล่งอ้างอิงอื่นๆที่เกี่ยวข้อง
    MPCP
    - [MPCP_Architecture](https://github.com/BBXDOO/W3_HB_team_BXCGICOG/blob/refactor/v0.2/docs/MPCP_architecture).
    
OWNER : BBX19
MAKER : BBX19

_ปรับปรุงล่าสุด: 2026-05-25_
    - 13:22 - 110869TH .
