# ปุ่มอัปเดตแอปและการตั้งค่าครั้งเดียว

AM Ⅲ - BUILD · OWNER: BBX19 · MAKER: ChatGPT/Codex

## ผู้ใช้แอป

ติดตั้ง APK รุ่น 0.3 ที่แนบในแชททับรุ่น 0.1/0.2 ก่อนหนึ่งครั้ง หลังจากนั้นใช้ปุ่ม **อัปเดตแอป** ที่ด้านบนหน้าหลักได้:

กดตรวจ → พบรุ่นใหม่ใน GitHub Releases ของ W3 → อ่านรายละเอียด → ดาวน์โหลดและติดตั้ง → อนุญาตติดตั้งจาก W3 แปลหน้าจอครั้งแรก → Android ขอให้ยืนยันติดตั้ง

ไม่ตรวจเองในพื้นหลัง ไม่กดติดตั้งแทนผู้ใช้ และไม่ถอนแอปเพื่อแก้ปัญหาลายเซ็น หากยังไม่มีรุ่นเผยแพร่ในช่องทางนี้ จะแจ้งว่ายังไม่พบรุ่นใหม่

## เจ้าของรีโป้ตั้งค่าเพียงครั้งเดียว

การตั้งค่าข้อนี้ต้องทำผ่านหน้าตั้งค่า GitHub เพราะการเชื่อมต่อที่ใช้พัฒนางานนี้ไม่รองรับการเพิ่ม repository secret

1. เปิดรีโป้ `BBXDOO/W3_HB_team_BXCGICOG` → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**
2. Name: `W3_TRANSLATOR_SIGNING_JSON`
3. Secret: คัดลอกเนื้อหาทั้งหมดของไฟล์ส่วนตัว `W3-Translator-Signing-Setup.json` ที่ส่งให้ในแชท แล้วกด **Add secret**
4. เมิร์ก PR ที่มีงานรุ่น 0.3 เข้า `refactor/v0.2` หลังตั้งค่า Secret แล้ว ระบบจะทดสอบ สร้างไฟล์ลงนาม ตรวจ certificate และเผยแพร่ tag `screen-translator-v3`
5. ถ้าเมิร์กไปก่อนตั้งค่า Secret ให้เปิด **Actions → Screen Translator APK → Run workflow** เลือก branch `refactor/v0.2` แล้วเลือก `publish_update` เป็น true

ไฟล์ JSON นี้มีกุญแจส่วนตัวสำหรับลงนามอัปเดต เก็บเป็นส่วนตัว ใช้ในช่อง Secret เท่านั้น ไม่อัปโหลดเป็นไฟล์โค้ด ไม่ใส่ใน Issue/PR/comment และไม่แนบเป็น public release asset

กุญแจในไฟล์ตั้งค่ารักษา certificate เดียวกับ APK 0.1/0.2 ที่ส่งให้ผู้ใช้ ไม่ได้คัดลอกกุญแจของ Personal Sandbox และไม่แก้ repository ของ Personal Sandbox

## วงจรเผยแพร่รุ่นถัดไป

เพิ่ม versionCode ให้สูงขึ้น → ส่ง PR → ทดสอบผ่าน → เมิร์กเข้า `refactor/v0.2` → job `publish-update` ใช้ Secret เดิมลงนาม → ตรวจ fingerprint ตาม `signing-certificate-sha256.txt` → เผยแพร่ release เฉพาะชื่อ `screen-translator-vN` → ปุ่มอัปเดตในแอปตรวจพบ

- ไม่เผยแพร่จาก pull_request และไม่เปิด Secret ให้โค้ดใน PR
- job ที่อ่าน Secret ทำงานเฉพาะ trusted branch `refactor/v0.2` หลังตรวจ APK ผ่าน
- ไม่เขียนทับ release/APK ที่เคยเผยแพร่แล้ว ต้องเพิ่ม versionCode เมื่อเปลี่ยนแอป
- ถ้าไม่ตั้งค่า Secret จะแสดง `publishing skipped` ใน summary; build/test artifact ยังตรวจแยกได้ แต่ไม่ถือว่าเผยแพร่อัปเดตสำเร็จ
- ภายในแอปตรวจ HTTPS/URL ใน repo ที่กำหนด, SHA-256, package ID, versionCode และ certificate ผู้ลงนามตรงกับแอปที่ติดตั้งอยู่ก่อนเปิด installer
- ผลทดสอบบนเครื่องจริงของการอัปเดตยังรอการตั้งค่าและเผยแพร่ signed release ครั้งแรก ไม่ถือว่า UI ปุ่ม/CI ผ่านแล้วแปลว่าดาวน์โหลดและติดตั้งครบวงจรผ่าน

## ที่มา

Updater สร้างใหม่สำหรับแอปนี้ อ้างอิงวิธีทำงานของ Personal Sandbox ในรีโป้ W3; `UpdateApkProvider.java` ดัดแปลงจาก `w3_tool_store/personal_sandbox_template/source/android-app/app/src/main/java/com/w3personalsandbox/app/UpdateApkProvider.java` โดยเปลี่ยน package, ชื่อไฟล์ และตรวจ authority เพิ่ม
