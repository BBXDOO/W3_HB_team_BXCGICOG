# Multi-System Request Assignment

คำร้องสามารถสร้างสายงานหลายระบบได้ โดยไม่บังคับให้ทุกระบบทำหน้าที่เดียวกัน

## Assignment model

Primary รับผิดชอบผลหลัก
Partner รับงานย่อยหรือร่วมสร้างหลักฐาน
Observer ตรวจดู/ให้ข้อสังเกต
Final decision node ตัดสินการปิดงาน

แต่ละ assignment ต้องอ้าง `request_id` และ source request เดียวกัน เพื่อให้สามารถย้อนประวัติการร่วมงานได้

## History chain

`REQUEST -> ASSIGNMENT -> HANDOFF -> CONTRIBUTION -> RESULT -> SIGN-OFF`

เมื่อมีหลายระบบ ให้สร้าง handoff แยกต่อ participant แทนการคัดลอกคำร้องโดยไม่มีร่องรอย เพื่อรักษาว่าใครได้รับอะไร ในบทบาทใด และส่งอะไรกลับมา

สถานะขั้นต่ำที่ใช้บันทึกได้:
`RECEIVED -> ROUTED -> ACKNOWLEDGED -> WORKING -> RETURNED -> REVIEW -> CLOSED`

สถานะ `CLOSED` ใช้ได้เมื่อเงื่อนไข final sign-off ของคำร้องครบเท่านั้น
