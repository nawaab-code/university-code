# CY52: first five lab experiments (Python)

These programs implement experiments 1–5 from the **Lab Experiments** section on page 2 of `Syllabus - CY52 - Advanced Networks.pdf`. They use only the Python standard library. Run commands from this directory with Python 3.10 or newer. Open two terminals for the client/server experiments. All servers bind to `127.0.0.1` by default, so the examples stay on your computer.

## 1. TCP file server and client

**Task:** The client sends a filename; the server sends the file contents if it exists.

```bash
# Terminal A
python3 tcp_file_server.py

# Terminal B
python3 tcp_file_client.py hello.txt
python3 tcp_file_client.py missing.txt
python3 tcp_file_client.py hello.txt --output received.txt
```

- `SOCK_STREAM` gives a reliable, ordered **byte stream**. It does not preserve message boundaries.
- Protocol: client sends `filename\n`; server sends `OK <byte_count>\n` plus exactly that many file bytes, or `ERR <reason>\n`. The length lets the client distinguish a complete file from an early disconnect.
- `sendall()` handles partial socket writes; the client reads until the announced number of bytes arrives. The server sends chunks so it does not load the whole file into memory.
- The server shares only direct files in `shared/`. Put another file there to try it.

**Viva:** What happens if a requested file is absent? The server sends `ERR file not found`. Why specify a file length? TCP is a stream, so one `recv()` is not guaranteed to return the entire file.

## 2. UDP datagram server and client

**Task:** Display a server-side message on the client.

```bash
# Terminal A
python3 udp_server.py --message "Welcome to CY52"

# Terminal B
python3 udp_client.py
```

- `SOCK_DGRAM` sends a complete datagram with `sendto()`. `recvfrom()` returns the datagram and sender address. There is no connection setup.
- The client sends one request datagram; the server replies to that client's address. The client has a 3-second timeout because UDP does not guarantee delivery or ordering.
- The 4096-byte receive buffer limits this *demo's* message size; a longer datagram may be truncated.

**Viva:** TCP gives an ordered byte stream; UDP preserves datagram boundaries but offers no delivery guarantee. A `recvfrom()` receives at most one datagram.

## 3. CRC-CCITT (16-bit)

**Task:** Generate a CRC and detect a changed bit.

```bash
python3 crc_ccitt.py 123456789
python3 crc_ccitt.py 123456789 --flip-bit 0
```

This code uses **CRC-CCITT-FALSE**: width 16, polynomial `0x1021` (the leading `x^16` term is implicit), initial register `0xFFFF`, no reflection, final XOR `0x0000`. These settings produce `0x29B1` for the standard test string `123456789`. “CRC-CCITT” alone can refer to several variants; use the parameters your instructor specifies if they differ.

For each data byte, XOR it into the high end of the 16-bit register. Shift once for each bit. When the old top bit is 1, XOR the register with `0x1021`. Keep only 16 bits. The sender appends the two CRC bytes; the receiver recalculates the CRC on the received data and compares it with the transmitted value.

**Viva:** A CRC detects many accidental error patterns, including every single-bit error with this polynomial. It is not encryption or authentication. If data and CRC are both maliciously changed, a matching CRC does not prove who sent them.

## 4. Client/server Internet checksum

**Task:** Sender generates a checksum; receiver checks it.

```bash
# Terminal A
python3 checksum_server.py

# Terminal B
python3 checksum_client.py hello
python3 checksum_client.py hello --corrupt
```

The sender groups bytes into 16-bit words in network byte order, pads an odd final byte with zero *for calculation*, adds the words with end-around carry, and complements all 16 result bits. The receiver calculates the checksum on received data and compares it with the transmitted 16-bit value.

The application protocol is `[4-byte data length][2-byte checksum][data]`. `--corrupt` flips one data bit **after** checksum generation to simulate a transmission error. The result should change from `VALID` to `INVALID`. TCP already has its own transport checksum; this extra application checksum is present to demonstrate the lab algorithm.

**Worked example:** `"ABCD"` becomes words `0x4142` and `0x4344`. Their sum is `0x8486`; its one's complement is `0x7B79`. For `"ABC"`, pad the last word to `0x4300` for calculation only.

**Viva:** Why fold carry bits back into the low 16 bits? This is one's-complement addition, not ordinary 16-bit truncation. A checksum detects errors but cannot guarantee that every possible change will be detected.

## 5. IPv4 fragmentation and reassembly

**Task:** Split a packet to fit an MTU, show offsets, and reconstruct its payload.

```bash
python3 ipv4_fragmentation.py 4000 1500
python3 ipv4_fragmentation.py 1000 1500  # no fragmentation
python3 ipv4_fragmentation.py 100 36    # small MTU example
```

Assumptions: the packet size **includes** a 20-byte IPv4 header with no options, the Don't Fragment flag is clear, and this simulation handles one packet. Each fragment gets its **own** 20-byte header. The IPv4 Fragment Offset counts 8-byte units, so every non-final payload must be a multiple of 8 bytes.

```text
original payload = packet size - 20
non-final payload limit = floor((MTU - 20) / 8) * 8
fragment offset = starting payload byte / 8
MF = 1 except on the final fragment
```

For packet size 4000 and MTU 1500, the original payload is 3980 bytes. The non-final limit is 1480 bytes. The fragments have payloads **1480, 1480, 1020**; total lengths **1500, 1500, 1040**; offsets **0, 185, 370**; and MF values **1, 1, 0**. Reassembly sorts by offset, rejects gaps or overlaps, and joins the payload bytes. The program deliberately reverses their arrival order to show that arrival order is irrelevant.

**Viva:** Why is the second offset 185 instead of 1480? `1480 / 8 = 185`. Why is the last fragment shorter? It carries the remaining bytes. In real IPv4, the destination uses fields including source, destination, protocol, and Identification to group fragments; this one-packet simulation omits those fields.

## Quick self-check

Explain each program before reading its code:

1. Identify the socket type and what one `send`/`recv` means for TCP versus UDP.
2. Explain the request and reply bytes for labs 1, 2, and 4.
3. Calculate the CRC of `123456789` and the checksum of `ABCD`.
4. Calculate the three offsets for a 4000-byte IPv4 packet with MTU 1500.
5. Show what each receiver does when a file is missing, a bit changes, or a fragment is missing.

Run the small checks with `python3 -m unittest -v test_lab_experiments.py`.
