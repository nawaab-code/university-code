"""Generate concurrent HTTP/2 requests for a Wireshark capture."""
import argparse
import asyncio
import os
import ssl

import httpx


async def capture_requests(url, cafile):
    os.umask(0o077)
    tls = ssl.create_default_context(cafile=cafile)
    tls.keylog_filename = "session.keys"
    async with httpx.AsyncClient(
        http2=True, verify=tls, trust_env=False, limits=httpx.Limits(max_connections=1),
    ) as client:
        responses = await asyncio.gather(*(client.get(url, params={"cyl57": i}) for i in range(6)))
    for response in responses:
        print(response.http_version, response.status_code, response.url)
    if any(response.http_version != "HTTP/2" for response in responses):
        raise RuntimeError("The server did not negotiate HTTP/2.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="HTTPS URL on an HTTP/2 server")
    parser.add_argument("--cafile", help="PEM CA for a local test server")
    args = parser.parse_args()
    try:
        if httpx.URL(args.url).scheme != "https":
            parser.error("Use an https:// URL.")
        asyncio.run(capture_requests(args.url, args.cafile))
    except (OSError, httpx.HTTPError, httpx.InvalidURL, RuntimeError) as error:
        parser.exit(1, f"{error}\n")
