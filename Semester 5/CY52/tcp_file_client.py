"""Lab 1: request a file by name and receive its exact bytes over TCP."""

import argparse
import socket
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("filename", help="name of a file in the server's shared directory")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5001)
    parser.add_argument("--output", type=Path, help="save bytes to this file instead of stdout")
    args = parser.parse_args()
    if "\n" in args.filename or "\r" in args.filename:
        parser.error("filename cannot contain a newline")

    with socket.create_connection((args.host, args.port), timeout=5) as connection:
        connection.sendall((args.filename + "\n").encode("utf-8"))
        reader = connection.makefile("rb")
        header = reader.readline(4097)
        if not header or len(header) > 4096 or not header.endswith(b"\n"):
            raise RuntimeError("invalid server response")
        if header.startswith(b"ERR "):
            raise SystemExit(header.decode("utf-8", errors="replace").strip())
        if not header.startswith(b"OK "):
            raise RuntimeError("unknown server response")
        size = int(header[3:].strip())
        if size < 0:
            raise RuntimeError("negative file size")

        destination = args.output.open("wb") if args.output else sys.stdout.buffer
        try:
            remaining = size
            while remaining:
                chunk = reader.read(min(64 * 1024, remaining))
                if not chunk:
                    raise RuntimeError("connection closed before file was complete")
                destination.write(chunk)
                remaining -= len(chunk)
        finally:
            if args.output:
                destination.close()
    if args.output:
        print(f"Received {size} bytes into {args.output}")


if __name__ == "__main__":
    main()
