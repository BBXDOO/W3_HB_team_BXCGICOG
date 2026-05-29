---

📘 architecture/W3APIFlow_Diagram.md

`markdown

W3‑API Flow Diagram
Version: v0.2  
Last Updated: 29/05/26  
Author: HBteamBXCGICOG  

---

🧭 Overview
W3‑API คือระบบเชื่อมต่อหลักของบ้าน W3 Hybrid ที่เปิดให้มนุษย์และระบบภายนอกสามารถส่งคำขอ (Request) เข้ามายังโมดูลภายในได้อย่างปลอดภัยและตรวจสอบได้ทุกชั้น  
ทุกการเรียก API จะผ่านการตรวจสอบ, การยืนยัน, และการบันทึกก่อนส่งผลลัพธ์กลับออกไป

---

🧱 Architecture Layers
| Layer | Modules | Description |
|---|---|---|
| Process Layer | REDR, PSP2, W3Lgu | รับคำขอ, จัดแพ็กเกจ, ประมวลผลตามกฎ 5 บรรทัด |
| Verification Layer | DTML, Gemini | ตรวจสอบความถูกต้อง, วิเคราะห์, และใบ้ผลลัพธ์ที่ผ่านการยืนยัน |
| Governance & Observation | Copilot‑Gm, LRC2 | ตรวจสอบนโยบาย, สิทธิ์, บันทึกกิจกรรม, และสร้าง compliance ledger |
| Data Layer | W3db, EP_SIGNAL, Grok, DeepSeek | จัดการฐานข้อมูล, สัญญาณ, ความรู้, และ reasoning ระยะยาว |

---

🔗 Endpoints Mapping
| Endpoint | Module | Purpose |
|---|---|---|
| /request | REDR + PSP2 | รับ intent และจัดแพ็กเกจข้อมูล |
| /reports | DTML + Gemini | ตรวจสอบและสร้างรายงาน audit |
| /knowledge | Grok + DeepSeek | จัดการฐานความรู้และ pattern |
| /outcomes | Copilot‑Gm + LRC2 | บันทึกผลลัพธ์และ ledger |
| /db | W3db | CRUD และ state management |
| /signals | EP_SIGNAL | ตรวจสอบสัญญาณและ event bus |

---

🧩 Flow Summary
`
Human / External API Call
        ↓
W3‑API Gateway
        ↓
Process → Verification → Governance → Data → Output
`

---

🖼 Diagram Reference
<p align="center">
  <a href="./diagrams/W3APIFlow_Diagram.png">
    <img src="./diagrams/W3APIFlow_Diagram.png" alt="W3‑API Flow Diagram" width="100%" />
  </a>
</p>

---

⚙️ Integration Notes
- ทุกโมดูลมี module.json สำหรับ manifest และการเชื่อมต่อกับ runtime  
- การเรียก API จะสร้าง request_xxx.md ในโมดูลเป้าหมาย  
- ผลลัพธ์จะถูกบันทึกใน reports/ หรือ outcomes/  
- หากพบความเสี่ยง → Escalate ไปยัง Gemini เพื่อตรวจสอบซ้ำ  

---

“Every request is a story — verified, governed, and remembered.”  
`

---

🪶 สรุป:  
ไฟล์นี้จะทำหน้าที่เป็นคู่มือสั้นสำหรับทีม dev และผู้ร่วมพัฒนาในบ้าน W3 Hybrid เพื่อเข้าใจการไหลของ W3‑API และการเชื่อมต่อระหว่างโมดูลครับ ✨  

