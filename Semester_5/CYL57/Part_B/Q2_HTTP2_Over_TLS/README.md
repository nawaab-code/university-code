# HTTP/2 over TLS capture and analysis

## 1. Question

Capture and analyse HTTP/2 traffic over TLS using Wireshark. Open a modern website that supports HTTP/2 and inspect the protocol negotiation, multiplexed streams, and TLS encryption.

## 2. Brief explanation

HTTP/2 splits messages into binary frames and can carry several request/response streams over one TCP connection. HTTPS encrypts those frames with TLS. Capture a browser page load, load the browser's TLS session secrets in Wireshark, and verify ALPN chose `h2` before inspecting HTTP/2 frames and stream IDs.

## 3. Extensive explanation

### Protocol layers

```text
HTTP/2 HEADERS and DATA frames, with stream IDs
                 |
TLS authenticated encryption
                 |
TCP ordered byte stream
                 |
IP packets and network link frames
```

ALPN is the TLS extension for choosing the application protocol. The client may offer `h2` and `http/1.1`; the server selects one. In TLS 1.3 the server's choice is in encrypted extensions, so TLS decryption may be needed to inspect it. Offering h2 does not prove it was selected. Chrome's Network panel can also show `h2` in its Protocol column.

### Understanding HTTP/2 frames

| Frame | Meaning |
| --- | --- |
| SETTINGS | Connection parameters; uses stream 0 |
| HEADERS | Request/response headers; HPACK compresses header fields |
| DATA | Message body bytes belonging to one stream |
| WINDOW_UPDATE | Flow-control credit |
| RST_STREAM | Ends one stream with an error |
| GOAWAY | Connection shutdown information |

The client connection preface starts with `PRI * HTTP/2.0`. Client-initiated streams have odd IDs such as 1, 3, and 5. Stream 0 is connection-wide, not a page request. A single TCP segment can carry several HTTP/2 frames, and one frame can span several TCP segments; Wireshark's reassembly connects those layers.

### Proving multiplexing

Find multiple HTTP/2 stream IDs inside the **same** `tcp.stream`. To demonstrate concurrent multiplexing, look for interleaved HEADERS/DATA frames for streams whose lifetimes overlap. Different stream IDs alone prove separate HTTP/2 streams but do not prove simultaneous activity. Different TCP connections do not demonstrate multiplexing on one connection.

`requests.js` starts six concurrent same-origin fetch requests with cache bypass requested. It reads response bodies so their DATA frames are available. The root path query values distinguish requests; the actual server may cache, redirect, serialize, or finish small responses too quickly to show clear overlap. Use an allowed HTTP/2 site with several sizeable resources and repeat if necessary. Do not manufacture a successful multiplexing observation.

### Useful filters and record details

| Purpose | Display filter |
| --- | --- |
| ALPN extension | `tls.handshake.extensions_alpn_str` |
| HTTP/2 frames | `http2` |
| One TCP connection | `http2 and tcp.stream == N` |
| One HTTP/2 stream | `http2.streamid == 1` |
| HEADERS frames | `http2.type == 1` |
| DATA frames | `http2.type == 0` |

Replace N with an actual TCP stream index. Record offered/selected ALPN, TLS version/cipher, TCP endpoints, at least two HTTP/2 stream IDs on one connection, their request paths/status codes, and frame numbers showing interleaving if present. Explain the difference between a TCP stream number and an HTTP/2 stream ID.

### Encryption and limits

Without session secrets you generally see TLS records rather than the HTTP/2 content. TLS encrypts header and body bytes; HPACK compression is not encryption. HTTP/2 still uses TCP, so loss of a TCP segment can delay all streams on that connection. HTTP/3 uses QUIC over UDP and is a different experiment.

## 4. How to operate/run the files

Requires Wireshark and Chrome/Chromium on macOS or Linux. Run commands from this folder.

1. Start Wireshark capture on the active network interface with capture filter `tcp port 443`.
2. Run `bash browser.sh`. This dedicated profile logs keys to this folder's `session.keys` and disables QUIC.
3. Browse to an HTTPS website supporting HTTP/2, for example `https://www.wireshark.org/`. Server support can change; verify the actual Protocol column in browser DevTools -> Network. Right-click Network column headings to enable Protocol.
4. In DevTools, enable **Disable cache** while DevTools is open, then reload the page to generate requests. To generate more requests, paste the contents of `requests.js` into the console on that website's own page and execute it. Review the six-request script before pasting; some browsers require you to enable console pasting explicitly.
5. Stop and save capture as `http2.pcapng`. Configure Wireshark TLS key-log preference to the absolute `session.keys` path printed by the launcher.
6. Check ALPN selection and filter `http2`. Choose a connection and inspect HEADERS/DATA with several stream IDs. Use Follow -> HTTP/2 Stream where available.
7. Record the evidence described above. If traffic is HTTP/1.1, choose another HTTP/2 site; if it is QUIC, confirm the lab browser was used.

`browser.sh` is the runnable browser helper. `requests.js` runs in the browser console, not with Node.js; it relies on browser `fetch` and the current page's `location`.

Close the lab browser before deleting `browser-profile` to reset the experiment. Remove session secrets when no longer needed. Capture files, profile data, and key logs are ignored by Git.

## References

[Wireshark HTTP/2 documentation](https://wiki.wireshark.org/http2) covers dissection and captures. [Wireshark TLS documentation](https://wiki.wireshark.org/TLS/) describes key logging. [HTTP/2 display fields](https://www.wireshark.org/docs/dfref/h/http2.html) lists frame filters.
