# Selective Input Principle — W3 Module Agent Application

**Author:** BBX19  **System:** W3 Knowledge  **Category:** Cognitive System Behavior  
**Status:** open-concept  
**Keywords:** input selection, attention, cognitive filtering, system efficiency, unexplained insight

---

## 1. Principle Summary

- ระบบหรือ agent ที่ดี **ต้องไม่รับข้อมูลทุกอย่าง** แต่เน้น “input selection” ตามเป้าหมายขณะนั้น
- Efficiency เกิดจาก “การกรอง” ไม่ใช่ “คิดมาก”
- ทุกกิจกรรมจริงที่เกิดขึ้น = เปลี่ยน state ของระบบ (irreversible)
- Log/memory = เพียงภาพสะท้อน ควรใช้ตรวจสอบ ไม่ใช่ rewrite reality
- ช่องว่าง/Unexplained Point = แหล่งของคำถามใหม่และ innovation
- ทุกคนในระบบ (expert, มือใหม่, คนเกี่ยวข้อง/ไม่เกี่ยวข้อง) มีสิทธิ์ตีความ unexplained point เพื่อกระตุ้นการเติบโตของความรู้
- “ผลลัพธ์จริง/เหตุการณ์” สำคัญกว่าคำตอบที่ถูกเชิงทฤษฎี

---

## 2. Agent Practice Pattern

### a. Input Filtering → Activity

- agent ควรมี filter/throttle เลือก input ที่ “relevant” กับ role หรือวัตถุประสงค์ของโมดูล
    - เช่น module วิเคราะห์: รับอินพุตเฉพาะข้อมูลที่ใช้โยงกับ pattern/goal ปัจจุบัน
    - ตัวอย่าง coding agent: filter เฉพาะ code diff ที่มีผลกับ logic ที่สนใจ
- หากมีเหตุผลเปลี่ยน filter หรือ input selection ให้ log เหตุผล+ผลกระทบทุกกรณี

### b. ปฏิบัติกิจกรรม → Log

- ทุก action, decision step, หรือ activity ควร log event จริง (“เกิดอะไร”) พร้อม input/logic/tool ที่ใช้
- ผลลัพธ์/เหตุการณ์ที่เกิดขึ้น แม้จะยังตีความไม่จบ/ผิด/exception: **บันทึกเสมอ**
- ใช้ format:  
    - Context/Goal
    - Input/Filter
    - Logic/Tool
    - Activity/Result
    - Unexplained Points (flag/comment ได้)

### c. Unexplained Point

- สร้าง field/unexplained-section ใน log หรือ report ทุกโมดูล
- ชี้ให้เห็น gap หรือสิ่งที่ logic ยังอธิบายไม่ได้ (“เหตุผล X → Y ยังไม่ชัด”, “outlier ที่ cause ไม่ตรงกับ assume”)
- agent มีหน้าที่ flag & suggest explore ถัดไป ไม่จำเป็นต้องปิดประเด็นนั้นทันที

### d. เปิดพื้นที่ตีความ/เสนอแนวคิด

- ให้ reviewer, agent อื่น, หรือ user ตั้ง/เสนอข้อสังเกต/ทฤษฎี response ต่อ unexplained point นั้นได้
- เสนอให้ทุก module ทำ retrospective หรือ discussion log รอบ unexplained point อย่างน้อย 1 ครั้งในแต่ละ cycle

---

## 3. ตัวอย่างการนำไปใช้จริงในแต่ละ agent

### ● Copilot-Gm (Governance/Review)
- Input selection: รับเฉพาะ signal/feedback ที่มีผลกับ boundary/structure policy
- Log ทุกรอบ review ที่ policy ไม่ครอบคลุม (unexplained point)
- บันทึก explicit “unexplained/edge-case” เพื่อเสนอใน retrospective

### ● Gemini / ChatGPT (Natural Language/Prompt Agent)
- Filter prompt/context เฉพาะที่เกี่ยวกับ task หรือความเข้าใจมนุษย์-ระบบที่ agent ถนัด
- ถ้า input บางส่วนทำ agent ออกผลผิด/logic ขัด, ให้ log unexplained และเปิดช่อง reviewer เสนอ insight

### ● DeepSeek / Grok (Data/Insight Agent)
- Log unknown correlation/anomaly ที่อธิบายไม่ได้
- ตีความผลที่เกิดขึ้น แม้จะ “ผิด hypothesis” ถ้ายังอธิบาย logic chain ไม่ครบ — log ไว้เป็น unexplained point
- เสริม: ทดสอบ version ที่ different input filter แล้ว map event outcome เปรียบเทียบ

### ● Cast (Context/Conversation Agent)
- ทดลองเปลี่ยน input selection strategy แล้วสังเกตผล/log event
- ชี้ว่าขั้นตอนสนทนาใดทำให้เกิด unexplained point (user intent loss, context drift ฯลฯ)

---

## 4. ข้อเสนอแนะสำหรับการนำไปใช้ในระบบจริง

- ทุก agent/team ตั้ง “input selection rule” ประจำตัว โดนบันทึกใน doc หรือ code header ชัดเจน
- พัฒนา logging format ที่บังคับให้เลือก, อธิบาย, และ flag unexplained point เสมอ
- กำหนดเวลา review unexplained point (weekly/monthly) พร้อมเปิดให้ทุกคนตั้งทฤษฎีใหม่
- “ระบบที่ดีไม่ใช่เข้มงวดกับ input filter อย่างเดียว แต่พร้อมรับมือ event/unexplained insight ที่เกิดขึ้นใหม่ด้วย”

---

## 5. Open Question (สำหรับทีม/agent สะท้อน)

> If a system learns to choose its own inputs, what kind of reality will it ultimately perceive?
> - ทีมควรใช้ question นี้จุดประกาย retrospective, team talk, ให้คิดค้านหรือชี้จุดบอดที่อาจเกิด
> - สนับสนุนให้ทุก agent/team ตอบในมุมของตัวเอง (ไม่ต้องให้มีคำตอบ fix)

---

**หมายเหตุ**  
- สามารถนำ pattern นี้ไปใส่ใน README/summary ของ agent/module ใดก็ได้  
- หากต้องการ bullet summary หรือ log template เฉพาะ agent แจ้งชื่อ agent/module ได้เลยครับ

