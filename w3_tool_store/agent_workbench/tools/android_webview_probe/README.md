# Android WebView layout probe

AM Ⅲ - BUILD · OWNER: BBX19 · MAKER: ChatGPT/Codex · 2026-10-27

## Body

ทางเลือกตรวจหน้าตาเว็บของ Personal Sandbox ในขนาดหน้าจอ Android ด้วย Chromium, touch input และภาพจับหน้าจอ ไม่ใช่ OPPO Find X9 Ultra emulator และไม่จำลอง ColorOS, Android WebView จริง, file picker, การติดตั้ง APK หรือข้อมูลในเครื่องผู้ใช้

ต้นทาง: `w3_tool_store/personal_sandbox_template/source/` และ Android wrapper ของ `W3-personal-sandbox-app` ใช้ URL ของ dev/preview server; ไม่มีการคัดลอกโค้ดจาก xrea หรือแอปมาไว้ที่นี่ ค่าเริ่มต้น 393 × 873 CSS px เป็น **ค่าทดลอง** ปรับได้ตามขนาด viewport ที่วัดบนเครื่องจริง

## Movement

จาก source แอป: `npm ci && npm run build && npm run preview -- --host 127.0.0.1`

จากโฟลเดอร์นี้: `npm install && npx playwright install chromium && npm run probe`

ตั้ง `W3_PROBE_URL`, `W3_PROBE_WIDTH`, `W3_PROBE_HEIGHT`, `W3_PROBE_OUTPUT` ได้ตามสภาพแวดล้อม ผลอยู่ใน `output/` เป็นภาพ Home/Project/Battle เท่าที่เปิดได้และ `report.json` ระบุ JavaScript error, แนวนอนล้นหน้าจอ และจำนวนส่วนที่เลื่อนได้ การกดเปิดโปรเจกต์และ Battle เป็น best effort ตามข้อความที่มองเห็น; หากยังไม่มีโปรเจกต์จะได้เฉพาะ Home ข้อมูลทดลองต้องสร้างใน browser context แยกก่อน

ต้องติดตั้ง Node และ Chromium ของ Playwright เพิ่ม เครื่องรันที่ไม่มี browser binary ใช้เครื่องมือนี้ไม่ได้ ผลที่ผ่านยังต้องทดสอบปุ่ม ระบบไฟล์ และ WebView บน OPPO เครื่องจริง

สถานะ: ตรวจ syntax ของสคริปต์แล้ว; ยังไม่รัน browser บน host นี้เพราะไม่มี Chromium/Android SDK
