import unittest
from ep_signal_adapter import to_ep_signal, from_ep_signal, interop_with_w3lgu, interop_with_mpcp
from ep_codec import EPError

class TestEPSignalAdapter(unittest.TestCase):
    
    # ---- Test cases ตาม TEST_CASES.md ----
    def test_group_a_basic(self):
        cases = [
            ("0", "0/1-0'BIN"),
            ("1", "1/1-1'BIN"),
            ("00", "0/2-0'BIN"),
            ("11", "1/2-2'BIN"),
            ("01", "0/11-1'BIN"),
            ("10", "1/11-1'BIN"),
        ]
        for binary, expected_ep in cases:
            with self.subTest(binary=binary):
                encoded = to_ep_signal(binary)
                self.assertEqual(encoded, expected_ep)
                decoded = from_ep_signal(encoded)
                self.assertEqual(decoded, binary)

    def test_group_b_alternating(self):
        cases = [
            ("1010", "1/1111-2'BIN"),
            ("0101", "0/1111-2'BIN"),
            ("10101010", "1/11111111-4'BIN"),
        ]
        for binary, expected_ep in cases:
            with self.subTest(binary=binary):
                self.assertEqual(to_ep_signal(binary), expected_ep)

    def test_group_c_repeated_blocks(self):
        cases = [
            ("000111", "0/33-3'BIN"),
            ("111000", "1/33-3'BIN"),
            ("00110011", "0/2222-4'BIN"),
        ]
        for binary, expected_ep in cases:
            with self.subTest(binary=binary):
                self.assertEqual(to_ep_signal(binary), expected_ep)

    def test_group_d_example(self):
        binary = "0011010110111000"
        expected = "0/221112133-8'BIN"
        self.assertEqual(to_ep_signal(binary), expected)

    # ---- Round-trip ทดสอบการ encode/decode แบบสุ่ม ----
    def test_roundtrip_random_binary(self):
        import random
        for _ in range(20):
            length = random.randint(1, 100)
            binary = ''.join(random.choice('01') for _ in range(length))
            encoded = to_ep_signal(binary)
            decoded = from_ep_signal(encoded)
            self.assertEqual(binary, decoded)

    # ---- Failure tests ----
    def test_failure_wrong_verify(self):
        with self.assertRaises(EPError):
            from_ep_signal("0/22-1'BIN")   # verify mismatch

    def test_failure_invalid_header(self):
        with self.assertRaises(EPError):
            from_ep_signal("2/22-2'BIN")

    def test_failure_missing_payload(self):
        with self.assertRaises(EPError):
            from_ep_signal("0//2'BIN")

    def test_failure_unknown_format(self):
        with self.assertRaises(EPError):
            from_ep_signal("0/22-2'XYZ")

    # ---- Adapter interop tests (ของคุณ) ----
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

    def test_mpcp_interop(self):
        mp_bin = "110011001100"
        ep_sig = interop_with_mpcp(mp_bin)
        self.assertEqual(from_ep_signal(ep_sig), mp_bin)

if __name__ == "__main__":
    unittest.main()
