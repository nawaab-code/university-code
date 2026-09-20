"""Lab 3: CRC-CCITT-FALSE (width 16, poly 0x1021, init 0xFFFF)."""

import argparse


def crc16_ccitt_false(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc


def make_frame(data: bytes) -> bytes:
    return data + crc16_ccitt_false(data).to_bytes(2, "big")


def verify_frame(frame: bytes) -> bool:
    return len(frame) >= 2 and crc16_ccitt_false(frame[:-2]) == int.from_bytes(frame[-2:], "big")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", help="UTF-8 message to protect")
    parser.add_argument("--flip-bit", type=int, metavar="N", help="flip bit N in the transmitted frame, counting from the left at 0")
    args = parser.parse_args()

    frame = make_frame(args.text.encode("utf-8"))
    print(f"Data: {frame[:-2]!r}")
    print(f"CRC: 0x{int.from_bytes(frame[-2:], 'big'):04X}")
    print(f"Transmitted frame (hex): {frame.hex()}")
    if args.flip_bit is not None:
        if not 0 <= args.flip_bit < len(frame) * 8:
            parser.error(f"--flip-bit must be from 0 to {len(frame) * 8 - 1}")
        changed = bytearray(frame)
        changed[args.flip_bit // 8] ^= 1 << (7 - args.flip_bit % 8)
        frame = bytes(changed)
        print(f"Received frame (hex):    {frame.hex()}")
    print("Verification:", "PASS" if verify_frame(frame) else "FAIL")


if __name__ == "__main__":
    main()
