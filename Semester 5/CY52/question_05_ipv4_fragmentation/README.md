# Question 5: IPv4 fragmentation and reassembly

**Task:** Given a packet size and MTU, generate fragments and offsets, then reconstruct the payload.

File: `ipv4_fragmentation.py`.

## Run

From this folder:

```bash
python3 ipv4_fragmentation.py 4000 1500
python3 ipv4_fragmentation.py 1000 1500  # no fragmentation
python3 ipv4_fragmentation.py 100 36    # small MTU
```

## Explanation

The packet size **includes** a 20-byte IPv4 header with no options. The Don't Fragment flag is clear, and this simulation handles one packet. Each fragment gets its own 20-byte header. Fragment Offset counts **8-byte units**, so non-final payloads must be multiples of 8 bytes.

```text
original payload = packet size - 20
non-final payload limit = floor((MTU - 20) / 8) * 8
fragment offset = starting payload byte / 8
MF = 1 except on the final fragment
```

For packet size 4000 and MTU 1500, the original payload is 3980 bytes:

| Fragment | Payload | Total length | Offset | MF |
| --- | ---: | ---: | ---: | ---: |
| 1 | 1480 | 1500 | 0 | 1 |
| 2 | 1480 | 1500 | 185 | 1 |
| 3 | 1020 | 1040 | 370 | 0 |

Reassembly sorts by offset, rejects gaps or overlaps, and joins the payload bytes. The program reverses the generated fragments before reassembly to show that arrival order may differ.

## Exam points

- The second offset is `1480 / 8 = 185`, not 1480.
- The last fragment may have a payload length that is not a multiple of 8.
- A real receiver groups fragments using fields such as source, destination, protocol, and Identification; this simulation does not model those fields.
