# โปรไฟล์ upstream ของอินเทอร์เฟซ EVM

ต้นฉบับ: [EVM interface upstream profile](https://github.com/BBXDOO/W3_HB_team_BXCGICOG/blob/f22e21a587f69d4da8dccf30e653e2b45ce72c55/w3_tool_store/xrea/third_party/evmole/README.md)

REA ผสาน [EVMole](https://github.com/cdump/evmole) ที่ไม่ได้แก้ไขเป็น
dependency ของ npm ที่ระบุแน่นอน `evmole@0.9.3` พร้อมตรวจสอบความสมบูรณ์ผ่าน lockfile
แท็ก `0.9.3` ชี้ไปยัง commit `0409707c2efef11a9043f9b4505cad5719054a7e`

binding ของ JavaScript และเอนจิน WASM ยังคงอยู่ในแพ็กเกจ upstream ต้นฉบับ
REA มีเพียงการตรวจสอบ carrier, worker adapter และสัญญาที่พกพาได้
ไม่จำเป็นต้องมี submodule หรือ fork ของเอนจินที่นำมาเก็บไว้ในโครงการ
ไม่มีการจัดหาฐานข้อมูลลายเซ็น, LLM decompiler, โหนดบล็อกเชน หรือ dependency ของ RPC

upstream ใช้ MIT, copyright (c) 2023 Maxim Andreev เนื่องจาก tarball ของ npm
ไม่มีไฟล์สัญญาอนุญาต REA จึงจัดรวม [LICENSE](https://github.com/BBXDOO/W3_HB_team_BXCGICOG/blob/f22e21a587f69d4da8dccf30e653e2b45ce72c55/w3_tool_store/xrea/third_party/evmole/LICENSE) จากแท็กที่ไม่ได้แก้ไขไว้ที่นี่
เอนจินถูกเริ่มต้นผ่านอินเทอร์เฟซ `no_tla`/`initSync` ของ upstream เฉพาะภายใน worker
ที่โครงการเป็นเจ้าของเท่านั้น การ import บริการของ REA ไม่ทำ WASM/file I/O

การวิเคราะห์อินเทอร์เฟซเบื้องต้นใช้ `contractInfo` โดยเปิดใช้ selectors, arguments และ
stateMutability การกู้คืน selector ยังสกัดและรายงานเมทาดาทาส่วนท้ายด้วย
โดยเก็บรูปแบบที่รายงานไว้พร้อมระบุว่าความแม่นยำและความครอบคลุมไม่ทราบ
เอาต์พุตอื่นของ upstream เป็นสัญญาแยกต่างหากสำหรับอนาคต
โดยเฉพาะอย่างยิ่ง ID ของปลายทาง CFG ไม่ใช่ที่อยู่แบบไบต์ และเมทาดาทา CBOR ส่วนท้าย
ไม่สามารถยืนยันค่าจำนวนเต็มแบบไม่สูญเสียข้อมูลผ่าน binding ปัจจุบันได้
