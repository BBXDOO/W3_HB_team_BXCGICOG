# ข้อมูล Universal Mach-O ที่ slice ใช้ CPU ชนิดเดียวกัน

ต้นฉบับ: [Universal Mach-O captures whose slices share one CPU type](https://github.com/BBXDOO/W3_HB_team_BXCGICOG/blob/f22e21a587f69d4da8dccf30e653e2b45ce72c55/w3_tool_store/xrea/tests/fixtures/native-macos/lipo-same-cpu/README.md)

เก็บข้อมูลบน macOS 27.0.1 (26A434), arm64 จากไฟล์ปฏิบัติการของระบบสองไฟล์ที่
FAT slice ทั้งหมดใช้ `CPU_TYPE_ARM64`:

```sh
lipo -detailed_info /System/Applications/Calculator.app/Contents/MacOS/Calculator > calculator.txt
lipo -detailed_info /System/Library/CoreServices/ShortcutDroplet.app/Contents/MacOS/ShortcutDroplet > shortcut-droplet.txt
```

Calculator มี `arm64e` (subtype `0x80000002`) และ `arm64e.x1` (subtype
`0x8000000c`) ส่วน ShortcutDroplet มี `arm64` (subtype `0`) และ `arm64e.x1`
การรับ target ระบุทั้งสองไฟล์ด้วยตระกูล CPU เดียวคือ `arm64` ขณะที่ lipo แสดงสอง slice

พาธของไฟล์ปฏิบัติการในบรรทัด `Fat header in:` ถูกแทนที่ด้วย `fixture` และลบ
ช่องว่างท้ายบรรทัด (lipo พิมพ์ `capabilities ` สำหรับ slice ที่ไม่มี capabilities)
รวมทั้งบรรทัดว่างสุดท้ายออก นอกนั้นฟิลด์จากเครื่องมือไม่เปลี่ยนแปลง
