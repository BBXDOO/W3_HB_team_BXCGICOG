# Changelog IGET

ประวัติการเปลี่ยนแปลงของระบบ IGET

## v9.0 — Active Runtime

สถานะ: Active runtime

### เพิ่ม / ปรับปรุง

- ใช้ summary comment แบบ idempotent ด้วย marker `<!-- iget:summary -->`
- รองรับ `pull_request_target` โดยใช้ trusted base code
- รองรับ manual dispatch พร้อม PR number ชัดเจน
- resolve runtime context จาก event payload และ environment
- validate repository / PR อย่างเข้มขึ้น
- ใช้ GitHub API client ที่ retry ได้
- inline comments เป็น opt-in
- summary reporting เป็น default ที่น่าเชื่อถือกว่า
- semantic state และ proof trace ยังคงอยู่ในรายงาน

### ความหมายของ v9

v9 เปลี่ยน IGET จาก script scoring tool ไปเป็น runtime governance assistant ที่มีความปลอดภัยและ trace มากขึ้น

---

## v8 / v7 Compatibility

สถานะ: compatibility layer

- มี semantic / proof contract จากรุ่นก่อน
- มี wrapper test เพื่อรักษาพฤติกรรมเดิม
- ใช้สำหรับไม่ให้ runtime ใหม่ทำลาย contract เก่า

---

## v5 — Stable Foundation

สถานะ: historical foundation

- scoring improved
- benchmark added
- inline comment support
- production stable

---

## Next

แนวคิดต่อไป:

- EP signal export
- trust signal
- timeout retry tuning
- multi repo mode
- manual test documentation ภาษาไทย
- BOX index สำหรับ IGET docs และ test manuals
