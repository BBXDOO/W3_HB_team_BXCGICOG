# Protocol Subsystem

โครงสร้างใหม่สำหรับโมดูลมาตรฐานกลางของระบบ W3 (version 2026)

---

## Directory Structure

- w3lgu/   — language/grammar engine (ย้ายจาก root)
- mpcp/    — mpcp core & blueprint spec (ย้ายจาก SYSTEM/TESTS/)
- w3db/    — W3DB interface/data law (ย้ายจาก SYSTEM/TESTS/)
- EP_SIGNAL/  — Event/Signal interface/semantic trigger (ย้ายจาก SYSTEM/TESTS/)
- Files.void/ — Substrate law/unresolved transmissive placeholder (ย้ายจาก SYSTEM/TESTS/)

## หมายเหตุ

- โฟลเดอร์ iget/ ยังอยู่ root ไม่ย้าย
- ภายในแต่ละโปรโตคอลสามารถแยก doc, spec, code, tests ตาม pattern ใหม่ได้
- หลัง refactor ทุก import/path/config/test ที่เคยอ้าง root หรือ SYSTEM/TESTS/ ต้องอัปเดต path ใหม่เป็น protocol/

---

_ปรับปรุงล่าสุด: 2026-05-25_