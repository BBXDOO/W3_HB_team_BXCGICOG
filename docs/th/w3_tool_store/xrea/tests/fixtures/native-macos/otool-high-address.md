# ข้อมูล otool สำหรับ address ค่าสูง

ต้นฉบับ: [High-address otool capture](https://github.com/BBXDOO/W3_HB_team_BXCGICOG/blob/f22e21a587f69d4da8dccf30e653e2b45ce72c55/w3_tool_store/xrea/tests/fixtures/native-macos/otool-high-address.md)

`otool-high-address.txt` เป็นผลลัพธ์ที่เก็บจาก Apple `otool` ที่ติดตั้งไว้ โดยเปลี่ยน
เฉพาะบรรทัดชื่อไฟล์แรกเป็น `fixture:` ข้อมูลนี้ทดสอบ address ที่เกินช่วงจำนวนเต็ม
ปลอดภัยของ JavaScript และรูปแบบการระบุ alignment จริง `2^N (bytes)` ไฟล์ Mach-O
ขนาดเล็กที่สุดถูกสร้างขึ้นในเครื่องโดยไม่มีการนำไบนารีเข้าระบบควบคุมเวอร์ชัน

สร้างข้อมูลนี้ซ้ำบน macOS ด้วย Xcode command line tools:

```sh
python3 - <<'PY'
import struct
from pathlib import Path

base = 0xfffffff007004001
header = struct.pack('<8I', 0xfeedfacf, 0x0100000c, 0, 5, 1, 152, 0, 0)
segment = struct.pack(
    '<II16sQQQQIIII', 0x19, 152, b'__TEXT', base, 0x1000, 0, 185, 5, 5, 1, 0,
)
section = struct.pack(
    '<16s16sQQIIIIIIII', b'__text', b'__TEXT', base + 184, 1,
    184, 0, 0, 0, 0x80000400, 0, 0, 0,
)
Path('/tmp/rea-high-address.macho').write_bytes(header + segment + section + b'\xc0')
PY
xcrun otool -h -l /tmp/rea-high-address.macho
```
