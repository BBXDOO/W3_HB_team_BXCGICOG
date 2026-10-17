# XREA — สำเนาต้นทาง REA

- AM: Ⅲ Process / บันทึกการนำเข้า
- ผู้ขอนำเข้า: BBX19
- ผู้ดำเนินการ: ChatGPT / Codex
- วันที่: 2026-10-17
- พื้นที่: `w3_tool_store/xrea/`
- ต้นทาง: https://github.com/morluto/rea
- Branch ต้นทาง: `main`
- Commit ต้นทาง: `5d6029ea62a65ec34fd739ee40223c77c6fdb63b`
- Tree ต้นทาง: `b5f0ddb4cc9a4f20fe49fedf774ed0eec746ed3f`
- ใบอนุญาต: MIT — เก็บ LICENSE และเครดิตต้นฉบับครบ

## สิ่งที่เก็บ

สำเนาไฟล์ที่ Git ติดตามทั้งหมดจาก commit ข้างต้น รวมไฟล์เอกสาร ซอร์สโค้ด รูปภาพ และ gitlink ของ submodule ทั้ง 5 ตัว โดยไม่แก้เนื้อหาต้นฉบับ ไม่รวมประวัติ Git ทั้งหมด เป็นสำเนาซอร์ส ณ commit ที่ระบุ ไม่ใช่ GitHub fork แยกต่างหาก

ตั้งชื่อโฟลเดอร์ว่า xrea ตามคำขอ แต่ชื่อแพ็กเกจภายในยังเป็น REA ตามต้นฉบับ

## Submodule

เก็บการอ้างอิง third_party ตาม commit เดิม ยังไม่ได้ดาวน์โหลดเนื้อหา submodule
ไฟล์ `.gitmodules` ที่รูท W3 กำหนดตำแหน่งให้สอดคล้องกับการเก็บภายใต้ xrea โดยเก็บ `.gitmodules` ต้นฉบับภายใน xrea ไว้เหมือนเดิม

หากต้องการดาวน์โหลดภายหลัง ให้รันจากรูท W3:

```bash
git submodule update --init --recursive -- w3_tool_store/xrea/third_party
```

## เอกสารใช้งาน

- [README ต้นฉบับ](../xrea/README.md)
- [README ภาษาไทยของต้นทาง](../xrea/docs/readme/README_th.md)
- [การติดตั้ง](../xrea/docs/installation.md)
- [ใบอนุญาต](../xrea/LICENSE)

## ขอบเขตการตรวจ

ตรวจความตรงกันของ Git tree ของ xrea กับต้นทาง ซึ่งครอบคลุมเนื้อหาไฟล์ ชื่อไฟล์ mode และ gitlink ไม่ได้ติดตั้ง dependency ไม่ได้รัน setup ไม่ได้เชื่อม MCP หรือแก้ runtime ของ W3 และไม่ได้ยืนยันความพร้อมรันบน Termux
