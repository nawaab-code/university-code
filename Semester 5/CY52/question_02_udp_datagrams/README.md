# UDP client-server datagram experiment

> This folder follows the syllabus name `question_02_udp_datagrams`. Some lab records may call the same UDP experiment **Lab 1**.

## Aim

Implement UDP datagram sockets in a client-server program and display the server's reply on the client.

## Concept

UDP is **connectionless**. The client does not create a permanent connection with the server.

1. The client sends `Hello Server` to the server's IP address and port.
2. The server receives the message and the client's address.
3. The server sends `Hello from Server` back to that address.
4. The client receives and displays the reply.

```text
Client                               Server
   |                                   |
   | ---- "Hello Server" ------------> |  sendto() / recvfrom()
   | <--- "Hello from Server" -------- |  recvfrom() / sendto()
   |                                   |
Displays reply
```

UDP is fast and simple, but it does not guarantee delivery or ordering.

## Required files

```text
question_02_udp_datagrams/
|-- udp_server.py
|-- udp_client.py
`-- README.md
```

- `udp_server.py`: waits for one message and replies.
- `udp_client.py`: sends one message and displays the reply.
- `README.md`: explanation and run instructions; the programs do not require it.

## Important functions

| Code | Purpose |
| --- | --- |
| `import socket` | Loads Python's networking library. |
| `socket.socket(AF_INET, SOCK_DGRAM)` | Creates an IPv4 UDP socket. |
| `bind((HOST, PORT))` | Assigns the server to an IP address and port. |
| `sendto(data, address)` | Sends one UDP datagram to an address. |
| `recvfrom(1024)` | Waits for a datagram and returns its data and sender address. |
| `encode("utf-8")` | Converts text into bytes for transmission. |
| `decode("utf-8")` | Converts received bytes back into text. |
| `close()` | Releases the socket after communication finishes. |

`127.0.0.1` means both programs run on the same computer. Port `5000` identifies the server program. The client and server must use the same port.

## Run

Open two terminals in this folder. Start the server first.

**Terminal 1:**

```bash
python3 udp_server.py
```

The server displays:

```text
Server waiting...
```

**Terminal 2:**

```bash
python3 udp_client.py
```

Expected server output:

```text
Server waiting...
Client: Hello Server
```

Expected client output:

```text
Server: Hello from Server
```

Both programs stop after this single exchange. On Windows, use `python` or `py -3` if `python3` is unavailable.

## What to remember

- Server: create socket -> `bind()` -> `recvfrom()` -> `sendto()` -> `close()`.
- Client: create socket -> `sendto()` -> `recvfrom()` -> `close()`.
- Use `SOCK_DGRAM` for UDP.
- `recvfrom()` returns both the message and the sender's address.
- Start the server before the client.

## Result

The UDP client sent a datagram to the server, and the server's reply was received and displayed successfully on the client.
