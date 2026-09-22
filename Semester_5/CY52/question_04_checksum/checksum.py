"""Common 16-bit one's-complement checksum function."""


def checksum(segments):
    total = sum(segments)
    while total > 0xFFFF:
        total = (total & 0xFFFF) + (total >> 16)
    return (~total) & 0xFFFF
