# คู่มือ W3.IDP Studio (w3openland)

## 1. ตำแหน่ง

Source ของ W3.IDP Studio ใช้พื้นที่:

`blueprints/GGinventory/w3openland/`

Branch หลักสำหรับงานชุดนี้: `refactor/v0.2`

## 2. ระบบนี้คืออะไร

จาก source export ปัจจุบัน W3.IDP Studio เป็นแอป React + TypeScript + Vite สำหรับสร้างและจัดการ Story / Boardgame Ecosystem โดยมีส่วนของ Characters, Board/Locations, Cards/Items, Rules, Story Flow และ Playtest

เอกสารนี้อธิบายเฉพาะสิ่งที่ตรวจพบจาก source export ปัจจุบัน ไม่ถือว่าเป็นนิยามถาวรของ W3 Openland หรือ W3 ทั้งระบบ

## 3. ความต้องการ

- Node.js 18 ขึ้นไป (ต้นฉบับแนะนำ Node.js 20 LTS)
- npm

## 4. ติดตั้ง

จาก root repository:

```bash
cd blueprints/GGinventory/w3openland
npm install
```

## 5. รันแบบ Development

```bash
npm run dev
```

Vite จะแสดง URL ที่ใช้งานได้ใน terminal

## 6. ตรวจ TypeScript

```bash
npm run lint
```

ใน package ปัจจุบันคำสั่งนี้เรียก `tsc --noEmit`

## 7. Build

```bash
npm run build
```

ผล build จะอยู่ใน `dist/` และไม่ควร commit กลับ repository

## 8. โครงสร้างสำคัญ

- `core/engine.ts` — logic/state evaluator
- `core/storage.ts` — storage/repository IO
- `core/utils.ts` — utility
- `features/library/` — project/library surface
- `features/editor/` — editor shell/navigation
- `features/board/` — board simulation
- `features/characters/` — character data/UI
- `features/cards/` และ `features/item/` — cards/items
- `features/rules/` — rules
- `features/story/` — story flow
- `features/play/` — playtest sandbox
- `ui/` — shared UI

## 9. Import / Security boundary

ก่อนนำ source จาก AI Studio เข้า W3 ให้ตรวจ credential และไฟล์ส่วนตัวเสมอ

รอบนำเข้าปัจจุบันกำหนดไม่ให้รวม:
- `node_modules/`, `dist/`, cache
- secret, API key, credential, local env
- ZIP source ที่ซ้อนอยู่ภายใน export
- `migrated_prompt_history/` เพราะไม่ใช่ runtime source และอาจมีข้อมูลจากประวัติการทำงาน

ห้ามรายงานว่า import สำเร็จจนกว่าไฟล์ source จะอยู่ใน branch และตรวจ commit ได้จริง

## 10. Mobile / PWA

ต้นฉบับมี `manifest.json` และ `sw.js` สำหรับ PWA ส่วนการทำ Android/iOS native ผ่าน Capacitor เป็นขั้นตอนเพิ่มเติม ไม่ใช่ dependency ที่ติดตั้งอยู่ใน source ปัจจุบัน

## 11. หมายเหตุ

คู่มือนี้ต้องอัปเดตเมื่อโครงสร้าง, build command, runtime หรือขอบเขตของ W3.IDP Studio เปลี่ยน


## 12. ผลการตรวจใช้งานจริงบน Android / Termux

วันที่ตรวจ: 2026-10-03

Environment ที่ใช้ตรวจ:
- Android + Termux
- Node.js 26.3.1
- Vite 6.4.3
- Branch: `refactor/v0.2`
- Path: `blueprints/GGinventory/w3openland/`

ผลการตรวจตามลำดับ:

1. `npm install` — **PASS**
   - ติดตั้ง 118 packages และตรวจ 119 packages สำเร็จ
   - npm รายงาน 5 vulnerabilities (2 moderate, 3 high) ซึ่งยังไม่ได้แก้ในรอบ baseline นี้
   - มีคำเตือน allow-scripts สำหรับ `@google/genai`, `esbuild`, `protobufjs`; ยังไม่เปลี่ยน dependency/config ในรอบนี้

2. `npm run lint` — **PASS**
   - `tsc --noEmit` จบโดยไม่มี TypeScript error

3. `npm run build` — **PASS**
   - Vite production build สำเร็จ
   - 61 modules transformed
   - build time ประมาณ 3.94s ในเครื่องที่ทดสอบ
   - มี warning ว่า JavaScript chunk หลัง minification ขนาดประมาณ 628.44 kB มากกว่า 500 kB; เป็น optimization warning ไม่ใช่ build failure

4. `npm run dev` — **PASS**
   - Vite dev server ready
   - เปิดผ่าน `http://localhost:3000/` ได้จริงบน browser ในโทรศัพท์

5. Browser/UI smoke test — **PASS (basic)**
   - UI ของ W3.IDP Studio แสดงผลจริง
   - เปิด project/editor surface ได้
   - เห็นเมนู Story, Characters, Cards, Board, Locations, Items, Events, Rules, Playtest และ Nexus AI
   - การแสดงผลบน mobile มีลักษณะ desktop-width/แนวนอนกว้าง จึงยังมีงาน responsive UX ที่ควรประเมินแยกต่างหาก

### สถานะที่ยังไม่ยืนยัน

ผลข้างต้นยังไม่ถือเป็นหลักฐานว่า:
- Nexus AI / Gemini API ทำงานสำเร็จ
- ทุก feature และทุก editor flow ผ่าน functional test
- PWA install/offline ผ่าน
- persistence/import/export ผ่านทุกกรณี
- dependency vulnerabilities ได้รับการแก้แล้ว

Baseline ปัจจุบันจึงยืนยันได้ว่า **source ติดตั้งได้, TypeScript ผ่าน, production build ได้ และ basic runtime/UI เปิดใช้งานจริงบน Android + Termux ได้**


## 13. คู่มือใช้งานผ่าน Termux (Android)

ส่วนนี้เป็นวิธีใช้งาน W3.IDP Studio ผ่าน Termux โดยตรง โดยไม่ต้องติดตั้ง PWA

### 13.1 เตรียมเครื่องครั้งแรก

ติดตั้ง Git และ Node.js:

```bash
pkg update
pkg install git nodejs -y
```

Clone repository โดยใช้ branch ของ W3:

```bash
cd ~
git clone -b refactor/v0.2 https://github.com/BBXDOO/W3_HB_team_BXCGICOG.git
```

เข้าโฟลเดอร์ W3.IDP Studio:

```bash
cd ~/W3_HB_team_BXCGICOG/blueprints/GGinventory/w3openland
```

ติดตั้ง dependencies:

```bash
npm install
```

ขั้นตอน `npm install` ใช้หลัก ๆ ในการเตรียมครั้งแรก หรือเมื่อ dependencies ใน `package.json` / lockfile เปลี่ยน

### 13.2 เปิดใช้งานตามปกติ

ครั้งต่อ ๆ ไปไม่ต้อง clone และไม่ต้อง `npm install` ใหม่ทุกครั้ง

เปิด Termux แล้วรัน:

```bash
cd ~/W3_HB_team_BXCGICOG/blueprints/GGinventory/w3openland
npm run dev
```

เมื่อ Vite แสดง:

```text
Local: http://localhost:3000/
```

ให้เปิด browser บนโทรศัพท์แล้วเข้า:

`http://localhost:3000/`

ระหว่างใช้งาน **อย่าปิด process ของ Termux ที่กำลังรัน Vite** เพราะ browser ใช้ server ตัวนี้อยู่

### 13.3 หยุดระบบ

กลับมาที่ Termux แล้วกด:

```text
Ctrl + C
```

เมื่อ prompt ของ shell กลับมา แปลว่า dev server หยุดแล้ว

### 13.4 อัปเดต source จาก GitHub

ก่อนเริ่มงานในวันที่ต้องการ source ล่าสุด:

```bash
cd ~/W3_HB_team_BXCGICOG
git switch refactor/v0.2
git pull
```

จากนั้นกลับเข้า Studio:

```bash
cd blueprints/GGinventory/w3openland
```

ถ้า `package.json` หรือ `package-lock.json` เปลี่ยน ให้รัน:

```bash
npm install
```

แล้วเปิดระบบ:

```bash
npm run dev
```

### 13.5 ตรวจ source ก่อนใช้งานหรือหลังอัปเดต

ตรวจ TypeScript:

```bash
npm run lint
```

ตรวจ production build:

```bash
npm run build
```

ทั้งสองคำสั่งไม่จำเป็นต้องรันทุกครั้งที่เปิด Studio แต่เหมาะสำหรับตรวจหลัง source/dependency มีการเปลี่ยนแปลง

### 13.6 คำสั่งใช้งานประจำแบบสั้น

```bash
cd ~/W3_HB_team_BXCGICOG/blueprints/GGinventory/w3openland
npm run dev
```

Browser:

```text
http://localhost:3000/
```

หยุด:

```text
Ctrl + C
```

### 13.7 ข้อควรระวัง

- ไม่ต้อง `git clone` ใหม่ทุกครั้ง
- ไม่ต้อง `npm install` ใหม่ทุกครั้ง
- อย่ารัน `npm audit fix` โดยอัตโนมัติเพียงเพราะ npm แสดง vulnerability; ให้ตรวจผลกระทบและ dependency ก่อน
- อย่า commit API key, credential หรือไฟล์ environment ที่มี secret
- หาก `npm run dev` ยังทำงานอยู่ การปิด/kill Termux process จะทำให้ `localhost:3000` หยุดตาม
- คู่มือนี้เป็นการใช้งานผ่าน Termux + browser และไม่พึ่งการติดตั้ง PWA
