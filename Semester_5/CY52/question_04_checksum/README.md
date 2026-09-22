# Question 4: Client-server checksum

## Aim

The client accepts ten 16-bit hexadecimal segments, calculates their checksum, and sends the segments plus checksum to the server. The server recalculates the checksum and reports whether it matches.

This follows the corrected checksum reference closely: ten user-defined hexadecimal segments, one's-complement checksum, TCP client/server communication, and a direct comparison.

## Folder structure

```text
question_04_checksum/
├── README.md
├── checksum.py
├── checksum_client.py
└── checksum_server.py
```

The client and server are separate processes. `checksum.py` holds the shared formula so both sides use exactly the same calculation without duplicating it. Run the programs from this folder so `from checksum import checksum` finds the helper file.

## Imported libraries

| File | Import | Purpose |
| --- | --- | --- |
| Client and server | `socket` | Creates the TCP connection and sends or receives bytes. |
| Client and server | `from checksum import checksum` | Imports the common calculation from the local `checksum.py` file. |
| Helper | None | Uses only Python's built-in arithmetic and sequence functions. |

## Networking and checksum concepts

The networking part uses **TCP**. The server performs `bind -> listen -> accept`; the client performs `connect`. Both use local port `5002`. The other socket labs use ports `5000` and `5001`, so each experiment has a distinct port.

The checksum uses 16-bit one's-complement addition:

1. Add all 16-bit segments.
2. If a carry passes bit 16, add that carry back into the low 16 bits.
3. Invert all 16 result bits.
4. Send the segments and checksum.
5. The receiver repeats the calculation and compares the two checksum values.

```text
Client: segments -> checksum -> send both
Server: receive -> recalculate -> compare -> send result
```

The message is plain text: hexadecimal values separated by spaces, with the checksum last. This is easy to inspect and sufficient for the lab.

## Run

Use two terminals in this folder:

```bash
# Terminal 1
python3 checksum_server.py

# Terminal 2
python3 checksum_client.py
```

Enter hexadecimal values such as `1234`, `ABCD`, or `0`. Do not type the `0x` prefix unless you want to; base 16 accepts either form. Both programs stop after one check.

## Checksum helper line-by-line

| Line | Explanation |
| ---: | --- |
| 1 | Describes the shared function. |
| 4 | Defines `checksum`, which receives a list of integer segments. |
| 5 | Adds all segments. |
| 6 | Repeats while the sum needs more than 16 bits. |
| 7 | Keeps the low 16 bits and adds the high carry back in. |
| 8 | Inverts the bits and masks the answer to 16 bits. |

For `4142` and `4344`: sum `8486`, complement `7B79`.

## Client line-by-line explanation

| Line | Explanation |
| ---: | --- |
| 1 | States the client's purpose. |
| 3 | Imports the TCP socket library. |
| 5 | Imports the local checksum function. |
| 8 | Prompts ten times, interprets each answer as hexadecimal, and stores the integers in a list. |
| 9 | Calculates the checksum. |
| 10 | Displays it in hexadecimal. |
| 12 | Converts every segment and the checksum to space-separated hexadecimal text. |
| 14 | Creates a TCP socket; omitted arguments default to IPv4 and TCP. |
| 15 | Connects to the checksum server on local port `5002`. |
| 16 | Encodes and sends the complete message. |
| 17 | Receives, decodes, and displays the server's verification result. |
| 18 | Closes the client socket. |

## Server line-by-line explanation

| Line | Explanation |
| ---: | --- |
| 1 | States the server's purpose. |
| 3 | Imports `socket`. |
| 5 | Imports the same local checksum function used by the client. |
| 8 | Creates a TCP socket. |
| 9 | Assigns it to `localhost:5002`. |
| 10 | Starts listening for one queued connection. |
| 11 | Shows that the server is ready. |
| 13 | Waits for and accepts the client. |
| 14 | Receives text, decodes it, and splits it at spaces. |
| 15 | Converts every value except the last from hex text into data integers. |
| 16 | Converts the last value into the received checksum. |
| 17 | Recalculates the checksum from the received segments. |
| 19-20 | Displays both checksum values. |
| 21 | Chooses `CORRECT` when they match and `WRONG` otherwise. |
| 22 | Displays the result on the server. |
| 24 | Sends the same result to the client. |
| 25-26 | Close the connected socket and listening socket. |

## What to remember

`sum -> end-around carry -> complement` for the calculation. The sender transmits data plus checksum; the receiver recalculates and compares.
