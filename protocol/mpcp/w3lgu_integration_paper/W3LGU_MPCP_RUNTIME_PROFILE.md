# W3Lgu-MPCP Runtime Profile

## 1. Purpose
เอกสารนี้กำหนด W3Lgu profile สำหรับ runtime ของ MPCP เพื่อใช้กับ:
- modew messages
- paper binding
- condien binding
- state exchange
- continuity signaling
- result linkage
- quick runtime visibility

เป้าหมายคือ:
- ให้ runtime พูดภาษาเดียวกับ ecosystem
- ทำให้ trace/debug ง่าย
- ไม่ทำลาย boundary
- ไม่ทำให้ signal แทน truth

---

## 2. Core Rule
Runtime profile ต้อง:
- สั้น
- ชัด
- trace ได้
- bind กับ Paper/Condien/Modew ได้
- อยู่ใต้ ROT
- ไม่ตกแต่ง result truth

---

## 3. Core Fields
- `TIME`
- `TASK`
- `MODEW`
- `PAPER`
- `CONDIEN`
- `STATE`
- `READ`
- `DENY`
- `OUTPUT`
- `TRACE`
- `TRACE_LINK`
- `CONTINUITY`
- `REBASE`
- `ENV`
- `RESULT`

---

## 4. Runtime Exchange Example

```text
TASK:report
MODEW:REPORT
PAPER:daily_summary
CONDIEN:CORE
READ:LAYER_B,LAYER_C
STATE:run
TRACE:required
CONTINUITY:carry-forward
OUTPUT:short_report
ENV:preserve
```

ความหมาย:
- มี task `report`
- modew ที่ execute คือ `REPORT`
- bind กับ paper `daily_summary`
- bind กับ condien `CORE`
- อ่าน layer B,C
- runtime state คือ run
- trace ต้องครบ
- continuity แบบ carry-forward
- มี output target
- preserve environment

---

## 5. Result Linkage Example

```text
RESULT:recorded
MODEW:REPORT
CONDIEN:CORE
TRACE_LINK:active
ENV:non-reduced
```

ข้อความนี้ใช้เพื่อบอกว่า:
- result ถูก record แล้ว
- ผูกกับ modew/condien ไหน
- trace link ยัง active
- environment ถูกเก็บแบบ non-reduced

---

## 6. Fast Signal Example

```text
TIME:now,MODEW:Auth,STATE:done
```

นี่คือ runtime quick signal  
มีไว้เพื่อให้เห็นเร็ว  
ไม่ใช่ replacement ของ result profile หรือ governance truth

---

## 7. Rules
1. Runtime profile ใช้สำหรับ exchange ไม่ใช่ governance law
2. ทุกข้อความต้องเคารพ Paper และ ROT
3. Result ต้องไม่ถูกตกแต่งเพื่อซ่อน misalignment
4. Signal แบบเร็วใช้ได้ แต่ห้ามแทน trace
5. Runtime messages ต้องใช้ W3Lgu profile นี้เป็น canonical form
6. ห้ามส่ง raw external payload ข้าม runtime boundary โดยไม่ normalize

---

## 8. Final Summary
W3Lgu-MPCP-Runtime profile เป็นภาษากลางสำหรับ runtime exchange ของ MPCP  
มีไว้เพื่อให้ modew, paper, condien, result linkage และ continuity พูดร่วมกันได้  
โดยยังรักษา boundary, traceability, และ environment truth
