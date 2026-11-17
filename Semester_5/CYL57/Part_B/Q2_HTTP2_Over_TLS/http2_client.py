"""Send six concurrent HTTP/2 requests over one TLS connection for Wireshark."""
import argparse
import asyncio
import ssl

import httpx


async def main(url, cafile):
    tls = ssl.create_default_context(cafile=cafile)
    tls.keylog_filename = "session.keys"  # Wireshark uses this to decrypt TLS

    # One connection, so all six requests become separate HTTP/2 streams on it.
    limits = httpx.Limits(max_connections=1)
    async with httpx.AsyncClient(http2=True, verify=tls, limits=limits) as client:
        requests = [client.get(url, params={"cyl57": i}) for i in range(6)]
        responses = await asyncio.gather(*requests)

    for response in responses:
        print(response.http_version, response.status_code, response.url)


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("url", help="HTTPS URL on an HTTP/2 server")
parser.add_argument("--cafile", help="PEM CA for a local test server")
args = parser.parse_args()
asyncio.run(main(args.url, args.cafile))
