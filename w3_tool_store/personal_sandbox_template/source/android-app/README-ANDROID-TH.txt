W3 Personal Sandbox — โครงการสร้างแอป Android สำหรับทดสอบ v38

ไฟล์เว็บใน app/src/main/assets/www อยู่ใน APK เปิดได้โดยไม่ต้องใช้ Termux หรือเซิร์ฟเวอร์
ข้อมูลแต่ละเครื่องเก็บในพื้นที่แอปของ Android เครื่องนั้น

สร้าง APK ด้วย Android Studio:
1. เปิดโฟลเดอร์ android-app เป็น Android Studio project
2. ให้ Android Studio ติดตั้ง Android SDK 35, JDK 17 และ Gradle ตามที่แจ้ง
3. เลือก Build > Build Bundle(s) / APK(s) > Build APK(s)
4. APK สำหรับทดสอบอยู่ใน app/build/outputs/apk/debug/app-debug.apk

สร้างบน GitHub โดยไม่ต้องมีคอมพิวเตอร์:
1. สร้างรีโปส่วนตัวใหม่สำหรับแซนด์บ็อกซ์ ไม่ใช้รีโป W3 ต้นฉบับ
2. อัปโหลดเนื้อหาในโฟลเดอร์ android-app ไปที่รากของรีโปใหม่
   ให้เห็น app/, build.gradle, settings.gradle และ .github/workflows/build-apk.yml
3. เปิดแท็บ Actions > Build W3 Sandbox APK > Run workflow
4. เมื่อสำเร็จ ดาวน์โหลด Artifact ที่ workflow สร้าง (ชื่ออาจระบุรุ่นทดสอบก่อนหน้า)
5. แตก ZIP ของ Artifact แล้วเปิด app-debug.apk เพื่อติดตั้งทดสอบ

ห้ามใช้ APK ทดสอบนี้เป็นรุ่นแจกจริง เพราะ GitHub สร้างกุญแจ debug ใหม่
ในแต่ละการรันและจะติดตั้งอัปเดตทับโดยรักษาข้อมูลไม่ได้

APK ทดสอบติดตั้งได้ แต่หากจะแจกต่อและอัปเดตแบบรักษาข้อมูลในเครื่อง
ให้สร้าง release APK ที่ลงนามด้วย signing key เดิมทุกครั้ง
การเปลี่ยนกุญแจหรือ applicationId ทำให้ติดตั้งทับเวอร์ชันเดิมไม่ได้

การนำข้อมูลจากเว็บเก่า: ใน Chrome เปิด W3 > Export Data > บันทึกไฟล์ JSON
จากนั้นเปิด APK > หน้าโครงการ > นำเข้าไฟล์ JSON
ข้อมูลของ Chrome จะไม่ย้ายเข้า APK อัตโนมัติ

ข้อจำกัด: นี่คือ source project สำหรับสร้าง APK ทดสอบ
รุ่น v38 เพิ่มตัวจัดรูปแบบเนื้อหา ปุ่มคำสั่งในแอป และภาพพื้นพื้นที่ทำงาน ต้องตรวจการใช้งานจริงบนโทรศัพท์หลังติดตั้ง
