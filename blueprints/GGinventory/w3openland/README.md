# W3.IDP Studio - Physical & Digital Ecosystem Boardgame Editor

ระบบจัดการและสร้างสตอรี่/บอร์ดเกม (Story & Boardgame Ecosystem Engine) ระดับ Professional รองรับการสร้างตัวละคร (Characters), กระดานและสถานที่ (Boards & Locations), การ์ดและไอเทม (Cards & Items), กฎกติกา (Rulesets), และ Story Flow Nodes พร้อมระบบ Playtest และ Dark Neumorphic UI

---

## 🚀 วิธีการติดตั้งและรันโปรเจกต์บนเครื่องของคุณ (Local Development)

### 1. ความต้องการของระบบ (Prerequisites)
- [Node.js](https://nodejs.org/) เวอร์ชัน 18 ขึ้นไป (แนะนำ v20 LTS)
- npm หรือ yarn หรือ pnpm หรือ bun

### 2. แตกไฟล์ ZIP และเปิด Terminal
```bash
# แตกไฟล์ zip แล้วเข้าไปในโฟลเดอร์โปรเจกต์
cd w3-idp-studio
```

### 3. ติดตั้ง Dependencies
```bash
npm install
```

### 4. รันโปรเจกต์ในโหมด Development
```bash
npm run dev
```
เปิดเบราว์เซอร์ไปที่ `http://localhost:3000` (หรือ URL ที่แสดงใน Terminal)

### 5. บิลด์สำหรับ Production
```bash
npm run build
```
ไฟล์ Production จะอยู่ที่โฟลเดอร์ `dist/` สามารถนำไป Deploy บน Vercel, Netlify, Cloudflare Pages, หรือ Web Server ใดๆ ได้ทันที

---

## 📱 วิธีแปลงเป็นแอปมือถือ (Android / iOS) ด้วย Capacitor

คุณสามารถเปลี่ยนโปรเจกต์นี้เป็น Native Mobile App สำหรับ Android และ iOS ได้อย่างง่ายดายด้วย **Capacitor**:

1. **ติดตั้ง Capacitor:**
   ```bash
   npm install @capacitor/core @capacitor/cli
   npx cap init "W3 IDP Studio" "com.w3.idpstudio" --web-dir dist
   ```

2. **บิลด์เว็บก่อน:**
   ```bash
   npm run build
   ```

3. **เพิ่มแพลตฟอร์ม Android / iOS:**
   ```bash
   # สำหรับ Android
   npm install @capacitor/android
   npx cap add android
   npx cap open android   # เปิดใน Android Studio เพื่อบิลด์เป็น APK / AAB

   # สำหรับ iOS (ต้องทำบน macOS ที่มี Xcode)
   npm install @capacitor/ios
   npx cap add ios
   npx cap open ios       # เปิดใน Xcode เพื่อรันบน iPhone หรือปล่อย App Store
   ```

4. **อัปเดตโค้ดเมื่อแก้ไข:**
   ```bash
   npm run build
   npx cap sync
   ```

---

## 💻 วิธีแปลงเป็น Desktop App (Windows .exe / macOS / Linux) ด้วย Electron

1. **ติดตั้ง Electron:**
   ```bash
   npm install --save-dev electron electron-builder concurrently wait-on
   ```

2. **สร้างไฟล์ `electron/main.js`:**
   ```javascript
   const { app, BrowserWindow } = require('electron');
   const path = require('path');

   function createWindow() {
     const win = new BrowserWindow({
       width: 1400,
       height: 900,
       backgroundColor: '#121214',
       webPreferences: {
         nodeIntegration: false,
         contextIsolation: true,
       }
     });

     if (process.env.NODE_ENV === 'development') {
       win.loadURL('http://localhost:3000');
     } else {
       win.loadFile(path.join(__dirname, '../dist/index.html'));
     }
   }

   app.whenReady().then(createWindow);
   ```

3. **บิลด์ไฟล์ติดตั้ง (.exe / .dmg):**
   ```bash
   npx electron-builder
   ```

---

## 🌐 ใช้งานเป็น PWA (Progressive Web App) ติดตั้งได้ทันทีไม่ต้องแปลง

โปรเจกต์นี้มี `manifest.json` และ `sw.js` (Service Worker) พร้อมใช้งาน:
- **บนโทรศัพท์ (Android / Chrome):** กดปุ่มเมนู 3 จุดของเบราว์เซอร์ -> เลือก **"เพิ่มลงในหน้าจอหลัก" (Add to Home Screen)** หรือ **"ติดตั้งแอป" (Install App)**
- **บนคอมพิวเตอร์ (Chrome / Edge):** กดไอคอนรูปคอมพิวเตอร์/หน้าจอที่แถบ Address bar ด้านขวาบน -> เลือก **"ติดตั้ง W3.IDP Studio"**
- รองรับการทำงานแบบ Offline และ Fullscreen Mode เหมือนแอปจริง 100%

---

## 📂 โครงสร้างโปรเจกต์ (Project Structure)

```
├── App.tsx                     # Main Application Controller & State
├── index.html                  # HTML Entry Point
├── index.tsx                   # React Root Mounting
├── index.css                   # Global Tailwind & Custom Styles
├── types.ts                    # Core TypeScript Definitions & Models
├── core/
│   ├── engine.ts               # Logic Engine & State Evaluator
│   ├── storage.ts              # LocalStorage & Repository IO
│   └── utils.ts                # Utility functions & ID Generator
├── features/
│   ├── library/LibraryPage.tsx # Story Repository & Project Hub
│   ├── editor/                 # Story & Boardgame Editor Modules
│   ├── characters/             # Character Attributes & Lore Manager
│   ├── board/                  # Interactive Board Simulation
│   ├── location/               # Location Sheets & Nodes
│   ├── cards/                  # Action & Trait Card Designer
│   ├── item/                   # Item & Relic Attributes
│   ├── rules/                  # Ecosystem Rules & Constraints
│   ├── story/                  # Story Flow Nodes & Graph
│   └── play/                   # Real-time Playtesting Sandbox
└── ui/
    ├── components/             # Neumorphic Buttons, Cards, Inputs, Modals
    └── layout/                 # Responsive Split-Screen Layouts
```

ขอให้สนุกกับการสร้างสรรค์และพัฒนาแอปครับ! 🚀
