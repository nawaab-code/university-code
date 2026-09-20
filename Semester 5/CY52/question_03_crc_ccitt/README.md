# Question 3: CRC-CCITT (16-bit)

**Task:** Generate and verify a CRC to detect accidental data changes.

File: `crc_ccitt.py`.

## Run

From this folder:

```bash
python3 crc_ccitt.py 123456789
python3 crc_ccitt.py 123456789 --flip-bit 0
```

The first run reports `0x29B1` and `PASS`; the second flips one bit and reports `FAIL`.

## Explanation

This implementation uses **CRC-CCITT-FALSE**: width 16, polynomial `0x1021` (implicit leading `x^16`), initial register `0xFFFF`, no reflection, and final XOR `0x0000`. “CRC-CCITT” can mean several variants, so compare these parameters with any values supplied by your instructor.

For each byte, XOR it into the high end of the register. Shift for each of its eight bits; if the previous top bit was 1, XOR with `0x1021`. Keep only 16 bits. The sender appends two CRC bytes. The receiver recalculates the CRC on the received data and compares the values.

## Exam points

- For these parameters, the standard string `123456789` produces `0x29B1`.
- This CRC detects any single-bit error. CRCs are for accidental error detection, not authentication.
- State the polynomial, initial value, reflection, and final XOR when giving a CRC value.
