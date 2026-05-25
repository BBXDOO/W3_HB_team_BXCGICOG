import ep_codec as epi   # ชื่อโมดูลจริงที่เรามี (เปลี่ยนจาก reference_implementation)

def to_ep_signal(data_bin: str) -> str:
    """
    แปลง binary string (ประกอบด้วย '0' และ '1' เท่านั้น) เป็น EP_SIGNAL format
    """
    if not data_bin or not all(c in '01' for c in data_bin):
        raise ValueError("data_bin must be a non-empty binary string")
    return epi.encode(data_bin, fmt="BIN")

def from_ep_signal(signal: str) -> str:
    """
    แปลง EP_SIGNAL format กลับเป็น binary string
    ถ้า decode ไม่ผ่านจะ raise EPError
    """
    return epi.decode(signal)

def interop_with_w3lgu(w3lgu_data: bytes) -> str:
    """Adapter สำหรับข้อมูล bytes ของ W3Lgu: แปลงเป็น binary string แล้ว encode เป็น EP_SIGNAL"""
    binstr = ''.join(f'{byte:08b}' for byte in w3lgu_data)
    return to_ep_signal(binstr)

def interop_with_mpcp(mp_data: str) -> str:
    """Adapter สำหรับข้อมูล mpcp ที่เป็น binary string อยู่แล้ว"""
    # mp_data ควรเป็น binary string เช่น "0011010110111000"
    return to_ep_signal(mp_data)
