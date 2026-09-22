# CY52 Advanced Networks labs

Python implementations of the first five questions in the **Lab Experiments** section of the CY52 syllabus. The programs were reduced to the scope shown in professor-corrected student records: short interactive code, one clear execution path, and only the concepts required by the experiment. They use only the standard library. Run each example with Python 3.10 or newer from its question folder.

| Question | Topic | Explanation |
| --- | --- | --- |
| 1 | TCP file transfer | [Question 1 README](question_01_tcp_file_transfer/README.md) |
| 2 | UDP datagrams | [Question 2 README](question_02_udp_datagrams/README.md) |
| 3 | CRC-CCITT (16-bit) | [Question 3 README](question_03_crc_ccitt/README.md) |
| 4 | Client/server checksum | [Question 4 README](question_04_checksum/README.md) |
| 5 | IPv4 fragmentation and reassembly | [Question 5 README](question_05_ipv4_fragmentation/README.md) |

## Reference matching

The supplied student records number the practical sessions by execution order, while the syllabus list places TCP before UDP and CRC. They were therefore matched by **topic**, not by the number printed on the record.

| Syllabus folder | Matching corrected record topic |
| --- | --- |
| Question 1: TCP file transfer | Lab 3 TCP records |
| Question 2: UDP datagrams | Lab 1 UDP records |
| Question 3: CRC-CCITT | Lab 2 CRC records |
| Question 4: checksum | Checksum client/server record |
| Question 5: fragmentation | IP fragmentation record dated 19-09-2026 |

The Java ICMP material was not used because it belongs to the syllabus experiment after these five questions.

## Checks

From this `CY52` directory:

```bash
python3 -m unittest discover -s tests -v
```

The tests cover the known CRC value, checksum carry behavior, fragment offsets, reassembly, and an invalid MTU. The socket examples can be tried with the commands in their question READMEs.

## Exam self-check

1. Explain why the TCP client reads until the server closes the connection, while the UDP client receives one datagram.
2. State the exact CRC parameters before giving a CRC-CCITT value.
3. Calculate a 16-bit one's-complement checksum, including end-around carry.
4. Calculate IPv4 fragment payload sizes and offsets in 8-byte units.
5. Show how each receiver responds to a missing file, changed bit, or missing fragment.
