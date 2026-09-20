# Question 2: UDP datagram messages

**Task:** Display a server-side message on a UDP client.

Files: `udp_server.py` and `udp_client.py`.

## Run

From this folder, use two terminals:

```bash
# Terminal A
python3 udp_server.py --message "Welcome to CY52"

# Terminal B
python3 udp_client.py
```

Stop the server with Ctrl+C, or start it with `--once` to answer one request.

## Explanation

Both programs use IPv4 `SOCK_DGRAM`. The client sends a request with `sendto()`. The server receives the request and sender address with `recvfrom()`, then sends its message back to that address. There is no connection setup.

UDP preserves datagram boundaries, but does not guarantee delivery or ordering. The client uses a three-second timeout. The 4096-byte receive buffer is a limit of this demo; longer messages can be truncated.

## Exam points

- TCP uses `SOCK_STREAM`; UDP uses `SOCK_DGRAM`.
- `recvfrom()` returns both data and the sender address. The server needs that address to reply.
- UDP itself does not retransmit if the reply is lost.
