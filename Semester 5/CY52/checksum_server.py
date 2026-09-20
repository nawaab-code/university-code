"""Lab 4: receive data and verify its application-layer checksum."""

import argparse
import socket

from checksum import valid


def receive_exact(connection: socket.socket, count: int) -> bytes:
    result = bytearray()
    while len(result) < count:
        chunk = connection.recv(count - len(result))
        if not chunk:
            raise ConnectionError("client disconnected before sending all bytes")
        result.extend(chunk)
    return bytes(result)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5003)
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((args.host, args.port))
        server.listen()
        print(f"Checksum server listening on {args.host}:{server.getsockname()[1]}", flush=True)
        while True:
            connection, address = server.accept()
            with connection:
                try:
                    connection.settimeout(5)
                    # Wire format: 4-byte length, 2-byte checksum, then data.
                    length = int.from_bytes(receive_exact(connection, 4), "big")
                    received_checksum = int.from_bytes(receive_exact(connection, 2), "big")
                    if length > 1_000_000:
                        raise ValueError("message is too large")
                    data = receive_exact(connection, length)
                    passed = valid(data, received_checksum)
                    print(f"From {address}: data={data!r}, checksum=0x{received_checksum:04X}, valid={passed}", flush=True)
                    connection.sendall(b"VALID\n" if passed else b"INVALID\n")
                except (ConnectionError, OSError, ValueError) as error:
                    print(f"Bad request: {error}", flush=True)
            if args.once:
                break


if __name__ == "__main__":
    main()
