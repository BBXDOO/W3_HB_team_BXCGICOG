# W3 แปลหน้าจอ

AM Ⅲ - BUILD · OWNER: BBX19 · MAKER: ChatGPT/Codex

แอป Android แยกสำหรับช่วยอ่านจีน ญี่ปุ่น และอังกฤษเป็นไทยในเกม คู่มือ และหนังสือ ใช้หน้าหลักภาษาไทย ปุ่มลอยลากย้ายได้ แปลทับบริเวณข้อความ หรือหยุดอ่านเป็นหน้าพร้อมต้นฉบับและปุ่มคัดลอก

## การใช้งาน

1. ติดตั้ง APK รุ่นทดลอง เป็นคนละแอปกับ Personal Sandbox
2. เลือกภาษา หากทราบให้เลือกตรง ๆ; อัตโนมัติยังเป็น heuristic
3. กด **ดาวน์โหลด / ตรวจชุดภาษา** ขณะต่อเน็ต รอข้อความพร้อม
4. กด **เริ่มแปลหน้าจอ** เปิดสิทธิ์แสดงทับแอปตามคำแนะนำ กลับมากดเริ่มและอนุญาตจับภาพทั้งหน้าจอ
5. สลับไปแอปที่ต้องการอ่าน แตะปุ่มลอย **ไทย** เพื่อเปิดเมนู ลากคำว่าไทยเพื่อย้ายปุ่ม
6. ใช้ **ซ่อนคำแปล** เพื่ออ่านต้นฉบับหรือแตะปุ่มแอปเดิม; **เลือกพื้นที่** แล้วลากกรอบเพื่อกรองบริเวณแปล (แตะเฉย ๆ คืนทั้งจอ)
7. ใช้ **อ่านเต็มหน้า** สำหรับข้อความยาว หน้าต่างอ่านเลื่อนได้; คัดลอกเฉพาะเมื่อกดปุ่ม
8. หยุดด้วย **ปิดตัวแปล**, ปุ่มหยุดในแอป หรือ notification ระบบ

## ขอบเขตรุ่นแรก

- Native Java, Android 8 ขึ้นไป, ARM64 (รุ่นแรกสำหรับโทรศัพท์ OPPO ของ BBX19); target/compile SDK 35
- MediaProjection + foreground service + overlay ไม่มี Accessibility service และไม่กดปุ่มแทนผู้ใช้
- OCR แบบ bundled: Latin, Chinese, Japanese; ML Kit Translation ดาวน์โหลดโมเดลในหน้าเตรียมภาษา แล้วแปลข้อความในเครื่องโดยไม่เรียก paid API
- ภาษาจีน/ญี่ปุ่น → ไทยอาจแปลผ่านอังกฤษตามกลไก ML Kit คุณภาพคำศัพท์เฉพาะอาจลดลง
- จับภาพย่อความกว้างไม่เกิน 1080 px; หนึ่งรอบอ่าน/แปลทำงานครั้งเดียว ไม่มีคิวซ้อน; เว้นรอบประมาณ 2.2 วินาทีหลังจบรอบก่อน ไม่รับประกันเวลาจริงหรือ FPS
- ซ่อนหน้าต่างของตัวแปลชั่วคราวและทิ้งเฟรมเก่าก่อนจับภาพใหม่ ป้องกันอ่านคำแปลตัวเอง จึงเห็นคำแปลหายชั่วครู่
- จำกัด 40 text blocks ต่อรอบ; ข้อความยาวมากให้เลือกพื้นที่หรือใช้หน้าอ่าน คำแปลทับจออาจตัดบรรทัด/ซ้อน; หน้าอ่านแสดงผลเต็ม
- อัตโนมัติใช้ Japanese OCR แล้วเลือกภาษาจาก kana/Han/Latin: ญี่ปุ่นคันจิล้วนแยกจากจีนไม่ได้ ให้เลือกญี่ปุ่นเอง ข้อความหลายภาษาภายใน block เดียวอาจแปลผิด
- เลือกพื้นที่กรองจากจุดกึ่งกลาง block; ยังไม่ crop ภาพก่อน OCR
- หมุนจอ/เปลี่ยนสัดส่วน capture ต้องเริ่มใหม่; ไม่รับประกัน floating windows, letterboxing, multi-window หรือ ColorOS ก่อนทดสอบจริง
- หน้าที่ป้องกัน capture หรือ overlay อ่านไม่ได้ เคารพข้อจำกัด Android
- ไม่บันทึกภาพหน้าจอหรือประวัติ เก็บคำแปล cache ในหน่วยความจำเฉพาะ session (ไม่เกิน 256 รายการ); ปิดแล้วล้าง อนุญาตเน็ตสำหรับดาวน์โหลดโมเดลและ SDK อาจส่ง diagnostics ตามเอกสาร Google
- รุ่น `0.2-preview`, application ID `org.w3.translate.preview`, ใช้ **debug signing สำหรับทดสอบ** ยังไม่ใช่ช่องอัปเดต release ห้ามแทนที่ Personal Sandbox

## Build และการตรวจ

```bash
# Java 17, Android SDK platform 35 และ build-tools
./gradlew :app:assembleDebug :app:testDebugUnitTest :app:lintDebug
# APK: app/build/outputs/apk/debug/app-debug.apk
ANDROID_HOME=/path/to/sdk python ../agent_workbench/tools/android_apk_probe/probe.py app/build/outputs/apk/debug/app-debug.apk --output /tmp/apk-report.json
```

ดู [DESIGN.md](DESIGN.md), [DEVICE_TEST_TH.md](DEVICE_TEST_TH.md) และ [ผลรุ่น 0.2](VALIDATION-v0.2.md) และ [ผลรุ่น 0.1](VALIDATION.md) แยกผล build/static tests ออกจากการทดสอบจริง ไม่อ้างว่าแปลบน OPPO ผ่านหากยังไม่มีหลักฐาน

## ที่มา

โค้ดสร้างใหม่ ไม่คัดลอก REA/xrea หรือ Personal Sandbox ใช้ Workbench สำหรับตรวจ APK และเก็บผล โปรเจกต์แอปแยกจากเครื่องมือกลาง Dependencies ของ Google อยู่ภายใต้เงื่อนไขของผู้พัฒนาเดิม:

- https://developers.google.com/ml-kit/vision/text-recognition/v2/android
- https://developers.google.com/ml-kit/language/translation/android
- https://developers.google.com/ml-kit/language/translation
- https://developers.google.com/ml-kit/terms
- https://developers.google.com/ml-kit/usage-and-billing
- https://developer.android.com/media/grow/media-projection

## ปุ่มลอยและแผงรุ่น 0.2

ใช้ภาพ Neumorphism ของ BBX19 เป็นแนวทาง: เทาอ่อน เงานุ่มสองทิศ ปุ่มลอยวงกลม และไอคอนคำสั่ง 2 คอลัมน์ กดแล้วปุ่มยุบลงเล็กน้อย แตะคำว่าไทยเพื่อเปิด/ย่อ ลากส่วนหัวเพื่อย้าย สถานะยังอยู่เมื่อย่อแล้วเปิดใหม่ แผงเลื่อนได้เมื่อพื้นที่จอไม่พอ โค้ดวาดด้วย Android Canvas ไม่มีรูปภาพหรือ dependency เพิ่มสำหรับธีมนี้
