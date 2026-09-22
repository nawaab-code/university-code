# Question 2: UDP datagram messages

## Aim

The client sends one message to a UDP server. The server displays it and sends a server-side message back for the client to display.

This matches the corrected UDP references: one request datagram and one reply datagram with no permanent connection.

## Folder structure

```text
question_02_udp_datagrams/
├── README.md
├── udp_client.py
└── udp_server.py
```

The two programs are separate because the server and client run in different terminals. No shared data folder or helper module is needed for this small exchange.

## Imported library

| Import | Purpose |
| --- | --- |
| `socket` | Creates UDP sockets and supplies `bind`, `sendto`, `recvfrom`, encoding transport, and socket cleanup. |

## Protocol concept

The programs use **UDP** with `AF_INET` and `SOCK_DGRAM`.

- UDP is connectionless, so there is no `listen()`, `accept()`, or `connect()` here.
- Each `sendto()` sends one datagram to an address.
- Each `recvfrom()` receives one datagram and returns its sender's address.
- UDP is fast and simple, but delivery, order, and duplicate protection are not guaranteed.

```text
Client -- "Hello Server" --> Server
Client <-- "Hello from Server" -- Server
```

Both programs use `127.0.0.1`, the IPv4 loopback address, so communication stays on the same computer. They use port `5000` and a 1024-byte buffer.

## Run

Use two terminals in this folder:

```bash
# Terminal 1
python3 udp_server.py

# Terminal 2
python3 udp_client.py
```

Both programs stop after one exchange.

## Server line-by-line explanation

| Line | Explanation |
| ---: | --- |
| 1 | Describes the server's job. |
| 3 | Imports the standard `socket` library. |
| 6 | Stores the loopback IPv4 address. |
| 7 | Stores the UDP port number. |
| 8 | Sets the maximum received size to 1024 bytes. |
| 11 | Creates an IPv4 UDP socket. |
| 12 | Attaches the socket to the server address and port. |
| 14 | Prints the waiting message. |
| 15 | Waits for one datagram and saves both its bytes and the client's address. |
| 16 | Decodes and displays the client's bytes as text. |
| 18 | Stores the server's reply. |
| 19 | Encodes and sends the reply to the address returned by `recvfrom()`. |
| 20 | Closes the UDP socket. |

## Client line-by-line explanation

| Line | Explanation |
| ---: | --- |
| 1 | Describes the client. |
| 3 | Imports `socket`. |
| 6-8 | Store the server address, port, and receive-buffer size. |
| 11 | Creates an IPv4 UDP socket. It does not need `bind()` because the OS chooses a temporary client port. |
| 13 | Stores the client message. |
| 14 | Encodes the message and sends one datagram to the server. |
| 16 | Waits for a reply datagram and records the server address. |
| 17 | Decodes and displays the reply. |
| 19 | Closes the client socket. |

## What to remember

UDP uses `sendto(data, address)` and `recvfrom(size)`. The address returned by the server's `recvfrom()` is the address used for its reply.
