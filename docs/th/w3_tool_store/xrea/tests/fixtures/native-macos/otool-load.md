# fixture ตัวอย่าง load command แบบ native

ต้นฉบับ: [Representative native load-command fixture](https://github.com/BBXDOO/W3_HB_team_BXCGICOG/blob/f22e21a587f69d4da8dccf30e653e2b45ce72c55/w3_tool_store/xrea/tests/fixtures/native-macos/otool-load.md)

`otool-load.txt` เป็นตัวอย่างขนาดกะทัดรัดที่สร้างขึ้นด้วยมือสำหรับตัวรัน native fixture
Mach header ของไฟล์ถูกทำให้สอดคล้องกับคำสั่งทั้งห้ารายการที่แสดงไว้ (คำสั่งรวม 296 ไบต์)
โดยไม่ใช่ข้อมูลที่เก็บจากไบนารีจริง หากต้องการข้อมูลจากเครื่องมือผู้สร้าง ให้ใช้ fixture
ภายใต้ `native-macho-header/` หรือ `native-reexport/`
