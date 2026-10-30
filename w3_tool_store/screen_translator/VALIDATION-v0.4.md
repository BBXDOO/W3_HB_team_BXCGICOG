# ผลตรวจรุ่น 0.4-preview

วันที่ 2026-10-30 · AM Ⅲ - OBSERVE · OWNER: BBX19 · MAKER: ChatGPT/Codex

## ผลที่ตรวจแล้ว

- Java 17, Gradle 8.9, Android SDK 35: `:app:assembleDebug :app:testDebugUnitTest :app:lintDebug :app:assembleRelease` **ผ่าน**
- JUnit **24 tests, 0 failures/errors**: เดิม 12 + บทความ 12 (DOM order, legacy manual chrome, malformed HTML, heading/list/code/table, language hints, charset, size limits, SQLite-row-sized paragraph splitting, escaped URLs, scheme rejection, lossless translation chunks, export fallback)
- Lint **0 errors, 9 warnings** จากการวาด/ข้อความ/ทิศทาง layout เดิม ไม่อ้างว่าไม่มีคำเตือน
- Workbench `android_apk_probe` ตรวจ APK release จริง **PASSED** ดู [evidence/apk-v0.4-report.json](evidence/apk-v0.4-report.json)
- `scripts/publish_update.py --check-only` ยืนยัน package `org.w3.translate.preview`, versionCode **4**, certificate ตรงกับ pin เดิม จึงผ่านเงื่อนไขลงนามสำหรับอัปเดตทับ (ยังไม่ยืนยันว่าติดตั้งบน OPPO สำเร็จ)
- APK release ในรอบนี้ 33,644,740 bytes; SHA-256 `b2911563e4eba1ab6fb60b58dc3b2ebe62a8050081d148d3fb6b0976e639fc3c` — APK จาก CI อาจมี hash ต่างกัน แต่ต้องผ่าน certificate pin เดียวกัน
- ทดสอบ restore signing ทั้งมี/ไม่มี configuration: ไม่สร้าง `GITHUB_ENV`, output มีเฉพาะ ready flag, encrypted keystore mode 0600, signed build ใช้ secret environment โดยตรง และลบไฟล์ชั่วคราวเมื่อจบ
- Python SQLite บนเครื่อง build ใช้ CREATE TABLE และ search SQL ที่ดึงจาก `ArticleStore.java` โดยตรง: ปิด/เปิดฐานข้อมูลแล้วยังมีต้นฉบับคู่ไทย, ค้นไทยพบ, URL ซ้ำถูกปฏิเสธ, ลบ article แล้ว blocks ถูกลบตาม **ผ่าน** เป็น host SQLite ไม่ใช่ Android SQLite runtime

## เนื้อหาเว็บจริงที่ทดลองแยกโครงสร้าง

ดาวน์โหลด HTML ผ่าน network proxy ตามปกติ แล้วเรียก **ArticleExtractor Java ตัวเดียวกับแอป** (ไม่เก็บเนื้อหาบทความทั้งหน้าใน repository):

| หน้า | ผล HTTP | ผลแยกข้อความ |
|---|---|---|
| https://docs.github.com/en/get-started/start-your-journey/about-github-and-git → `/what-is-github` | 200 หลัง redirect | 38 ส่วน / 4 หัวข้อ / 3,369 ตัวอักษร / ภาษา en |
| https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F | 200 | 37 ส่วน / 7 หัวข้อ / 1 บล็อกโค้ด / 7,588 ตัวอักษร / ภาษา en |
| https://pmc.ncbi.nlm.nih.gov/articles/PMC11330162/ | 203 | ไม่ถือว่าได้บทความวิชาการ; ตัว fetch ในแอปรับเฉพาะ HTTP 200 |

พบ Git book navigation ปะปนในการทดสอบรอบแรก จึงเพิ่มการเลือก `#main`/article body ก่อน container ทั่วไป และเพิ่ม regression test เพื่อไม่เอาสารบัญทั้งเล่มมาต่อเป็นบทความหน้าปัจจุบัน

ลองเรียก `ArticleFetcher` end-to-end ด้วย JVM ในเครื่อง build แล้วติด **UnknownHostException** ก่อน HTTP เพราะ runtime นี้ใช้ DNS ผ่าน proxy ฝั่งเครือข่าย จึง **ไม่อ้างว่า Java HTTP fetch บน Android ผ่าน** ไม่ปิด TLS/ไม่เปลี่ยน DNS เพื่อหลบข้อจำกัด ผลตารางข้างบนยืนยันการดาวน์โหลดผ่าน proxy และการ parse HTML จริง แยกจากการทดสอบ native network บนโทรศัพท์

## สิ่งที่ยังรอหลักฐาน

- UI / share intent / Android SQLite persistence / offline model / pause+resume / document picker / rotation บน OPPO จริง
- การติดตั้ง v0.4 ทับ v0.3 ผ่านตัวอัปเดตจริง
- ความครบของบทความจากเว็บอื่น โดยเฉพาะเนื้อหาที่ต้องล็อกอิน/JavaScript/anti-bot/PDF
- ไม่รับประกันคำแปลทางวิชาการ สูตร หรือโค้ด inline; แยกต้นฉบับให้ตรวจเสมอ บล็อกโค้ดไม่แปล

ใบทดลองที่ทำตามได้อยู่ใน [DEVICE_TEST_TH.md](DEVICE_TEST_TH.md) หัวข้อ A1–A13; คู่มือและขอบเขตอยู่ใน [ARTICLES_TH.md](ARTICLES_TH.md)
