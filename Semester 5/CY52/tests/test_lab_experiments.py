"""Algorithm checks for the first five CY52 labs."""

import unittest

from question_03_crc_ccitt.crc_ccitt import crc16_ccitt_false, make_frame, verify_frame
from question_04_checksum.checksum import checksum, valid
from question_05_ipv4_fragmentation.ipv4_fragmentation import fragment_packet, reassemble


class LabAlgorithmsTest(unittest.TestCase):
    def test_crc_known_vector_and_corruption(self) -> None:
        self.assertEqual(crc16_ccitt_false(b"123456789"), 0x29B1)
        frame = make_frame(b"123456789")
        self.assertTrue(verify_frame(frame))
        corrupted = bytearray(frame)
        corrupted[0] ^= 1
        self.assertFalse(verify_frame(corrupted))

    def test_checksum_even_odd_and_corruption(self) -> None:
        self.assertEqual(checksum(b"ABCD"), 0x7B79)
        self.assertEqual(checksum(b"ABC"), 0x7BBD)
        self.assertTrue(valid(b"ABC", checksum(b"ABC")))
        self.assertFalse(valid(b"BBC", checksum(b"ABC")))

    def test_fragmentation_and_reassembly(self) -> None:
        payload, fragments = fragment_packet(4000, 1500)
        self.assertEqual([f.total_length for f in fragments], [1500, 1500, 1040])
        self.assertEqual([f.offset_units for f in fragments], [0, 185, 370])
        self.assertEqual([f.more_fragments for f in fragments], [True, True, False])
        self.assertEqual(reassemble(list(reversed(fragments))), payload)
        with self.assertRaises(ValueError):
            reassemble([fragments[0], fragments[2]])

    def test_no_fragmentation_and_too_small_mtu(self) -> None:
        payload, fragments = fragment_packet(1000, 1500)
        self.assertEqual(len(fragments), 1)
        self.assertEqual(reassemble(fragments), payload)
        with self.assertRaises(ValueError):
            fragment_packet(100, 27)


if __name__ == "__main__":
    unittest.main()
