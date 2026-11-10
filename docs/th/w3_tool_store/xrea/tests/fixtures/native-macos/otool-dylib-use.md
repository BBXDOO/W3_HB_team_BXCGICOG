# ข้อมูล otool สำหรับ dylib-use

ต้นฉบับ: [Dylib-use otool capture](https://github.com/BBXDOO/W3_HB_team_BXCGICOG/blob/f22e21a587f69d4da8dccf30e653e2b45ce72c55/w3_tool_store/xrea/tests/fixtures/native-macos/otool-dylib-use.md)

`otool-dylib-use.txt` เป็น stdout จริงของ `otool -h -l` ที่เก็บไว้โดย
[งานตรวจสอบ Apple CLI/MCP](https://github.com/morluto/rea/actions/runs/38176410166/job/114579755550)
โดยแทนที่เฉพาะบรรทัดชื่อไฟล์แรกด้วย `/owned/fixture:`

แอปพลิเคชันที่สร้างจากซอร์สมาจาก `scripts/verify/apple/macos-bundle.mjs`
ใน load command ทั้ง 23 รายการมี dependency แบบหน่วงเวลาบน `@rpath/libdelay.dylib`
คำสั่ง dylib-use นั้นมีแถว `options delay-init` แทนแถว `time stamp` แบบเดิม
ส่วนคำสั่ง dylib อีกสามรายการยังคงรูปแบบเดิม

ข้อมูลที่เก็บไว้แสดงข้อความจริงจากเครื่องมือผู้สร้าง ขอบเขตคำสั่ง และฟิลด์ dependency
การทดสอบ replay บน Linux ไม่ได้ยืนยันการทำงานจริงของ provider บน macOS;
สายงานตรวจสอบ Apple CLI/MCP เป็นส่วนที่ครอบคลุมการทำงานดังกล่าว
