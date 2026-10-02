# W3.IDP Studio — w3openland

Status: imported-source staging  
Source: Google AI Studio export supplied by BBX19  
Target: `blueprints/GGinventory/w3openland/`

## Purpose

พื้นที่นี้ใช้เก็บต้นฉบับ W3.IDP Studio ซึ่งเป็น Story & Boardgame Ecosystem Editor / sandbox สำหรับงาน W3 Openland

โครงสร้างต้นฉบับที่ตรวจพบเป็น React + TypeScript + Vite และมีส่วนหลัก เช่น:

- `core/` — engine, storage, utilities
- `features/` — agent, board, cards, characters, dashboard, editor, event/events, item, library, location, play, rules, story
- `ui/` — shared components และ layout
- `App.tsx`, `index.tsx`, `types.ts` — application entry/state/model
- `manifest.json`, `sw.js` — PWA surface

## Import boundary

ไฟล์ export จาก AI Studio ถูกตรวจเบื้องต้นก่อนนำเข้า

ไม่ควรนำสิ่งต่อไปนี้เข้า source tree:
- `node_modules/`, `dist/`, cache
- secret / API key / credential / `.env.local`
- exported ZIP ที่ซ้อนอยู่ใน `public/`
- `migrated_prompt_history/` ซึ่งเป็นประวัติ prompt/export และไม่จำเป็นต่อ runtime

การตัดรายการเหล่านี้ออกไม่ใช่การเปลี่ยน logic ของตัวแอป แต่เป็น boundary สำหรับ source repository

## Runtime

ต้นฉบับกำหนด:
```bash
npm install
npm run dev
npm run build
```

ดูคู่มือภาษาไทย: `docs/W3_IDP_STUDIO_TH.md`
