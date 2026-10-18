# SSL/TLS handshake capture and analysis

## 1. Question

Use Wireshark to capture and analyse SSL/TLS handshake. Perform a secure browser transaction and analyze packet-level handshake.

## 2. Brief explanation

Start a capture before opening an HTTPS page. Find the ClientHello and ServerHello, identify the negotiated TLS version and cipher suite, then inspect the encrypted application records. Export session secrets from a dedicated lab browser so Wireshark can also decode the encrypted handshake messages and HTTP contents.

## 3. Extensive explanation

### What happens on the wire?

1. TCP establishes a connection with SYN, SYN-ACK, and ACK.
2. ClientHello offers TLS versions, cipher suites, key shares, and application protocols (ALPN). Server Name Indication (SNI) often identifies the requested host, although encrypted client hello can hide it.
3. ServerHello selects the version, cipher suite, and key share. The endpoints derive traffic secrets from the key exchange; the secret keys are not sent as plaintext.
4. In a typical full TLS 1.3 handshake, the server sends encrypted extensions, its certificate, CertificateVerify, and Finished. The client verifies the server and sends Finished. Resumption can omit certificate authentication; use a fresh browser profile to favor a full handshake.
5. HTTP requests and responses travel inside authenticated encrypted TLS records.

In TLS 1.2, certificate messages are normally visible without session keys; TLS 1.3 encrypts most handshake messages after ServerHello. Do not conclude that a TLS 1.3 server sent no certificate just because it was invisible before decryption. Optional compatibility ChangeCipherSpec records are not the actual TLS 1.3 key agreement.

The legacy version field may say TLS 1.2 even for TLS 1.3. Check the **supported_versions** extension in ServerHello for the negotiated version. SSL is the obsolete predecessor; use TLS in the actual experiment.

### Understanding the files

- `browser.sh` launches Chrome/Chromium with a separate profile, disables QUIC so this experiment uses TCP/TLS, and sets `SSLKEYLOGFILE` to an absolute path. `umask 077` limits new secret-file permissions.
- `tls_client.py` is an optional repeatable HTTP/1.1-over-TLS client. It validates certificates using the default trust store, prints the negotiated version/cipher and status, and explicitly enables Python TLS key logging. It does not replace the syllabus's browser step.
- `ssl.create_default_context()` enables certificate and hostname checks. `wrap_socket` performs the handshake.
- The request ends with a blank CRLF line. `Connection: close` lets the read loop finish when the server closes the connection. The helper is for a small response, not a general web browser.

### Useful Wireshark filters

Capture filters decide what is recorded; display filters decide what is shown afterward. Their syntax is different.

| Purpose | Filter |
| --- | --- |
| Capture TCP HTTPS | Capture filter: `tcp port 443` |
| Show TLS | Display filter: `tls` |
| ClientHello | `tls.handshake.type == 1` |
| ServerHello | `tls.handshake.type == 2` |
| Certificate, after decryption if needed | `tls.handshake.type == 11` |
| One connection | `tcp.stream == N` (replace N with its stream number) |
| Decrypted web traffic | `http or http2` |

### What to record

Record actual frame numbers, client/server IPs and ports, TCP stream number, offered versus selected TLS version and cipher suite, key exchange group, certificate subject/issuer, and the order of handshake messages. Note what appeared only after key logging was configured. Select packets and expand TLS details; save screenshots and your capture locally.

Expected conclusion: TLS establishes authenticated encryption before carrying the browser's HTTP transaction. A packet's ciphertext length and timing remain visible even when its content is encrypted. A key log enables local inspection because it reveals session secrets, not because TLS has been broken.

## 4. How to operate/run the files

Requires Wireshark with capture permission and Chrome/Chromium on macOS or Linux. Open a terminal in this folder.

1. Open Wireshark and select the interface carrying internet traffic (often Wi-Fi or Ethernet). Use capture filter `tcp port 443` and start capturing.
2. Run `bash browser.sh`. In the new lab window open `https://www.example.com/` or another HTTPS page. A successful page load is the secure browser transaction; no login or payment is needed.
3. Close the lab window after the page loads. Stop capture and save as `tls.pcapng`.
4. Open Wireshark preferences/settings -> Protocols -> TLS -> **(Pre)-Master-Secret log filename**. Select the absolute `session.keys` path printed by the script. Apply and redisplay the capture.
5. Use the filters above and fill in your actual observations. Follow the relevant TCP/TLS stream to examine request and response data.

Optional repeatable client (Python 3.8+, standard library only):

```bash
python3 tls_client.py www.example.com
```

For a controlled local TLS server with your own trusted certificate:

```bash
python3 tls_client.py localhost --port 8443 --cafile server.crt
```

Capture loopback and `tcp port 8443` in that case. The certificate must include `localhost` in its Subject Alternative Name. No certificate checks are disabled.

### Troubleshooting and cleanup

- No packets: choose the correct interface, start capture before navigation, and ensure a fresh browser connection.
- Only UDP/QUIC: use the dedicated launched browser and its `--disable-quic` flag.
- No decrypted messages: confirm `session.keys` is nonempty and matches the captured connection. A different browser process/profile may not inherit the environment.
- To repeat a full handshake, close the lab browser and delete its `browser-profile` directory before launching again. Profile and secret files are generated and ignored by Git.
- When finished, close the lab browser and remove `session.keys` and `browser-profile` if you no longer need them. Keep captures with secrets private.

## References

[Wireshark TLS documentation](https://wiki.wireshark.org/TLS/) explains TLS dissection and key-log configuration. [TLS display fields](https://www.wireshark.org/docs/dfref/t/tls.html) lists filters.
