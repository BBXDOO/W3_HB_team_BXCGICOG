# นำ WABT มาเอง

ต้นฉบับ: [Bring-your-own WABT](https://github.com/BBXDOO/W3_HB_team_BXCGICOG/blob/f22e21a587f69d4da8dccf30e653e2b45ce72c55/w3_tool_store/xrea/third_party/wabt/README.md)

REA ไม่ได้รวม แก้ไข ติดตั้ง หรือดาวน์โหลดไฟล์ปฏิบัติการ WABT ผู้ดำเนินการเลือก
ไดเรกทอรีเครื่องมือที่มีอยู่ด้วย `REA_WABT_BIN_DIRECTORY`

- upstream: https://github.com/WebAssembly/wabt
- รุ่นที่ยอมรับ: https://github.com/WebAssembly/wabt/releases/tag/1.0.42
- commit ของซอร์ส: `ff0ef7e0009402740c805a9744c09b05be063e48`
- สัญญาอนุญาต upstream: Apache-2.0, https://github.com/WebAssembly/wabt/blob/1.0.42/LICENSE
- เครื่องมือขณะทำงาน: `wasm-validate`, `wasm-objdump`, `wasm2wat`
- คอมไพเลอร์สำหรับ fixture ในการตรวจสอบ: `wat2wasm` (ไม่ใช่ข้อกำหนดเบื้องต้นขณะทำงาน)

adapter กำหนดให้ข้อความแสดงเวอร์ชันของทุกเครื่องมือระบุ `1.0.42` และบันทึก
พาธไฟล์ปฏิบัติการที่ระบุได้ SHA-256 ข้อความแสดงเวอร์ชันที่ตรงตามจริง และอาร์กิวเมนต์ของแต่ละเครื่องมือ
การยอมรับเวอร์ชันระบุโปรไฟล์ producer ที่รองรับ แต่ไม่ได้รับรองความแท้ของผู้เผยแพร่
ผู้ดำเนินการยังคงรับผิดชอบเรื่องแหล่งที่มาที่เชื่อถือได้ของไฟล์ปฏิบัติการ
ไม่มีการใช้ `wasm-interp`, decompiler, ตัวแยกวิเคราะห์ไบนารีทดแทน หรือการรันเป้าหมาย

การตรวจสอบจริงบน macOS arm64 ใช้ไฟล์รีลีสทางการ
`wabt-1.0.42-macos-arm64.tar.gz` ที่ไม่ได้แก้ไข ซึ่งตรวจสอบ SHA-256 เทียบกับ
เมทาดาทาของ GitHub release แล้ว:
`3f654779b436c628db3ca4323c51538815f5fbc887a6d5f3bb1c18d36281e240`
ค่านี้ระบุไฟล์ archive ที่ใช้ในการตรวจสอบนั้น ไม่ใช่เครื่องมือใด ๆ ที่ผู้ดำเนินการจัดหามา
