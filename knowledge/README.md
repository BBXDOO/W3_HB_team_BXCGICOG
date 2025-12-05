# Knowledge folder — รายการไฟล์ (snapshot)

ไฟล์/โฟลเดอร์ชุดนี้เป็นเก็บชั้นความรู้เชิง abstract — ไม่มี logic หรือ data ที่มีความลับ
สร้างไว้เพื่อ:
- ให้โครงสร้างที่ชัดเจนสำหรับโมดูลที่สร้างเนื้อหาทางความรู้
- เป็นแหล่งอ้างอิงและ placeholder เพื่อให้โฟลเดอร์ถูก track ใน repo

---

## โครงสร้าง (รายการไฟล์ที่ควรมี)
1. `knowledge/placeholder.md`  
   - จุดประสงค์: ทำให้โฟลเดอร์ `knowledge/` ถูก track (โฟลเดอร์ไม่ว่าง)
   - Suggested content (copy → create file):
     ```
     # Placeholder

     This placeholder exists to ensure the folder is tracked in the repo.
     Add module-level docs and outputs here when available.
     ```
   - Commit message: `chore: add knowledge/placeholder.md`

2. `knowledge/narratives/placeholder.md`  
   - จุดประสงค์: โฟลเดอร์สำหรับรายงานเชิง narrative, human-facing summaries
   - Suggested content:
     ```
     # Narratives placeholder

     Place human-readable narratives, story summaries and contextual writeups here.
     ```
   - Commit message: `chore: add knowledge/narratives/placeholder.md`

3. `knowledge/patterns.md`  
   - จุดประสงค์: เก็บแพตเทิร์นหรือ schema ของ knowledge artifacts (json schema, example patterns)
   - Suggested content:
     ```
     # Knowledge Patterns

     - pattern-1: description
     - pattern-2: description

     (Add pattern definitions and example JSON snippets for knowledge outputs)
     ```
   - Commit message: `chore: add knowledge/patterns.md`

4. `knowledge/index.md` (หรือ `knowledge/README.md`)  
   - จุดประสงค์: สรุปภาพรวมของโฟลเดอร์นี้ (แนะนำให้ใช้ไฟล์นี้เป็นหน้า entry สำหรับคนดู)
   - Suggested content (เป็นหน้ารวม — สามารถใช้ไฟล์นี้แทนหรือคู่กับไฟล์ที่ผมให้ตอนต้น):
     ```
     # Knowledge — Overview

     This folder contains human-focused artifacts produced by knowledge modules:
     - /knowledge/narratives/ : readable summaries and stories
     - /knowledge/patterns.md : canonical patterns and schemas
     ```
   - Commit message: `chore: add knowledge/index.md`
