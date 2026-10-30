# Android APK probe

AM Ⅲ - BUILD · OWNER: BBX19 · MAKER: ChatGPT/Codex

ตรวจ APK ที่สร้างจริงด้วย Android SDK: ลายเซ็น, application ID, permissions และ manifest พร้อม SHA-256 ไม่เรียกแอป ไม่อ่านข้อมูลในโทรศัพท์ ไม่ใช่หลักฐานว่า OCR หรือแปลบนเครื่องจริงผ่านแล้ว

```bash
ANDROID_HOME=/path/to/sdk python probe.py /path/to/app.apk --output /tmp/apk-report.json
```

ต้องมี Java, Android SDK command-line tools/latest และ build-tools ใช้ SDK ตาม `ANDROID_HOME` หรือ `--sdk` ไม่มีการดาวน์โหลดหรือติดตั้งอัตโนมัติ ข้อมูลเข้าเป็น APK; ผลออกเป็น JSON ทาง stdout และไฟล์ที่ระบุ รายงานไม่มี key หรือลายเซ็นส่วนตัว มีเพียง fingerprint สาธารณะ หากคำสั่งใดตรวจไม่สำเร็จ คืน FAILED และ exit 1

โค้ดสร้างใหม่สำหรับ W3 ไม่คัดลอกจาก xrea สถานะรันจริงดูหลักฐานในโครงการปลายทาง เช่น [Screen Translator](../../../screen_translator/README.md)
