# ผลตรวจรุ่น 0.2-preview — ปุ่มลอยและแผงคำสั่ง

AM Ⅲ - OBSERVE · OWNER: BBX19 · MAKER: ChatGPT/Codex

เปลี่ยน UI ตามภาพอ้างอิง Neumorphism: วงกลมไทย แผงเทาอ่อน เงาขาวบนซ้าย/เงาเข้มล่างขวา ปุ่มเว้าตอนกด ไอคอนเส้นและคำสั่งไทย 2 คอลัมน์ 3 แถว พื้นที่เมนูเลื่อนได้เมื่อจอเตี้ยหรือปรับตัวอักษรใหญ่

| การตรวจ | ผล |
|---|---|
| assembleDebug / testDebugUnitTest / lintDebug | ผ่าน |
| JUnit | 6 tests, 0 failures/errors |
| Android lint | 0 errors, 7 warnings |
| Workbench APK probe | PASSED |
| application ID | org.w3.translate.preview (เดิม) |
| versionCode / versionName | 2 / 0.2-preview |
| SHA-256 ของ certificate เทียบ APK 0.1 ที่ส่งผู้ใช้ | ตรงกัน — ไฟล์แนบ 0.2 ใช้ key เดิม |
| ขนาด APK | 34,329,594 bytes |
| หน้าตา/ปุ่ม/การลาก/การเลื่อนบน OPPO | รอทดสอบรุ่น 0.2 จริง |

APK SHA-256: `c123a50320fa5ab6e33d3b293fbbd07962b5ddd05a9609525c3ea44beea84a78`

[หลักฐาน static APK](evidence/apk-v0.2-report.json)

ผลเครื่องจริงรุ่น 0.1: ผู้ใช้เปิดสิทธิ์ overlay สำเร็จ และส่งภาพแปลอังกฤษหน้า About Git เป็นไทยพร้อมต้นฉบับได้แล้ว ไม่ถือเป็นผลทดสอบรูปลักษณ์ใหม่ 0.2 หรือผลยืนยันภาษาจีน/ญี่ปุ่น

ไฟล์ APK 0.2 ที่ส่งในแชทติดตั้งอัปเดตทับไฟล์ 0.1 ที่ส่งในแชทได้ตาม package/version/certificate ที่ตรวจแล้ว ส่วน APK จาก GitHub Actions ใช้ debug key ของ runner ซึ่งอาจต่างกัน จึงไม่ยืนยันว่าใช้แทนกันสำหรับอัปเดตได้
