"""Lab 2: send a server-side message to a UDP client."""

import argparse
import socket


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5002)
    parser.add_argument("--message", default="Hello from the UDP server")
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((args.host, args.port))
        print(f"UDP server listening on {args.host}:{server.getsockname()[1]}", flush=True)
        while True:
            request, address = server.recvfrom(4096)
            print(f"Received {request!r} from {address}", flush=True)
            server.sendto(args.message.encode("utf-8"), address)
            if args.once:
                break


if __name__ == "__main__":
    main()
