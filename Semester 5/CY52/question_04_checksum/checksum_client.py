"""Lab 4: calculate and send a checksum; optionally corrupt the data in transit."""

import argparse
import socket

from checksum import checksum


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("message", help="UTF-8 message to send")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5003)
    parser.add_argument("--corrupt", action="store_true", help="flip one data bit after calculating the checksum")
    args = parser.parse_args()

    data = args.message.encode("utf-8")
    if args.corrupt and not data:
        parser.error("cannot corrupt an empty message")
    value = checksum(data)
    transmitted = bytearray(data)
    if args.corrupt:
        transmitted[0] ^= 1
    packet = len(transmitted).to_bytes(4, "big") + value.to_bytes(2, "big") + transmitted
    print(f"Sender checksum: 0x{value:04X}")
    with socket.create_connection((args.host, args.port), timeout=5) as connection:
        connection.sendall(packet)
        response = connection.makefile("rb").readline(32)
    print("Receiver:", response.decode("ascii").strip())


if __name__ == "__main__":
    main()
