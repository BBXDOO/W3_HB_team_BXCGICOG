import reference_implementation as epi

def to_ep_signal(data_bin: str) -> str:
    """แปลง binary string เป็น EP_SIGNAL format"""
    return epi.encode(data_bin, fmt="BIN")

def from_ep_signal(signal: str) -> str:
    """แปลง EP_SIGNAL format กลับเป็น binary string"""
    return epi.decode(signal)

def interop_with_w3lgu(w3lgu_data: bytes) -> str:
    """ตัวอย่าง adapter สำหรับข้อมูล bytes ของ W3Lgu (แปลงเป็น binary string แล้ว encode)"""
    binstr = ''.join(f'{byte:08b}' for byte in w3lgu_data)
    return to_ep_signal(binstr)

def interop_with_mpcp(mp_data: str) -> str:
    """Adapter สำหรับข้อมูล mpcp ที่ส่ง/รับเป็น binary string โดยตรง"""
    return to_ep_signal(mp_data)
