import unittest
from ep_signal_adapter import to_ep_signal, from_ep_signal, interop_with_w3lgu

class TestEPSignalAdapter(unittest.TestCase):
    def test_basic_encode_decode(self):
        binary = "01010111"
        encoded = to_ep_signal(binary)
        decoded = from_ep_signal(encoded)
        self.assertEqual(binary, decoded)

    def test_w3lgu_interop(self):
        buf = bytes([0b01110011, 0b00111000])
        ep_sig = interop_with_w3lgu(buf)
        binstr = ''.join(f'{byte:08b}' for byte in buf)
        decode_out = from_ep_signal(ep_sig)
        self.assertEqual(binstr, decode_out)

if __name__ == "__main__":
    unittest.main()
