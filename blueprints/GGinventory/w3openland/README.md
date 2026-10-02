# W3.IDP Studio — W3 Openland

> **Path:** `blueprints/GGinventory/w3openland/`  
> **Branch:** `refactor/v0.2`  
> **Status:** Source imported / validation pending  
> **Origin:** Google AI Studio export supplied by BBX19

W3.IDP Studio เป็นโปรเจกต์ React + TypeScript + Vite สำหรับสร้างและจัดการ Story / Boardgame Ecosystem โดย source ปัจจุบันมีส่วนของ Characters, Boards & Locations, Cards & Items, Rules, Story Flow และ Playtest

README นี้อธิบาย **source ที่อยู่ใน repository ปัจจุบัน** และวิธีเรียกใช้งานเบื้องต้น โดยไม่ถือว่ารายละเอียดของ implementation ปัจจุบันเป็นนิยามถาวรของ W3 Openland

---

## Quick Start

ต้องมี Node.js และ npm ก่อนใช้งาน

```bash
cd blueprints/GGinventory/w3openland
npm install
npm run dev
```

Vite ถูกกำหนดให้ใช้ port `3000` และ host `0.0.0.0`

### ตรวจ TypeScript

```bash
npm run lint
```

คำสั่ง `lint` ใน source ปัจจุบันคือ `tsc --noEmit`

### Build

```bash
npm run build
```

ผลลัพธ์ของ Vite จะถูกสร้างใน `dist/`

> **หมายเหตุสถานะ:** การมี source อยู่ใน repository ไม่ได้หมายความว่า build ผ่านแล้ว การตรวจ build/typecheck ต้องบันทึกตามผลที่เกิดขึ้นจริง

---

## Project Structure

```text
w3openland/
├── App.tsx
├── index.html
├── index.tsx
├── index.css
├── types.ts
├── core/
│   ├── engine.ts
│   ├── storage.ts
│   └── utils.ts
├── features/
│   ├── agent/
│   ├── board/
│   ├── cards/
│   ├── characters/
│   ├── dashboard/
│   ├── editor/
│   ├── event/
│   ├── events/
│   ├── item/
│   ├── library/
│   ├── location/
│   ├── play/
│   ├── rules/
│   └── story/
├── reports/
├── ui/
├── manifest.json
├── sw.js
├── package.json
├── package-lock.json
├── tsconfig.json
└── vite.config.ts
```

### Runtime / package ที่ยืนยันจาก `package.json`

- React `^19.2.3`
- React DOM `^19.2.3`
- Vite `^6.2.0`
- TypeScript `~5.8.2`
- Tailwind CSS `^4.3.0`
- `@google/genai` `^1.38.0`

Scripts:

```text
npm run dev      -> vite
npm run build    -> vite build
npm run preview  -> vite preview
npm run lint     -> tsc --noEmit
npm run pack:zip -> python3 build_zip.py
```

---

## Gemini API configuration

`vite.config.ts` อ่านค่า `GEMINI_API_KEY` จาก environment แล้วส่งให้ application ผ่าน `process.env.API_KEY` และ `process.env.GEMINI_API_KEY`

ห้าม commit API key จริงลง repository

ตัวอย่าง local environment:

```bash
export GEMINI_API_KEY="YOUR_KEY"
npm run dev
```

หรือใช้ไฟล์ environment สำหรับเครื่อง local โดยต้องตรวจว่าไฟล์ดังกล่าวถูก ignore และไม่มี secret ถูก commit

---

## PWA

Source มี `manifest.json` และ `sw.js` อยู่แล้ว จึงมีองค์ประกอบสำหรับ PWA

อย่างไรก็ตาม การมี manifest/service worker **ไม่ใช่หลักฐานเพียงพอว่า offline/PWA install ทำงานครบทุกกรณี** ต้องตรวจจาก build และ browser จริงก่อนรายงานสถานะว่า ready

---

## Mobile / Desktop

Capacitor และ Electron **ไม่ได้เป็น dependency ของ source ปัจจุบัน** ดังนั้น Android/iOS/Desktop packaging ถือเป็นขั้นตอนต่อยอด ไม่ใช่ runtime ที่ยืนยันแล้วของ repository ชุดนี้

หากจะเพิ่มในภายหลัง ควรทำเป็นงานแยกและบันทึก dependency/config ที่เพิ่มเข้ามาให้ตรวจสอบได้

---

## Import Boundary

การนำ source จาก AI Studio รอบนี้ตั้งใจไม่นำรายการต่อไปนี้เข้ามา:

- `migrated_prompt_history/` — ประวัติ prompt ไม่ใช่ runtime source
- `public/` จาก export ชุดนี้ — มีเพียง source ZIP ซ้อน
- `bun.lock` — ไฟล์ export เป็น 0 byte
- `node_modules/`, `dist/`, cache — generated/dependency output
- secret, API key, credential และ local environment files

การตัดรายการเหล่านี้ออกไม่เปลี่ยน application source ที่ใช้ใน runtime ตามโครงสร้างที่ตรวจพบ

---

## Source / Evidence Rule

สำหรับพื้นที่นี้ให้แยกสถานะออกจากกัน:

```text
Source present != Typecheck passed
Typecheck passed != Build passed
Build passed != Runtime verified
Runtime verified != W3 integration completed
```

เมื่อมีการเปลี่ยนแปลง source, dependency, build process หรือขอบเขตของ W3.IDP Studio ให้ปรับ README และคู่มือที่เกี่ยวข้องตามหลักฐานล่าสุด

---

## เอกสารภาษาไทย

คู่มือการติดตั้ง/ใช้งานและขอบเขตการนำเข้า:

`docs/W3_IDP_STUDIO_TH.md`

---

## Current checkpoint

- Source export: **received**
- Source placement: **imported into `w3openland/`**
- Import exclusions: **applied by upload selection**
- Secret value committed: **ยังไม่พบจากไฟล์ config ที่ตรวจ**
- TypeScript check: **pending verification**
- Production build: **pending verification**
- Runtime/browser verification: **pending verification**

ขั้นถัดไปคือการตรวจ source tree ที่อัปโหลดจริง จากนั้นจึงรัน typecheck/build และบันทึกผลตามจริง
