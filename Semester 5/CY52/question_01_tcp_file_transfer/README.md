# Question 1: TCP file transfer

**Task:** The client sends a filename; the server sends its contents if the file exists.

Files: `tcp_file_server.py`, `tcp_file_client.py`, and sample `shared/hello.txt`.

## Run

From this folder, use two terminals:

```bash
# Terminal A
python3 tcp_file_server.py

# Terminal B
python3 tcp_file_client.py hello.txt
python3 tcp_file_client.py missing.txt
python3 tcp_file_client.py hello.txt --output received.txt
```

Stop the server with Ctrl+C, or start it with `--once` to serve one client.

## Explanation

The server uses IPv4 `SOCK_STREAM`, binds to `127.0.0.1:5001`, listens, and accepts clients. The client sends `filename\n`. The server replies with `OK <byte_count>\n` followed by exactly that many file bytes, or `ERR <reason>\n`. The file length tells the client when a complete transfer has arrived.

TCP is a reliable, ordered **byte stream**, so one `recv()` may return fewer bytes than expected. `sendall()` handles partial writes, and the client reads in a loop until it has the announced length. The server sends chunks rather than loading the whole file into memory. It shares only direct files in `shared/`.

## Exam points

- `bind()`, `listen()`, and `accept()` are server operations; `connect()` is the client operation.
- TCP does not preserve application message boundaries; the newline and byte count frame this protocol.
- A missing file produces `ERR file not found`, not an empty successful transfer.
