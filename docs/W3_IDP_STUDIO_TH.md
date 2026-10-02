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
