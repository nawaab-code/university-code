"""Small checks for the three calculation-based labs."""

import unittest

from question_03_crc_ccitt.crc_ccitt import crc_ccitt
from question_04_checksum.checksum import checksum
from question_05_ipv4_fragmentation.ipv4_fragmentation import fragment_packet, reassemble


class LabAlgorithmsTest(unittest.TestCase):
    def test_crc_known_value(self):
        self.assertEqual(crc_ccitt(b"123456789"), 0x29B1)

    def test_checksum(self):
        self.assertEqual(checksum([0x4142, 0x4344]), 0x7B79)
        self.assertEqual(checksum([0xFFFF, 0x0001]), 0xFFFE)

    def test_fragmentation_and_reassembly(self):
        fragments = fragment_packet(4000, 1500)
        self.assertEqual(fragments, [(0, 1480, 1), (185, 1480, 1), (370, 1020, 0)])
        self.assertEqual(reassemble(fragments), 4000)

    def test_invalid_mtu(self):
        with self.assertRaises(ValueError):
            fragment_packet(100, 20)


if __name__ == "__main__":
    unittest.main()
