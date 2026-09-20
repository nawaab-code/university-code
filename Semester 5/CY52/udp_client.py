"""Lab 2: request and display one UDP message from the server."""

import argparse
import socket


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5002)
    parser.add_argument("--request", default="Send me your message")
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client.settimeout(3)
        client.sendto(args.request.encode("utf-8"), (args.host, args.port))
        try:
            message, address = client.recvfrom(4096)
        except socket.timeout:
            raise SystemExit("No UDP response within 3 seconds") from None
        print(f"Message from {address}: {message.decode('utf-8', errors='replace')}")


if __name__ == "__main__":
    main()
