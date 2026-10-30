# ผลตรวจรุ่น 0.3-preview — อัปเดตแอป

AM Ⅲ - OBSERVE · OWNER: BBX19 · MAKER: ChatGPT/Codex

| รายการ | ผล |
|---|---|
| assembleRelease พร้อม signing config จริง | ผ่าน |
| assembleDebug / testDebugUnitTest / lintDebug | ผ่าน |
| JUnit | 12 tests, 0 failures/errors |
| Android lint | 0 errors, 9 warnings |
| Workbench APK probe บน signed release APK | PASSED |
| publish_update.py --check-only | PASSED: package/version/certificate ตรงก่อนเผยแพร่ |
| Signing restore configured/unconfigured | ผ่าน; secret ไม่ตั้งค่าต้อง skip publishing; ไฟล์กุญแจ permission 0600 |
| Certificate เทียบไฟล์ APK 0.1/0.2 ที่ส่งในแชท | ตรงกัน |
| versionCode / versionName | 3 / 0.3-preview |
| APK | 33,447,158 bytes |
| GitHub channel ก่อนตั้งค่า | ไม่พบ release ของแอปนี้ |
| เพิ่ม repository secret | ต้องทำในหน้า GitHub โดยเจ้าของรีโป้ |
| เผยแพร่ signed release ครั้งแรก | รอตั้งค่า secret และ merge/run workflow |
| ดาวน์โหลด/ติดตั้งอัปเดตครบวงจรบน OPPO | ยังไม่ได้ทดสอบ |

APK SHA-256: `7f2b08c2d1a1a999b1f0ba4d837226efd2decbabcc6ccf1d45d460d322a16b0d`

[หลักฐาน APK](evidence/apk-v0.3-report.json) · [ตั้งค่าครั้งเดียว](UPDATE_SETUP_TH.md)

ไม่มี private key หรือค่า secret ใน source/PR/public artifact ไฟล์ตั้งค่าที่ให้ผู้ใช้แยกอยู่ในพื้นที่ส่วนตัว ไม่ถือว่า build/CI ผ่านเท่ากับเผยแพร่ update channel สำเร็จ

## แก้ CodeQL: clear-text password storage

ลบการเขียนรหัสผ่านลง GITHUB_ENV จาก restore_signing.py ให้ขั้น build รับ INPUT_SIGNING_JSON จาก GitHub Secret โดยตรง และให้ Gradle อ่านค่าในหน่วยความจำ GITHUB_OUTPUT มีเพียง ready=true/false ส่วน keystore ที่เข้ารหัสแล้วใช้ไฟล์ permission 0600 และลบหลังจบ job

ตรวจจริงทั้งกรณีมีและไม่มี Secret: ไม่สร้างไฟล์ GITHUB_ENV, output มีเพียง ready flag และไม่มีรหัสผ่าน จากนั้น assembleRelease ด้วย config เดิมผ่าน ไม่เปลี่ยน certificate หรือรูปแบบ Secret เดิม รอ CodeQL/CI ของ PR แก้ไขและการสแกนหลัง merge เพื่อยืนยันการปิด alert
