# เทมเพลต Issue / Comment สำหรับเจ้าของ GitHub

คัดลอกส่วนด้านล่าง เปลี่ยนเจตนา/พาธก่อนส่ง ใช้ @Origin เฉพาะเป้าหมายที่ต้องการ
บล็อก w3-origin ใส่ payload เท่านั้น รหัสงานสร้างจาก issue/comment
ตัวอย่างละพาธเนอร์เพื่อใช้ Orchestration

---

@ChatGPT

ขออ่านไฟล์ที่ระบุและคืนหลักฐานผลอ่านตามวงจร Origin

```w3-origin
{
  "operations": [
    {"action": "read", "path": "ChatGPT/README.md"}
  ]
}
```

---

สำหรับซ่อมโครงสร้าง แทน JSON ในบล็อกด้วยส่วน payload จาก
[selected-repair.origin.json](selected-repair.origin.json) ที่ BBX19 เลือกจุดแล้ว
อย่าใส่ใบงานเต็มในบล็อก มิฉะนั้น operations จะอยู่ผิดตำแหน่ง
