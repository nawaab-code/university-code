"""Optional HTTPS request with TLS key logging; browser.sh satisfies the browser task."""
import argparse
import socket
import ssl
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("host", nargs="?", default="www.example.com")
    parser.add_argument("--port", type=int, default=443)
    parser.add_argument("--cafile", help="Trust this PEM CA/certificate for a local TLS server")
    args = parser.parse_args()
    context = ssl.create_default_context(cafile=args.cafile)
    context.keylog_filename = str(Path("session.keys").resolve())
    context.set_alpn_protocols(["http/1.1"])
    with socket.create_connection((args.host, args.port), timeout=10) as tcp:
        with context.wrap_socket(tcp, server_hostname=args.host) as tls:
            print("Version:", tls.version())
            print("Cipher:", tls.cipher()[0])
            request = f"GET / HTTP/1.1\r\nHost: {args.host}:{args.port}\r\nConnection: close\r\n\r\n"
            tls.sendall(request.encode("ascii"))
            response = bytearray()
            while True:
                block = tls.recv(4096)
                if not block:
                    break
                response.extend(block)
            print("Status:", response.split(b"\r\n", 1)[0].decode("ascii", errors="replace"))
    print("Wireshark TLS key log:", context.keylog_filename)


if __name__ == "__main__":
    main()
