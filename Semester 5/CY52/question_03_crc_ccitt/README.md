# Question 3: CRC-CCITT 16-bit

## Aim

Generate a 16-bit CRC-CCITT value for entered text and compare it with a received CRC to decide whether the data is valid or corrupted.

The corrected references included both a basic binary CRC exercise and a true CRC-CCITT implementation. This solution uses the true CRC-CCITT form required by the syllabus while keeping the same short, interactive style.

## Folder structure

```text
question_03_crc_ccitt/
├── README.md
└── crc_ccitt.py
```

Only one program is required because generation and verification are calculations performed in a single run. There are no external dependencies or data files.

## Imported libraries

None. The program uses only Python operators and built-in functions such as `input`, `int`, `encode`, and `print`.

## CRC concept

A **Cyclic Redundancy Check** produces a small remainder from the data and a generator polynomial. The sender transmits the data and CRC. The receiver repeats the calculation and compares the received CRC with the calculated value.

This program uses the CRC-CCITT-FALSE parameters:

| Parameter | Value |
| --- | --- |
| Width | 16 bits |
| Polynomial | `0x1021` |
| Initial CRC | `0xFFFF` |
| Input/output reflection | No |
| Final XOR | `0x0000` |

The standard input `123456789` produces `29B1`. “CRC-CCITT” can describe multiple variants, so these parameters matter.

## Run

```bash
python3 crc_ccitt.py
```

Example:

```text
Enter data: 123456789
Generated CRC-CCITT: 29B1
Enter received CRC (hex): 29B1
Data is valid
```

Enter a different received CRC to demonstrate error detection.

## Line-by-line explanation

| Line | Explanation |
| ---: | --- |
| 1 | States the program's purpose. |
| 4 | Defines a reusable CRC function that accepts bytes. |
| 5 | Initializes the 16-bit register to `0xFFFF`. |
| 6 | Processes the input one byte at a time. |
| 7 | Moves the byte into the high 8 bits and XORs it with the register. |
| 8 | Repeats once for each bit in that byte. `_` means the loop number is unused. |
| 9 | Tests the register's top bit with mask `0x8000`. |
| 10 | When the top bit is 1, shifts left and XORs the polynomial `0x1021`. `& 0xFFFF` keeps 16 bits. |
| 11-12 | When the top bit is 0, only shifts left and keeps 16 bits. |
| 13 | Returns the final CRC integer. |
| 16 | Runs the interactive section only when this file is executed directly; tests can import the function safely. |
| 17 | Reads text and converts it to bytes because CRC operates on bits and bytes. |
| 18 | Calculates the sender's CRC. |
| 19 | Prints exactly four uppercase hexadecimal digits. |
| 21 | Reads the received hexadecimal CRC and converts it to an integer. |
| 22-25 | Compares the values and prints whether the data is valid or corrupted. |

## What to remember

Initialize `FFFF`, XOR each byte into the high end, process 8 bits, use polynomial `1021` when the top bit is 1, and keep only 16 bits.
