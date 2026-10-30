# Personal Sandbox v51 — Story Writer / GitHub Markdown

30 ตุลาคม 2026 · คำขอ BBX19 · ส่งผ่านปุ่มอัปเดตเดิม ไม่เปิด PR

## ผลงาน

- Story → รายการ / เพิ่ม → แตะชื่อตอน หรือเขียนตอนใหม่: เปิดหน้าต่างเขียนเต็มพื้นที่แอป มีชื่อเอกสารและปุ่มบันทึกด้านบน กลับ Story ได้จากปุ่มในหน้าจอหรือทางย้อนกลับ Android
- โหมดเขียน, เขียนคู่พรีวิว, พรีวิว; จอแคบแบ่งบน–ล่าง จอกว้างแบ่งซ้าย–ขวา เลื่อนแต่ละส่วนแยกกัน แถบเครื่องมือปัดแนวนอนได้
- เครื่องมือหัวข้อ ตัวหนา/เอียง/ขีดฆ่า รายการ เช็กลิสต์ อ้างอิง ลิงก์ โค้ด ตาราง ส่วนพับได้ ค้นหา/แทนที่ Undo/Redo และขนาดตัวหนังสือเขียน
- นำเข้า .md / .markdown / .txt UTF-8 ไม่เกิน 4 MB รองรับ BOM และ CRLF เลือกสร้างตอนใหม่ เพิ่มท้าย หรือแทนที่ (ถามยืนยัน) ได้ ย้อนการแทนที่กลับทั้งข้อความและรูปแบบได้
- ส่งออกต้นฉบับตอนที่เปิดเป็น .md / .txt: Android ใช้ ACTION_CREATE_DOCUMENT ด้วย MIME text/markdown หรือ text/plain; เว็บดาวน์โหลด UTF-8 ได้ JSON สำรองโครงการยังใช้ช่องทางเดิม
- GitHub-flavored Markdown: หัวข้อ ตาราง รายการ เช็กลิสต์ ลิงก์ ขีดฆ่า โค้ด และ HTML ที่ปลอดภัย เช่น details/summary ตัวอ่านใช้ react-markdown + remark-gfm + rehype-raw + rehype-sanitize และบรรจุแบบ offline chunk ภายในแอป
- ภาพอ้างอิงแสดงคำบรรยายแทน ไม่โหลดภาพภายนอกอัตโนมัติ ลิงก์เว็บไซต์เปิดผ่านการแตะ ไฟล์ Markdown ไม่ได้แนบไฟล์ภาพมาอัตโนมัติในรุ่นนี้
- ตอนเดิมยังเก็บรูปแบบ legacy; ตอนใหม่ Markdown; bodyFormat เป็นข้อมูลเสริม ไม่เปลี่ยน StoryNode ID, choices หรือส่วนอื่น โครงการทั้งสามโหมดและ JSON backup เก็บข้อมูลได้
- บันทึกอัตโนมัติเดิมทำงานต่อ มีสถานะในหน้าต่างเขียน เมื่อเขียนลง storage ไม่สำเร็จจะไม่ปิดหน้าต่างหรือสร้างตอนใหม่ทับงานค้าง และยังส่งออกสำเนาได้
- เพิ่มคู่มือไทยหัวข้อ 8 และ tests/storyDocuments.ts; ปรับ Button ให้ส่งผ่าน id/DOM props และ MouseEvent ตามชนิดจริง พร้อมแก้ effect cleanup ให้ผ่าน React type checks

## ตรวจสอบ

- npm run lint และ npm run build ผ่าน; parser Markdown แยก lazy chunk เพื่อลดโค้ดเริ่มต้นของแอป
- tests/storyDocuments.ts: UTF-8/BOM/CRLF, ปฏิเสธชนิดไฟล์/ขนาด/encoding ผิด, legacy choices และ backup round trip ครบ library/bookcraft/concept ผ่าน
- tests/authoringSmoke.tsx เดิม: ทุกหน้าและ runtimes/inventory/persistence/backup/isolation ผ่าน
- Chromium หน้าสัมผัส: หน้าต่างเต็มพื้นที่และส่วนเขียน/พรีวิวไม่ซ้อน ที่ 360/640/1000px; ข้อมูลไทย ตาราง เช็กลิสต์ โค้ด details แสดงได้
- Bold, Undo/Redo, ค้นหา/แทนที่, นำเข้าใหม่/เพิ่มท้าย/แทนที่, Undo คืนรูปแบบ, ส่งออก .md/.txt และอ่านไฟล์ดาวน์โหลดกลับตรงต้นฉบับ ผ่าน
- จำลอง storage quota ล้มเหลว: ปิดไม่ได้/ไม่สร้างตอนใหม่ ต้นฉบับส่งออกได้ หลังคืน storage บันทึกและกลับ Story ได้
- จำลอง AndroidBridge: ส่งชื่อไฟล์/MIME/payload ถูกต้อง และ back event กลับ Story ได้; ตัวอ่าน Playtest แสดง Markdown ได้
- ป้องกัน HTML script/event/style และไม่มี remote image requests ใน fixture; ไม่พบ uncaught page errors

ตรวจด้วยเบราว์เซอร์และ native build pipeline การใช้ Android document picker และปุ่มย้อนกลับบนเครื่อง OPPO จริงให้เจ้าของตรวจต่อหลังอัปเดต

## อ้างอิงไลบรารี

- https://github.com/remarkjs/react-markdown
- https://github.com/remarkjs/remark-gfm
- https://github.com/rehypejs/rehype-sanitize
