# Interface Map (Safe Abstract Version)

เอกสารชุดนี้อธิบายเฉพาะ Interface Conceptual ของระบบ โดยไม่เปิด protocol จริง

## Module ↔ Module (Concept Only)
- การรับส่งข้อมูลเป็นแบบ abstract  
- ไม่มีการเปิด table, format หรือ state  

## Human Node ↔ AI Node
- ให้เห็นภาพทิศทางการติดต่อ (direction only)
- ไม่ระบุ internal command set  

## System ↔ External Bridge
- อธิบายระดับ conceptual ว่ามีช่องทางเชื่อมต่อ
- เก็บรายละเอียด protocol ไว้ใน private layer
