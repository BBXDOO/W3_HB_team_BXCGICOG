# fixture จากเครื่องมือสร้าง WABT

ต้นฉบับ: [WABT producer fixtures](https://github.com/BBXDOO/W3_HB_team_BXCGICOG/blob/f22e21a587f69d4da8dccf30e653e2b45ce72c55/w3_tool_store/xrea/tests/fixtures/wasm/README.md)

`module.wat` เป็นซอร์สที่โครงการดูแลเอง คำสั่ง WABT 1.0.42
`wat2wasm module.wat -o module.wasm` สร้างไบนารีที่ใช้กับ
`wasm-objdump -h -x module.wasm` (`objdump.txt`) และ
`wasm2wat --enable-all module.wasm` (`decoded.wat`) โดยไม่มีการนำไบนารีเข้าระบบ
ควบคุมเวอร์ชัน โมดูลมีฟังก์ชันที่นำเข้า memory และฟังก์ชันที่ส่งออก และ custom section
ชื่อ `test` ส่วน payload ของ custom section ยังคงอยู่เป็น annotation `@custom` ใน WAT
ที่ถอดรหัสแล้ว

commit ของแท็ก upstream: `ff0ef7e0009402740c805a9744c09b05be063e48`
ตัวตรวจสอบที่ใช้เครื่องมือจริงซึ่งแยกต่างหากจะสร้าง fixture ของตนเองด้วย WABT ที่ผู้เรียก
จัดหาให้ แล้วเปรียบเทียบผลลัพธ์จากเครื่องมือผู้สร้างแบบตรงทั้งหมดกับส่วนติดต่อ CLI/MCP
สาธารณะ `custom-names.wat` ครอบคลุมอักขระขึ้นบรรทัดใหม่ เครื่องหมายอัญประกาศ Unicode
แบ็กสแลช เครื่องหมาย section ที่ฝังอยู่ และ NUL ในชื่อ custom โดย objdump แสดงชื่อ
เหล่านั้นโดยไม่ escape และจบแต่ละชื่อที่ NUL ตัวแรก
นอกจากนี้ยังครอบคลุม U+FEFF ที่อยู่ต้นชื่อ รวมถึงชื่อที่ต่างจาก section พิเศษ `name`
และแยกชื่อที่มีเพียง U+FEFF ออกจากชื่อว่าง
