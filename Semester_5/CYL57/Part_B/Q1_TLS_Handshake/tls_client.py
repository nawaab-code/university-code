"""Make an HTTPS request and save the TLS secrets for Wireshark."""
import argparse
from contextlib import closing
from http.client import HTTPSConnection
import os
from pathlib import Path
import ssl


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("host", nargs="?", default="www.example.com")
    parser.add_argument("--port", type=int, default=443)
    parser.add_argument("--cafile", help="Trust this PEM CA/certificate for a local TLS server")
    args = parser.parse_args()

    os.umask(0o077)
    context = ssl.create_default_context(cafile=args.cafile)
    context.keylog_filename = str(Path("session.keys").resolve())
    context.set_alpn_protocols(["http/1.1"])
    with closing(HTTPSConnection(args.host, args.port, timeout=10, context=context)) as connection:
        connection.connect()
        print("Version:", connection.sock.version())
        print("Cipher:", connection.sock.cipher()[0])
        connection.request("GET", "/", headers={"Connection": "close"})
        response = connection.getresponse()
        version = "HTTP/1.0" if response.version == 10 else "HTTP/1.1"
        print(f"Status: {version} {response.status} {response.reason}")
        response.read()
    print("Wireshark TLS key log:", context.keylog_filename)
