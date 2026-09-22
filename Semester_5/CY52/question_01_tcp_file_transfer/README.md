# Question 1: TCP file transfer

## Aim

The client sends a filename through a TCP connection. The server reads that text file from `shared/` and returns its contents. If it does not exist, the server returns `File not found`.

This version follows the scope of the corrected TCP references: one server, one client, one request, and a direct response. It keeps a receive loop in the client because TCP may deliver a file in several pieces.

## Folder structure

```text
question_01_tcp_file_transfer/
├── README.md
├── tcp_file_client.py
├── tcp_file_server.py
└── shared/
    └── hello.txt
```

The client and server are separate because they run as separate processes. `shared/` represents the server's available files and keeps test data separate from program code. Run both programs from this question folder so `shared/hello.txt` resolves correctly.

## Imported library

| Import | Purpose |
| --- | --- |
| `socket` | Creates TCP sockets and provides `bind`, `listen`, `accept`, `connect`, `sendall`, and `recv`. It is part of Python's standard library. |

## Protocol and file-transfer concept

The program uses **TCP**, selected by `AF_INET` and `SOCK_STREAM`.

- `AF_INET` means IPv4 addresses are used.
- `SOCK_STREAM` means TCP: a reliable, ordered byte stream.
- The server listens on `localhost` port `5001`.
- The client sends the filename as encoded bytes.
- The server decodes the filename, reads the text file, encodes the contents, and sends them.
- Closing the server-side connection tells the client that the byte stream has ended.

```text
Client -- filename --> Server -- reads shared/file --> Server -- contents --> Client
```

TCP does not preserve message boundaries. A single `recv(1024)` may return only part of a large file, so the client repeats `recv()` until it gets empty bytes, which means the server closed the connection.

## Run

Use two terminals in this folder:

```bash
# Terminal 1
python3 tcp_file_server.py

# Terminal 2
python3 tcp_file_client.py
```

Enter `hello.txt`. Restart the server before testing another filename because this lab server handles one client and exits.

## Server line-by-line explanation

| Line | Explanation |
| ---: | --- |
| 1 | Describes the purpose of the file. |
| 3 | Imports Python's `socket` networking library. |
| 6 | Creates an IPv4 TCP socket. |
| 7 | Assigns the socket to local port `5001`. |
| 8 | Places it in listening mode; `1` is the pending-connection queue size. |
| 9 | Shows that the server is ready. |
| 11 | Waits for a client. It returns a new connected socket and the client's address. |
| 12 | Receives up to 1024 filename bytes and converts them to text. |
| 13 | Displays the requested name on the server. |
| 15 | Starts error handling for a missing file. |
| 16 | Opens the named file inside `shared/` in text-read mode. `with` closes it automatically. |
| 17 | Reads the complete text file into `data`. |
| 18-19 | If the file is absent, stores an error message instead. |
| 21 | Converts the response to bytes and sends all of it. |
| 22 | Closes the connection to the client. |
| 23 | Closes the listening socket and ends the one-client server. |

## Client line-by-line explanation

| Line | Explanation |
| ---: | --- |
| 1 | Describes the client's purpose. |
| 3 | Imports `socket`. |
| 6 | Creates an IPv4 TCP socket. |
| 7 | Connects to the server at local port `5001`. |
| 9 | Reads the required filename from the user. |
| 10 | Encodes the filename and sends it completely. |
| 12 | Prints a label before the response. |
| 13 | Starts a loop because TCP may split the file into several chunks. |
| 14 | Receives up to 1024 bytes. |
| 15-16 | Stops when `recv()` returns empty bytes after the server closes its connection. |
| 17 | Decodes and prints each chunk without adding extra newlines. |
| 19 | Prints one final newline. |
| 20 | Closes the client socket. |

## What to remember

`socket -> connect -> send filename -> recv in a loop -> close` on the client, and `socket -> bind -> listen -> accept -> recv -> read file -> send -> close` on the server.
