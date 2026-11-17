"""Make one HTTPS request and save the TLS secrets for Wireshark."""
import argparse
import ssl
from http.client import HTTPSConnection

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("host", nargs="?", default="www.example.com")
parser.add_argument("--port", type=int, default=443)
parser.add_argument("--cafile", help="PEM CA for a local test server")
args = parser.parse_args()

tls = ssl.create_default_context(cafile=args.cafile)
tls.keylog_filename = "session.keys"  # Wireshark uses this to decrypt TLS

connection = HTTPSConnection(args.host, args.port, timeout=10, context=tls)
connection.connect()  # TLS handshake happens here
print("Version:", connection.sock.version())
print("Cipher:", connection.sock.cipher()[0])
connection.request("GET", "/")
response = connection.getresponse()
print(f"Status: HTTP/{response.version / 10} {response.status} {response.reason}")
connection.close()
