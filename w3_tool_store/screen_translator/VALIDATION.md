# ผลตรวจรุ่น 0.1-preview

AM Ⅲ - OBSERVE · OWNER: BBX19 · MAKER: ChatGPT/Codex

สถานะ: **สร้างไฟล์ติดตั้งและตรวจแบบ static สำเร็จ — รอทดสอบบนโทรศัพท์**

| การตรวจ | ผล |
|---|---|
| Clean assembleDebug | ผ่าน |
| JUnit LanguagePolicyTest | 6 tests, 0 failures, 0 errors |
| Android lintDebug | ผ่าน; 0 errors, 7 warnings |
| โต๊ะช่าง android_apk_probe | PASSED: ลายเซ็น, package ID, permissions, manifest |
| Native ARM64 ELF LOAD alignment | ทั้ง libmlkit_google_ocr_pipeline.so และ libtranslate_jni.so มีค่า 16384 bytes ทุก LOAD segment |
| ขนาด APK | 34,329,594 bytes (~34.3 MB) |
| เปิดแอป/overlay/capture บนโทรศัพท์จริง | **ยังไม่ได้ทดสอบ** |
| ดาวน์โหลดโมเดลและแปลจริง/ความเร็ว/คุณภาพ | **ยังไม่ได้ทดสอบ** |
| ColorOS / OPPO Find X9 Ultra | **ยังไม่ได้ทดสอบ** |

SHA-256 ของ APK:

`5839ed6642b3e00b99e793412f0a8e045429a32dc0661d88244ae60a2f9caea0`

ไฟล์เป็นรุ่นทดลอง ARM64 ใช้ Android debug certificate ยังไม่มี release signing/update channel ที่คงที่ รุ่นถัดไปอาจต้องติดตั้งใหม่หากใช้ key ต่างกัน ไม่ได้แตะ key หรือข้อมูลของ Personal Sandbox

Lint warnings ที่เหลือเกี่ยวกับ ARM64-only/ChromeOS, การรองรับ click ของพื้นที่ลากเลือก, ข้อความไทยที่ไม่ได้แยก resources และพิกัด LEFT ซึ่งตั้งใจยึดตำแหน่งภาพ capture แทนทิศทางตัวอักษร ไม่ปิด lint errors หรือสร้าง baseline เพื่อข้ามการตรวจ

หลักฐาน machine-readable: [evidence/apk-report.json](evidence/apk-report.json)

ขั้นทดสอบจริง: [DEVICE_TEST_TH.md](DEVICE_TEST_TH.md)
