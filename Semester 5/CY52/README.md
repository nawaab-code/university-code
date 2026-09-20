# CY52 Advanced Networks labs

Python implementations of the first five questions in the **Lab Experiments** section of the CY52 syllabus. They use only the standard library. Run each example with Python 3.10 or newer from its question folder. Socket examples need two terminals and bind to `127.0.0.1` by default.

| Question | Topic | Explanation |
| --- | --- | --- |
| 1 | TCP file transfer | [Question 1 README](question_01_tcp_file_transfer/README.md) |
| 2 | UDP datagrams | [Question 2 README](question_02_udp_datagrams/README.md) |
| 3 | CRC-CCITT (16-bit) | [Question 3 README](question_03_crc_ccitt/README.md) |
| 4 | Client/server checksum | [Question 4 README](question_04_checksum/README.md) |
| 5 | IPv4 fragmentation and reassembly | [Question 5 README](question_05_ipv4_fragmentation/README.md) |

## Checks

From this `CY52` directory:

```bash
python3 -m unittest discover -s tests -v
```

The tests cover the known CRC value, even and odd-length checksums, error detection, fragment offsets, reassembly, and invalid inputs. The socket examples can be tried with the commands in their question READMEs.

## Exam self-check

1. Explain why the TCP file protocol sends a length but the UDP example receives one datagram at a time.
2. State the exact CRC parameters before giving a CRC-CCITT value.
3. Calculate a 16-bit one's-complement checksum, including end-around carry.
4. Calculate IPv4 fragment payload sizes and offsets in 8-byte units.
5. Show how each receiver responds to a missing file, changed bit, or missing fragment.
