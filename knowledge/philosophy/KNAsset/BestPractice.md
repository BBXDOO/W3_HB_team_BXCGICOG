# Best Practice (แนวปฏิบัติ/ข้อแนะนำ)

## 1. ออกแบบระบบแบบ modular/agent สากล
- แยกบทบาท agent/plan/context/doc ออกจากกัน
- ทุก agent ต้องรับ—ส่งข้อมูลเป็น parameter/plan/context ชัดเจน
- การเชื่อมโยงระหว่าง agent/plan ใช้มาตรฐานที่ตรวจสอบและดัดแปลงได้ง่าย (เช่น dict/json)

## 2. ทุก agent/module ต้องมี testcase
- สร้างตัวอย่าง input/output สำหรับแต่ละฟีเจอร์/flow 
- ทดสอบก่อนใช้งานจริง, ปรับ example case เพิ่มได้
- ให้ testcase คลุม edge case และ normal case

## 3. ทุกระบบควรมี Usecase ให้ครบก่อน implement จริง
- เพื่ออธิบาย requirement ง่าย, onboarding ได้ทุกคน
- Usecase = "ตัวอย่างกรณีการใช้งานจริง" อย่างเข้าใจง่าย

## 4. ออกแบบให้เพิ่ม agent/template ได้ง่าย
- เพิ่มฟีเจอร์/เปลี่ยน flow, agent, template
  โดยไม่ต้องแก้ระบบอื่น

## 5. ทุกไฟล์ความรู้ต้องเสริม Glossary
- ช่วยให้สื่อสารทุกระดับ ทุกภาษา ทุกชาติ เข้าใจตรงกัน 
- เติมศัพท์/ขยายตัวอย่างใน Glossary เท่านั้น

---

> แนวทางในไฟล์นี้ปรับใช้ได้กับทุกระบบในองค์กรและโครงการ open source
> ถ้าเจอ best practice ใหม่ เติมต่อได้เสมอ เช่น "แนวทาง naming, commit, workflow"
