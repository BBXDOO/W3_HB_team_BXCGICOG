# W3Lgu-MPCP Blueprint Profile

## 1. Purpose
เอกสารนี้กำหนด W3Lgu profile สำหรับ blueprint เชิงระบบของ MPCP

Blueprint มีหน้าที่เป็น:
- แบบแผน
- แผนการประกอบระบบ
- รูปแบบ setup
- การเลือก target/lib/bridge/mode/partition
- เอกสารที่ใช้ซ้ำได้

Blueprint ไม่ใช่:
- runtime log
- source code
- event packet
- one-time command script

---

## 2. Core Rule
**Blueprint defines setup, not execution.**

W3Lgu-MPCP-Blueprint profile จึงถูกใช้เพื่อสื่อสาร:
- รูปร่างของระบบ
- ตัวเลือกที่ระบบต้องใช้
- compatibility ที่ต้องเคารพ
- boundary/tracing/environment expectations

ไม่ใช่เพื่อกำหนด execution step-by-step

---

## 3. Recommended Fields
- `NAME`
- `TARGET`
- `MODE`
- `LIB`
- `CORE`
- `BRIDGE`
- `OPTIONAL`
- `PARTITION`
- `ROLE`
- `BOUNDARY`
- `TRACE`
- `ENV`

---

## 4. Basic Example

```text
NAME:MPCP_CORE
TARGET:android
MODE:min
LIB:fs,store,net
BRIDGE:android
PARTITION:A,B,C
BOUNDARY:rot-governed
TRACE:required
ENV:preserve
```

ความหมาย:
- blueprint ชื่อ `MPCP_CORE`
- เป้าหมาย Android
- mode แบบ minimal
- ใช้ lib ตามชุดที่ระบุ
- ใช้ bridge แบบ android
- มี partition ที่ประกาศไว้
- อยู่ใต้ ROT boundary
- trace ต้องมี
- environment ต้อง preserve

---

## 5. Condien-Oriented Example

```text
NAME:CONDIEN_RUNTIME
TARGET:linux
MODE:full
LIB:file,event,storage
BRIDGE:linux
OPTIONAL:debug,merge-view
ROLE:meaning_state_layer
BOUNDARY:paper-strict
TRACE:cause-action-result
ENV:non-reduced
```

ความหมาย:
- blueprint นี้เอียงไปทาง Condien runtime
- target เป็น Linux
- เปิด optional views บางชนิด
- role เชิงระบบเกี่ยวกับ meaning/state
- ต้องรักษา trace แบบ cause-action-result
- environment ต้องเก็บแบบ non-reduced

---

## 6. Rules
1. Blueprint ต้องเป็น declarative
2. Blueprint ต้อง reusable
3. ห้ามใส่ runtime log
4. ห้ามใส่ one-time command
5. ห้ามยัด execution logic ลง blueprint
6. Blueprint ต้องใช้ W3Lgu profile นี้เป็น canonical form
7. Blueprint ต้องชัดว่าเป็น “แผน” ไม่ใช่ “การกระทำ”

---

## 7. Final Summary
W3Lgu-MPCP-Blueprint profile คือรูปแบบภาษากลางสำหรับ blueprint ของ MPCP  
มีไว้เพื่อให้ระบบหลายส่วนใช้แผนร่วมกันได้ โดยไม่สับสนกับ runtime หรือ source code
