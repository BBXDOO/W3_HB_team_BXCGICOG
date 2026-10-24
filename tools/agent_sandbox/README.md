# MPCP + W3Lgu Agent Sandbox

เครื่องมือให้เอเจนท์ทดลองกับ runtime จริงใน W3 ด้วย Python 3.10+ โดยไม่ต้องติดตั้ง REA หรือโมเดล AI เพิ่ม

## เริ่มใช้งาน

รันจาก root ของรีโป้ ใช้โฟลเดอร์ผลลัพธ์ชื่อใหม่ทุกครั้ง:

```sh
python tools/mpcp_sandbox.py --request tools/agent_sandbox/local_setup.json --output local_workspace/trial-001
python tools/mpcp_sandbox.py --request tools/agent_sandbox/local_setup.json --output local_workspace/trial-002 --execute
```

คำสั่งแรกคืน `WAIT` เพราะยังไม่เปิดสิทธิ์สร้าง setup ส่วนคำสั่งที่สองอนุญาตเฉพาะความสามารถ `sandbox_materialize` ในพื้นที่ทดลอง เป็นสิทธิ์จากการเรียก CLI ไม่ใช่การอ้างว่า BBX19 อนุมัติ deployment

Exit code: `0` = SUCCESS พร้อมตรวจชิ้นงานจริง, `2` = WAIT/STOP/ผลยังไม่ผ่าน, `1` = สร้างพื้นที่ทดลองไม่ได้

## วงจรที่เกิดจริง

1. สำเนาไฟล์ที่ Git ติดตามใน `protocol/` และ `src/` รวมการแก้ไฟล์เหล่านั้นใน working tree พร้อม SHA-256 ของแต่ละไฟล์
2. เปิด Python subprocess ใน working directory ใหม่ ไม่ส่ง environment ทั้งหมดเข้าไป
3. W3Lgu อ่าน event, จัดห้อง/PX, ทำ REDR → PSP2 → DTML → LRC2
4. ถ้า DTML เป็น STOP หรือ REVIEW จะไม่เรียก Modew; REVIEW คืน WAIT
5. ผ่าน ENV gateway และ ExecutionAgreement สำหรับขอบเขตทดลองเท่านั้น
6. MPCP เรียก Modew จริง เพื่อตรวจ Blueprint สร้าง partition directories และ `artifacts/setup.json`
7. ตรวจ hash ของ manifest และตรวจว่า directories มีจริง แล้วบันทึกผลกลับผ่าน W3Lgu/LRC2
8. เก็บผลและตรวจ hash ของต้นฉบับกับสำเนาหลังรัน

Blueprint ยังคงเป็นแผน การสร้าง filesystem เป็นหน้าที่ของ Modew แยกต่างหาก

## ผลลัพธ์ที่เอเจนท์อ่านได้

| ที่อยู่ใน output | เนื้อหา |
|---|---|
| `request.json` | คำขอต้นฉบับ |
| `result.json` | state, gate, MPCP result, ENV/Cross-L return, executor trace, LRC2, hashes, ช่องว่างที่เหลือ |
| `worker.log` | log และ exception รวมกรณี worker ล้ม |
| `source/` | สำเนา source ที่ใช้จริงในรอบนั้น |
| `workspace/artifacts/` | partition directories และ manifest เมื่อผ่าน |

รับ JSON เฉพาะ `blueprint` และ `event` ไม่รับ shell command หรือชื่อ Python module จากข้อมูลคำขอ ใช้ `--source-root` เพื่อเลือก checkout ที่เอเจนท์กำลังปรับ แล้วรันซ้ำด้วย output ใหม่เพื่อเปรียบเทียบก่อน/หลัง รหัส `revision` บอก base commit; hashes บอก source bytes ที่ใช้จริง ไม่สรุปว่า working tree ตรงกับ commit โดยอัตโนมัติ

เครื่องมือนี้ไม่แก้โค้ดให้อัตโนมัติ เอเจนท์ต้องอ่านหลักฐาน แก้ source ในสาขาทดลอง ตรวจผล แล้วเสนอ diff เพื่อพิจารณารวมงาน

## ขอบเขตรอบแรกและสิ่งที่ยังขาด

- รองรับ `TARGET:local`, `LIB:file,storage`, ชื่อ partition แบบง่าย และ fields ตามตัวอย่างเท่านั้น ความสามารถที่ไม่รองรับต้องคืน STOP
- `MODE` ใช้โหมด foundation เดิม เช่น `plan`, `observe`, `review` ไม่แปลง `min/full/stable/test` เป็น `observe` อย่างเงียบ ๆ โหมดติดตั้งจาก paper ยังต้องนิยาม profile ให้ตรงกับ runtime
- ไม่ติดตั้ง library, ไม่ build APK, ไม่ deploy, ไม่เชื่อม external agent และไม่เขียน W3DB จริง หลักฐานจาก gateway เป็น evidence candidate
- การแยกสำเนาและ subprocess ไม่ใช่ container/VM หรือ OS security isolation สำหรับโค้ดที่ไม่เชื่อถือ Source ยังเป็น Python ที่มีสิทธิ์ของผู้รัน hash เป็นการตรวจการเปลี่ยนแปลงหลังรัน ไม่ใช่การป้องกันการเข้าถึงระบบ
- ยังไม่มี REA MCP adapter และยังไม่ได้ผูกเข้าตัวมอบหมายงาน W3 เอเจนท์ที่เรียก CLI ได้ใช้เครื่องมือนี้ได้แล้ว
- `phase_ready:false` เป็นข้อจำกัดของรายงานนี้ ไม่ใช่การตัดสินแทน BBX19 ว่าห้ามขยับเฟส ต้องประเมินงานจริงด้านอื่นก่อนประกาศว่าฐานทั้งระบบพร้อม

## ตรวจซ้ำ

```sh
python -m unittest discover -s tests -p test_mpcp_agent_sandbox.py -v
python protocol/mpcp/runtime_sanity_sweep.py
python protocol/mpcp/test_condien_blueprint.py
```

CI ใน `.github/workflows/mpcp-agent-sandbox.yml` ตรวจ regression และเก็บหลักฐานจากการสร้าง setup จริงไว้เป็น artifact
