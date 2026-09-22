"""Generate and verify a 16-bit CRC-CCITT value."""


def crc_ccitt(data):
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc


if __name__ == "__main__":
    data = input("Enter data: ").encode()
    generated_crc = crc_ccitt(data)
    print(f"Generated CRC-CCITT: {generated_crc:04X}")

    received_crc = int(input("Enter received CRC (hex): "), 16)
    if generated_crc == received_crc:
        print("Data is valid")
    else:
        print("Data is corrupted")
