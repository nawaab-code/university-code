# Question 4: Client/server checksum

**Task:** The sender generates a checksum; the receiver verifies it to detect transmission errors.

Files: `checksum.py` (algorithm), `checksum_client.py` (sender), and `checksum_server.py` (receiver).

## Run

From this folder, use two terminals:

```bash
# Terminal A
python3 checksum_server.py

# Terminal B
python3 checksum_client.py hello
python3 checksum_client.py hello --corrupt
```

Stop the server with Ctrl+C, or start it with `--once` to handle one client.

## Explanation

The sender groups bytes into 16-bit words in network byte order. It pads an odd last byte with zero **for calculation only**, adds the words with end-around carry, then complements all 16 bits. The receiver calculates the checksum on received data and compares it with the transmitted value.

The application protocol is `[4-byte data length][2-byte checksum][data]` over TCP. `--corrupt` flips one data bit after checksum generation to show an `INVALID` response. TCP already has its own transport checksum; this extra application checksum demonstrates the lab algorithm.

**Worked example:** `"ABCD"` becomes `0x4142` and `0x4344`; the sum is `0x8486`, so the checksum is `0x7B79`. For `"ABC"`, calculate using `0x4142` and padded `0x4300`.

## Exam points

- Fold carry bits back into the low 16 bits instead of discarding them.
- The calculation padding is not sent as data.
- A checksum detects many errors, but different messages can occasionally have the same checksum.
