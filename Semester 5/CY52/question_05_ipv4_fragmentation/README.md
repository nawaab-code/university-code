# Question 5: IPv4 fragmentation and reassembly

## Aim

Accept an original IPv4 packet size and MTU, calculate each fragment's data size, offset, and More Fragments flag, then demonstrate reassembly by adding the fragment data sizes.

This solution follows the corrected fragmentation reference and keeps its tuple-based calculation and console table. It adds one small input check to prevent an invalid MTU from creating an endless loop.

## Folder structure

```text
question_05_ipv4_fragmentation/
├── README.md
└── ipv4_fragmentation.py
```

Only one script is needed because this is a calculation-based simulation. The two functions keep fragmentation and reassembly easy to test, while the interactive section handles input and output.

## Imported libraries

None. The program uses Python built-ins: `input`, `int`, `min`, `sum`, `enumerate`, lists, tuples, and formatted printing.

## Fragmentation concept

Assumptions:

- The input packet size includes a 20-byte IPv4 header with no options.
- Every fragment receives its own 20-byte header.
- The input MTU includes that fragment header.
- The Fragment Offset field counts blocks of 8 data bytes.
- Every non-final fragment therefore carries a multiple of 8 data bytes.
- `MF = 1` means more fragments follow; the final fragment has `MF = 0`.

```text
Original data       = packet size - 20
Maximum fragment data = floor((MTU - 20) / 8) * 8
Offset               = starting data byte / 8
```

For packet size `4000` and MTU `1500`:

| Fragment | Data size | Offset | MF |
| ---: | ---: | ---: | ---: |
| 1 | 1480 | 0 | 1 |
| 2 | 1480 | 185 | 1 |
| 3 | 1020 | 370 | 0 |

The reassembled size is `1480 + 1480 + 1020 + 20 = 4000` bytes. Only one header is counted after reassembly.

## Run

```bash
python3 ipv4_fragmentation.py
```

Enter `4000` for packet size and `1500` for MTU to reproduce the table above.

## Line-by-line explanation

| Line | Explanation |
| ---: | --- |
| 1 | Describes the simulation. |
| 4 | Defines the fragmentation function with packet size and MTU inputs. |
| 5 | Uses the standard 20-byte IPv4 header without options. |
| 6 | Removes the original header to find the data size. |
| 7 | Finds the largest data amount that fits the MTU and is divisible by 8. `//` is integer division. |
| 9-10 | Reject an impossible packet size or MTU. |
| 12 | Creates the list that will hold fragment tuples. |
| 13 | Starts the first fragment at offset 0. |
| 14 | Tracks data still waiting to be placed in fragments. |
| 16 | Repeats until all data is assigned. |
| 17 | Uses the maximum amount or the smaller final remainder. |
| 18 | Sets MF to 1 when data remains after this fragment, otherwise 0. |
| 19 | Stores `(offset, data size, MF)` for the fragment. |
| 20 | Advances the offset in 8-byte units. |
| 21 | Removes the assigned data from the remaining count. |
| 23 | Returns all fragment tuples. |
| 26 | Defines the reassembly calculation. |
| 27 | Adds all fragment data sizes and one final IPv4 header. |
| 30 | Runs the input/output section only when the script is executed directly. |
| 31-32 | Read the original packet size and MTU as integers. |
| 33 | Generate the fragments. |
| 35 | Print the table heading. |
| 36 | Number the fragments from 1 and unpack each tuple. |
| 37 | Print one table row. |
| 39 | Calculate the reassembled packet size. |
| 40 | Display that size. |
| 41 | Compare it with the original and show success or failure. |

## What to remember

Subtract one 20-byte header, round fragment data down to a multiple of 8, express offsets in 8-byte units, set MF to 0 only on the final fragment, then add the data plus one header during reassembly.
