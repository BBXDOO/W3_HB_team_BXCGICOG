# หลักฐานการรัน local setup

รันด้วย source ที่แก้ในสาขา `feat/mpcp-agent-sandbox` บน base commit `5e4882cc379356d521ac2a589e0b9b8cc5028ffc` ไม่ใช่การรัน source ของ base commit ที่ยังไม่แก้

คำสั่งจริง:

```sh
python tools/mpcp_sandbox.py --request tools/agent_sandbox/local_setup.json --output local_workspace/mpcp-baseline-20261024 --execute
```

ผลที่สังเกตได้:

- `SUCCESS`, manifest SHA-256 ตรงกับไฟล์ที่เขียนจริง
- มี partition directories A/B/C ใน workspace ที่แยกไว้
- LRC2 มี 8 records สำหรับ event ขาเข้าและผลขาออก ตรวจ hash chain ผ่าน
- original source และ snapshot hashes หลังรันตรงกับก่อนรัน
- `phase_ready:false`: ยังไม่ใช่หลักฐานการพร้อมของ W3 ทั้งระบบ

ไฟล์ในโฟลเดอร์นี้เป็นสำเนาหลักฐานจากการรันจริง `local_setup_result.json` เก็บ source hashes และ trace เต็ม, `setup.json` คือ manifest ที่ได้จริง, `worker.log` คือ log ของ worker

ผลตรวจเพิ่มเติมที่รันใน workspace นี้:

- `python -m pytest -q tests/test_mpcp_agent_sandbox.py tests/test_w3lgu_core.py tests/test_w3lgu_operational.py tests/test_w3lgu_event_field_logic27.py tests/test_w3lgu_mfc_logic.py`: 62 passed, 2 subtests passed (มี datetime.utcnow deprecation warnings 8 รายการ)
- `python protocol/mpcp/runtime_sanity_sweep.py`: 81/81 passed
- `python protocol/mpcp/test_condien_blueprint.py`: 69/69 passed

ยังไม่ได้ตรวจ Android/Termux/iOS, ไม่ได้เรียก REA provider, ไม่ได้ตรวจการ deploy และยังไม่มีผล CI ระยะไกล ณ เวลาสร้างหลักฐานนี้
