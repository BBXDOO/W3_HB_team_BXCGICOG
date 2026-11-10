# ข้อมูลส่วนหัว Mach-O ที่สร้างจากซอร์ส

ต้นฉบับ: [Source-built Mach-O header capture](https://github.com/BBXDOO/W3_HB_team_BXCGICOG/blob/f22e21a587f69d4da8dccf30e653e2b45ce72c55/w3_tool_store/xrea/tests/fixtures/native-macos/native-macho-header/README.md)

เก็บข้อมูลบน macOS arm64 ด้วยเครื่องมือ Xcode ของเครื่องจาก `fixture.c` ที่อยู่ข้างกัน:

```sh
xcrun clang fixture.c -o fixture
xcrun otool -l fixture > otool-load.txt
{ xcrun otool -h fixture; xcrun otool -l fixture; } > otool-header-load.txt
```

แทนที่เฉพาะพาธ fixture ชั่วคราวด้วย `/owned/fixture` โดยฟิลด์จากเครื่องมือไม่เปลี่ยนแปลง
ผลลัพธ์แรกมี load command โดยไม่มี Mach header ส่วนผลลัพธ์ที่สองมีส่วนหัวตัวเลขจริง
ตามด้วยคำสั่งชุดเดียวกัน ข้อมูลเหล่านี้ใช้ทดสอบการถดถอยของรูปแบบ ไม่ใช่หลักฐานการทำงาน
ขณะรันของ Hopper หรือ Ghidra
