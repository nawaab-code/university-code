"""Lab 4: 16-bit one's-complement Internet checksum over application data."""


def checksum(data: bytes) -> int:
    if len(data) % 2:
        data += b"\x00"  # padding participates in calculation, not transmission
    total = sum((data[i] << 8) | data[i + 1] for i in range(0, len(data), 2))
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)
    return (~total) & 0xFFFF


def valid(data: bytes, received_checksum: int) -> bool:
    return checksum(data) == received_checksum
