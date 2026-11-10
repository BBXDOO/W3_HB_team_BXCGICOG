# ฉบับแปลภาษาไทย: architecture/system-map.md

> **ต้นฉบับ:** [architecture/system-map.md](https://github.com/BBXDOO/W3_HB_team_BXCGICOG/blob/f22e21a587f69d4da8dccf30e653e2b45ce72c55/architecture/system-map.md) (commit `f22e21a587f69d4da8dccf30e653e2b45ce72c55`)

# ระบบ W3 Hybrid — แผนที่การปฏิบัติงาน
ผู้ใช้ → ทางเข้าโมดูล → เจตนา → การดำเนินการ → บันทึก → ทบทวน → Merge → สถานะ → UI

1. ผู้ใช้/BBX19 → เลือกโมดูล
2. ทางเข้าโมดูล → `request_XXX.md`
3. การดำเนินการ → งานโดย AI/มนุษย์
4. บันทึก (Log) → ลงใน reports หรือ knowledge
5. ทบทวน → BBX19 หรือผู้ทบทวนที่มอบหมาย
6. Merge → ผ่านขั้นตอน PR
7. สถานะ/UI → รีโป้ที่อัปเดตแล้ว
