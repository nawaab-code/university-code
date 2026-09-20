"""Lab 1: serve a named file over a TCP byte stream."""

import argparse
import socket
from pathlib import Path


CHUNK_SIZE = 64 * 1024


def serve_file(connection: socket.socket, shared_dir: Path) -> None:
    with connection:
        request = connection.makefile("rb").readline(4097)
        if not request or len(request) > 4096 or not request.endswith(b"\n"):
            connection.sendall(b"ERR invalid request\n")
            return

        try:
            filename = request[:-1].decode("utf-8")
        except UnicodeDecodeError:
            connection.sendall(b"ERR filename must be UTF-8\n")
            return

        # Restrict the exercise server to files directly inside shared_dir.
        if not filename or Path(filename).name != filename or filename in {".", ".."}:
            connection.sendall(b"ERR invalid filename\n")
            return
        path = shared_dir / filename
        if not path.is_file() or path.resolve().parent != shared_dir.resolve():
            connection.sendall(b"ERR file not found\n")
            return

        with path.open("rb") as source:
            connection.sendall(f"OK {path.stat().st_size}\n".encode("ascii"))
            while chunk := source.read(CHUNK_SIZE):
                connection.sendall(chunk)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5001)
    parser.add_argument("--shared-dir", type=Path, default=Path(__file__).with_name("shared"))
    parser.add_argument("--once", action="store_true", help="stop after one client")
    args = parser.parse_args()
    args.shared_dir.mkdir(parents=True, exist_ok=True)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((args.host, args.port))
        server.listen()
        print(f"TCP file server listening on {args.host}:{server.getsockname()[1]}", flush=True)
        while True:
            connection, address = server.accept()
            print(f"Client connected: {address}", flush=True)
            try:
                serve_file(connection, args.shared_dir)
            except (BrokenPipeError, ConnectionResetError) as error:
                print(f"Client disconnected: {error}", flush=True)
            if args.once:
                break


if __name__ == "__main__":
    main()
