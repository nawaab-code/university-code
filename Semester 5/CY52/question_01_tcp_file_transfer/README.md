# Question 1: TCP file transfer

## Lab question

Develop a client-server program using TCP/IP sockets. The client sends a filename, and the server sends the file's contents if the file is available.

This implementation uses Python. The same networking concepts apply to C, C++, and Java implementations.

## 1. What the program does

The experiment has two programs:

- The **server** owns a folder containing files and waits for requests.
- The **client** connects to the server and requests one file by name.
- If the file exists, the server sends its size and contents.
- If the file does not exist, the server sends an error message.

The programs can run on the same computer or on two computers connected through a network. "Client" and "server" describe the programs' roles, not special types of computers.

## 2. Concepts required to understand the experiment

### Client and server

A **server** waits for and responds to requests. A **client** starts communication by sending a request. Here, the request is a filename such as `hello.txt`; the response is either the file or an error.

### IP address

An IP address identifies the computer with which the client wants to communicate.

- `127.0.0.1` is the loopback address and always means **this same computer**.
- An address such as `192.168.1.20` may identify another computer on a local network.
- `0.0.0.0` tells a server to listen on all available network interfaces. A client should not use it as the destination.

### Port number

One computer can run many network programs. A port identifies the particular program that should receive network traffic. This experiment uses TCP port `5001` by default, and both programs must use the same port.

An IP address identifies the computer; a port identifies a program on that computer. Together, they form an endpoint such as `127.0.0.1:5001`.

### Socket

A socket is the programming interface used for network communication:

- The server creates a listening socket.
- The client creates a socket and connects to the server.
- When a client connects, the server receives a separate connection socket for that client.

### TCP

TCP stands for **Transmission Control Protocol**. It is connection-oriented and supplies an ordered, reliable stream of bytes.

- A connection is established before application data is exchanged.
- Bytes arrive in the order in which they were sent.
- TCP retransmits lost network data internally.
- The application receives an error if the connection cannot be maintained.

TCP is a **byte stream**. It does not preserve application message boundaries. One send of 1,000 bytes may be returned by one receive operation or several smaller ones. The application therefore needs rules for identifying where a message or file ends.

This program does not implement TCP itself. Python asks the operating system for a TCP socket; the program defines what the bytes carried through that socket mean.

### The application protocol

The client and server use this simple protocol:

1. The client sends a filename followed by a newline: `hello.txt\n`.
2. If the file exists, the server sends `OK <size>\n`, then exactly `<size>` file bytes.
3. If the request fails, the server sends `ERR <reason>\n`.

Example:

```text
Client                                  Server
  | -------- TCP connection ----------> |
  | -------- "hello.txt\n" ------------> |
  | <------- "OK 37\n" ----------------- |
  | <------- 37 file bytes ------------- |
  | -------- connection closes -------- |
```

The newline marks the end of a text header. The byte count tells the client exactly how many file bytes it must read. These rules provide **framing** on top of TCP's byte stream.

### The protocol stack behind the transfer

Several layers cooperate during the transfer:

| Layer | Responsibility in this experiment |
| --- | --- |
| Application | The Python program defines the filename request, the `OK` and `ERR` responses, and the file-length rule. |
| Transport | TCP establishes the connection and supplies reliable, ordered bytes between the two programs. |
| Network | IP carries TCP segments between source and destination computers using IP addresses. |
| Link | Ethernet or Wi-Fi carries frames over the local physical network. |

The lab says "using TCP/IP," but TCP/IP does not define the filename format. This application defines that protocol; TCP transports its bytes.

The request passes through these transformations:

```text
Python string "hello.txt"
        |
UTF-8 encode
        v
Application bytes b"hello.txt\n"
        |
TCP divides and transports the byte stream
        |
IP routes the TCP data to the server
        |
Server TCP reassembles the ordered stream
        |
readline() reads through b"\n"
        |
UTF-8 decode
        v
Python string "hello.txt"
```

TCP may divide the bytes into segments differently on every run. The programs do not depend on those divisions; they depend only on the ordered byte stream.

### Exact application-protocol messages

Request:

```text
<UTF-8 filename>\n
```

Successful response:

```text
OK <decimal byte count>\n<exact file bytes>
```

Unsuccessful response:

```text
ERR <human-readable reason>\n
```

For example, `hello.txt\n` can produce `OK 37\n` followed by exactly 37 bytes. The response is interpreted in two stages: read one newline-terminated header, then, for `OK`, read exactly the declared body length.

The declared size is the file delimiter. Connection closure is not the normal delimiter, so the client can distinguish a complete file from a connection that failed halfway through.

### What TCP handles and what the application handles

TCP handles acknowledgements, retransmission, ordering, duplicate removal, flow control, and congestion control. This program handles connection setup, its message format, filename validation, filesystem access, exact-length reading, and application errors.

TCP does not guarantee that:

- One `sendall()` corresponds to one `read()`.
- A full application message arrives in one read.
- A server is running at the destination.
- A firewall permits the connection.
- Received bytes follow this program's protocol.
- A requested file exists.

## 3. Imported libraries and why they are required

All imports come from Python's standard library, so no `pip install` is required.

### `argparse`

`argparse` converts command-line text into validated program options. It lets the same scripts run with different hosts, ports, directories, filenames, and output paths without editing source code.

The code uses:

- `argparse.ArgumentParser(description=...)` to create the parser and generate help output.
- `parser.add_argument(...)` to declare arguments, types, defaults, and flags.
- `parser.parse_args()` to read the command line and return values such as `args.port`.
- `parser.error(...)` to show a usage error and stop for invalid client input.

### `socket`

`socket` is Python's interface to operating-system networking. It is the central networking library here.

The server uses `socket.socket()`, `setsockopt()`, `bind()`, `listen()`, and `accept()`. The client uses `socket.create_connection()`. Connected sockets use `sendall()` and `makefile()`.

### `pathlib.Path`

`Path` represents filesystem paths as objects. The server uses it to locate and create `shared`, join paths, validate the requested file, open it, and read its size. The client uses it for the optional output path. It also makes path operations portable across Windows, macOS, and Linux.

### `sys`

Only the client imports `sys`. It uses `sys.stdout.buffer`, the binary form of standard output, when no `--output` file is supplied. Normal `print()` expects text, while a transferred file contains arbitrary bytes.

### Built-in Python features

These require no import:

- `with` closes sockets and files even when an exception occurs.
- `encode()` converts text to bytes; `decode()` converts bytes to text.
- `len()` counts bytes, `int()` parses the byte count, and `min()` limits each read.
- `try`/`except` handles expected failures; `try`/`finally` guarantees cleanup.
- The `:=` assignment expression stores a chunk while checking whether it is empty.

## 4. Files and their purposes

### `tcp_file_server.py`

The server creates and binds a TCP socket, listens, accepts clients, validates each requested filename, and sends a file or error. It is required on the server computer.

### `tcp_file_client.py`

The client connects to the server, sends a filename, reads the response, and displays or saves the received file. It is required on the client computer.

### `shared/hello.txt`

This is a 37-byte sample file stored by the server. The `shared` folder represents files that the server is willing to provide.

The server creates the folder if necessary, but it does not create requested files. A file must be put in this folder before it can be received. The client requests `hello.txt`, not `shared/hello.txt`, because the server adds the shared-folder path itself.

### `README.md`

This document explains the experiment. The programs do not read it, so it is documentation rather than a runtime requirement.

## 5. Complete program flow

### Server flow

```text
Start
  |
Create TCP socket
  |
Bind to an IP address and port
  |
Listen and accept a client
  |
Read and validate the filename
  |
Does the file exist in shared/?
  |                         |
 Yes                        No
  |                         |
Send OK and byte count      Send ERR file not found
  |
Send file in chunks
  |
Close client connection
  |
Wait for another client unless --once was used
```

### Client flow

```text
Start
  |
Read command-line arguments
  |
Connect to server
  |
Send filename and newline
  |
Read response header
  |
Is it an ERR response?
  |                         |
 Yes                        No
  |                         |
Display error and exit      Read size from OK response
                            |
                            Read exactly that many bytes
                            |
                            Display or save the file
```

## 6. Server API and function reference

This section explains the inputs, outputs, blocking behavior, and purpose of the important server functions. The following line-by-line section shows where each is called.

### `serve_file(connection, shared_dir)`

This function is defined by the program. `connection` is the TCP socket returned by `accept()` for one client, and `shared_dir` is the `Path` containing available files. It reads one request, sends one response, and returns `None`.

### `connection.makefile("rb")`

This wraps the socket in a buffered file-like binary reader. `r` means read and `b` means bytes. It returns an object that supports `readline()` and `read()`. The data still comes from TCP; the wrapper makes buffered line reading convenient.

### `readline(4097)`

`readline()` waits until it receives a newline, reaches end of stream, reaches the size limit, or encounters a socket error. The 4,097-byte limit lets the server detect a line exceeding its allowed 4,096 bytes. It returns `bytes`.

### `request.endswith(b"\n")`

`endswith()` returns `True` when the request has the required newline delimiter. It checks application-protocol framing.

### `request[:-1].decode("utf-8")`

The slice removes the final newline. `decode()` converts the remaining UTF-8 bytes to a Python string and raises `UnicodeDecodeError` for invalid input.

### `connection.sendall(data)`

`sendall()` accepts bytes and repeatedly asks the operating system to send them until all are submitted or an error occurs. It returns `None` on success. Success does not mean the remote application has already processed the bytes.

### `Path(filename).name`

`.name` returns the final path component. Comparing it with the original rejects directory paths such as `folder/file.txt` and `../file.txt`.

### `shared_dir / filename`

`Path` overloads `/` to join path components. This constructs a candidate path without opening the file.

### `path.is_file()`

This returns `True` only when the path currently identifies a regular file. Missing paths and directories return `False`.

### `path.resolve()` and `.parent`

`resolve()` creates an absolute normalized path and resolves symbolic links. `.parent` obtains its containing directory. Their comparison confirms that the resolved file remains directly inside `shared`.

### `path.open("rb")`

This opens the file for binary reading and returns a file object. The `with` block closes it automatically. Opening can raise an `OSError` if permission is denied or the filesystem changes after validation.

### `path.stat().st_size`

`stat()` requests filesystem metadata; `st_size` is the byte length placed in the success header.

### `source.read(CHUNK_SIZE)`

`read(65536)` returns up to 65,536 bytes and may return fewer near the end. At end of file it returns `b""`, which ends the loop.

### `socket.socket(AF_INET, SOCK_STREAM)`

`AF_INET` selects IPv4 addresses represented by `(host, port)`. `SOCK_STREAM` selects TCP's byte-stream behavior. The new socket is not listening until it is bound and `listen()` is called.

### `server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)`

This enables the general socket option `SO_REUSEADDR`, helping a restarted server reuse its local address. It does not normally allow two active servers to use the same endpoint simultaneously.

### `server.bind((host, port))`

`bind()` assigns the socket's local IP address and port. It returns `None` or raises an `OSError`, for example if the address is unavailable or the port is occupied.

### `server.listen()`

`listen()` turns the bound socket into a passive listening socket and asks the operating system to queue connection attempts. It does not return a client socket.

### `server.accept()`

`accept()` blocks until a connection is ready. It returns a new connected socket and the client's address tuple. The original server socket remains available for later clients.

### `server.getsockname()`

This returns the socket's local address. Index `[1]` is the actual port, including an automatically assigned port if the program ever binds to port zero.

### Server exceptions

- `UnicodeDecodeError`: the filename is not valid UTF-8.
- `BrokenPipeError`: the server sends after the client has closed the connection.
- `ConnectionResetError`: the client forcibly resets the connection.
- `OSError`: the base class for many socket, permission, bind, and file failures.

Protocol and client-disconnection errors are handled explicitly. Setup and unexpected filesystem errors remain visible so the operator knows why the server failed.

## 7. Server code explained line by line

The line numbers refer to `tcp_file_server.py`. Blank lines only separate logical sections.

| Line | Explanation |
| --- | --- |
| 1 | The module docstring describes the file. `argparse` later uses it as help text. |
| 3 | Imports `argparse` for options such as `--host` and `--port`. |
| 4 | Imports Python's `socket` module for TCP communication. |
| 5 | Imports `Path` for filesystem paths. |
| 8 | Sets the chunk size to `64 * 1024`, or 65,536 bytes. Large files can be sent without loading them completely into memory. |
| 11 | Defines `serve_file()`, which handles one connected client. The annotations describe the expected argument types; `-> None` means it returns no useful value. |
| 12 | Enters a context manager that closes the connection when this block finishes. |
| 13 | Creates a binary reader for the socket and reads one line, with a 4,097-byte limit. |
| 14 | Rejects an empty request, a request longer than 4,096 bytes, or one without a final newline. |
| 15 | Sends `ERR invalid request\n`. The `b` prefix makes it a bytes value. |
| 16 | Stops processing this request. |
| 18 | Begins a `try` block because byte-to-text decoding can fail. |
| 19 | Removes the final newline with `request[:-1]` and decodes the remaining UTF-8 bytes into text. |
| 20 | Catches invalid UTF-8 input. |
| 21 | Sends an error explaining the required encoding. |
| 22 | Stops processing. |
| 24 | Documents the reason for filename validation. |
| 25 | Rejects an empty name, directory paths, and the special names `.` and `..`. |
| 26 | Sends `ERR invalid filename\n`. |
| 27 | Stops processing. |
| 28 | Joins the shared directory and filename to form the requested path. |
| 29 | Confirms that the path is a file and that its resolved parent is the shared directory. This prevents access to unrelated files. |
| 30 | Sends `ERR file not found\n`. |
| 31 | Stops processing the missing-file request. |
| 33 | Opens the file in binary read mode. Binary mode supports text, images, archives, and other file types without conversion. |
| 34 | Gets the byte size and sends a success header such as `OK 37\n`. The string is encoded into bytes. |
| 35 | Reads one chunk at a time. The `:=` operator assigns and tests the chunk; an empty result marks end of file. |
| 36 | Sends the whole current chunk. `sendall()` handles partial low-level writes. |
| 39 | Defines the main server setup and loop. |
| 40 | Creates the command-line parser. |
| 41 | Adds `--host`; its default `127.0.0.1` accepts only same-machine clients. |
| 42 | Adds integer option `--port`, defaulting to `5001`. |
| 43 | Adds `--shared-dir`. By default it is the `shared` folder beside the server script, regardless of the current terminal directory. |
| 44 | Adds `--once`, which makes the server stop after one client. |
| 45 | Parses command-line arguments and stores them in `args`. |
| 46 | Creates the shared directory and missing parent directories. `exist_ok=True` avoids an error if it already exists. |
| 48 | Creates an IPv4 TCP socket. `AF_INET` selects IPv4; `SOCK_STREAM` selects TCP. The context manager later closes it. |
| 49 | Enables `SO_REUSEADDR`, helping the server reuse the address soon after a previous run. |
| 50 | `bind()` assigns the selected local address and port to the socket. |
| 51 | `listen()` puts the socket into listening mode. |
| 52 | Prints the actual listening address and port. `flush=True` displays it immediately. |
| 53 | Starts a loop so the server can serve further clients sequentially. |
| 54 | `accept()` waits for a client and returns a new connection socket plus the client's address. Waiting here is normal. |
| 55 | Prints the client address. Its port is normally a temporary port selected by the client's operating system. |
| 56 | Begins error handling for this connection. |
| 57 | Calls `serve_file()` to process the request. |
| 58 | Catches a broken or reset connection if the client disconnects during transfer. |
| 59 | Prints that error rather than unexpectedly terminating the server. |
| 60 | Checks whether `--once` was supplied. |
| 61 | Ends the loop after one client when `--once` is active. |
| 64 | Checks whether the file was run directly rather than imported. |
| 65 | Calls `main()` to start the server. |

## 8. Client API and function reference

### `main()`

This program-defined function parses arguments, opens one connection, sends one request, receives one response, and exits.

### `socket.create_connection((host, port), timeout=5)`

This convenience function resolves the host if needed, creates a suitable TCP socket, connects it, and returns the connected socket. The timeout prevents network operations from waiting forever. Failures can raise `socket.timeout`, `ConnectionRefusedError`, or another `OSError`.

### `connection.sendall((filename + "\n").encode("utf-8"))`

The expression appends the protocol delimiter, converts the complete string to UTF-8 bytes, and sends every request byte.

### `reader.readline(4097)`

This reads one response header with a safety limit. The first newline ends the header, so later file bytes are not decoded as header text.

### `header.startswith(prefix)`

`startswith()` returns a Boolean indicating whether the bytes begin with a recognized prefix. Checking `ERR ` first separates an application error from a successful response.

### `header.decode("utf-8", errors="replace").strip()`

`decode()` converts error bytes into displayable text. `errors="replace"` substitutes a marker for malformed bytes instead of raising another error. `strip()` removes the ending newline and surrounding whitespace.

### `int(header[3:].strip())`

The slice removes `OK `, `strip()` removes the newline, and `int()` parses the decimal byte count. Invalid numeric text raises `ValueError` because the response is malformed.

### `args.output.open("wb")`

This opens the destination for binary writing. `w` creates or truncates the file; `b` prevents text conversion. It returns a file object with `write()` and `close()` methods.

### `sys.stdout.buffer`

This is standard output's underlying binary stream. It allows arbitrary received bytes to be written without decoding them as text.

### `reader.read(min(64 * 1024, remaining))`

`min()` chooses the smaller of the chunk limit and bytes still expected. `read()` may return fewer bytes than requested, so the loop subtracts the actual length and repeats. An empty result while `remaining` is positive means an incomplete transfer.

### `destination.write(chunk)`

`write()` places bytes in the output file or terminal and returns the number written. Closing a buffered file flushes pending output to the operating system.

### `raise RuntimeError(...)`

`raise` stops normal execution. `RuntimeError` reports a malformed protocol response or incomplete transfer that should not occur during a valid exchange.

### `raise SystemExit(...)`

`SystemExit` ends the client cleanly with the server's message. It is used for an expected application error, such as a missing file, rather than malformed protocol data.

## 9. Client code explained line by line

The line numbers refer to `tcp_file_client.py`.

| Line | Explanation |
| --- | --- |
| 1 | The module docstring describes the client. |
| 3 | Imports `argparse` for command-line input. |
| 4 | Imports `socket` for the TCP connection. |
| 5 | Imports `sys` to access the terminal's binary output. |
| 6 | Imports `Path` for the optional output-file path. |
| 9 | Defines the client's `main()` function. |
| 10 | Creates the command-line parser. |
| 11 | Adds the required filename argument: a direct filename in the server's shared directory. |
| 12 | Adds the server address, defaulting to same-machine address `127.0.0.1`. |
| 13 | Adds the server port, defaulting to `5001`. It must match the server. |
| 14 | Adds optional `--output`. Without it, received bytes go to the terminal. |
| 15 | Parses the command-line arguments. |
| 16 | Rejects newline and carriage-return characters because they would break the line-based request. |
| 17 | Displays a command-line error and stops for such a filename. |
| 19 | Opens a TCP connection with a five-second connection timeout. The context manager closes it later. |
| 20 | Appends a newline to the filename, converts it to UTF-8 bytes, and sends the whole request. |
| 21 | Creates a binary file-like reader for the socket. |
| 22 | Reads the server's response header as one length-limited line. |
| 23 | Rejects a missing, overlong, or unterminated response. |
| 24 | Raises an invalid-response error. |
| 25 | Checks for an `ERR ` response. |
| 26 | Decodes and displays the error, then exits. `errors="replace"` handles malformed text safely. |
| 27 | Checks that a non-error response begins with `OK `. |
| 28 | Rejects an unknown response. |
| 29 | Extracts and converts the byte count after `OK ` into an integer. |
| 30 | Checks for an impossible negative size. |
| 31 | Rejects a negative size. |
| 33 | Opens `--output` in binary write mode or selects terminal output. `wb` creates or overwrites the output file. |
| 34 | Starts a `try` block so an output file can be closed even after a receive error. |
| 35 | Records how many file bytes remain to be received. |
| 36 | Continues reading until the remaining count reaches zero. A zero-byte file skips this loop correctly. |
| 37 | Reads at most 65,536 bytes and never more than the amount remaining. It does not assume one read returns the entire file. |
| 38 | Detects the connection closing before all promised bytes arrive. |
| 39 | Raises an incomplete-transfer error. |
| 40 | Writes received bytes to the selected destination. |
| 41 | Subtracts the received length from the amount remaining. |
| 42 | Begins cleanup that runs even after an error. |
| 43 | Checks whether an output file was opened. |
| 44 | Closes that file. The terminal's standard output is not closed. |
| 45 | After the connection closes, checks whether an output file was used. |
| 46 | Reports the received byte count and output path. |
| 49 | Checks whether the file was run directly. |
| 50 | Calls `main()` to start the client. |

## 10. Requirements on another machine

### Software

- Python 3.10 or newer.
- No third-party Python packages; only the standard library is used.
- A terminal or command prompt.
- No internet connection when using one machine or an available local network.

Check Python:

```bash
python3 --version
```

On Windows, the command may be:

```powershell
py -3 --version
```

### Files

For a same-machine demonstration, use this structure:

```text
question_01_tcp_file_transfer/
|-- tcp_file_server.py
|-- tcp_file_client.py
`-- shared/
    `-- hello.txt
```

For two machines:

- The server computer needs `tcp_file_server.py` and `shared/` with the requested file.
- The client computer needs `tcp_file_client.py`.
- The client does not need the file before the transfer.

### Network access

- The chosen TCP port must be available.
- For two machines, the network must allow them to reach one another.
- The server firewall must permit incoming TCP traffic on the port.
- The client must know the server's IP address.

## 11. Running both programs on one machine

Open two terminals in this directory and start the server first.

Terminal A:

```bash
python3 tcp_file_server.py
```

Expected output:

```text
TCP file server listening on 127.0.0.1:5001
```

The server then waits in `accept()`; it is not frozen.

Terminal B:

```bash
python3 tcp_file_client.py hello.txt
```

Expected client output:

```text
Hello from the CY52 TCP file server.
```

The server prints a line similar to:

```text
Client connected: ('127.0.0.1', 53124)
```

The exact client port varies.

Save the file instead of printing it:

```bash
python3 tcp_file_client.py hello.txt --output received.txt
```

Expected output:

```text
Received 37 bytes into received.txt
```

Test a missing file:

```bash
python3 tcp_file_client.py missing.txt
```

Expected output:

```text
ERR file not found
```

Stop the server with `Ctrl+C`, or make it stop after one client:

```bash
python3 tcp_file_server.py --once
```

On Windows, replace `python3` with `py -3` if necessary.

## 12. Running on two machines

1. Connect both computers to a network that permits communication.
2. Find the server computer's local IP address.
3. Put the requested file in the server's `shared` folder.
4. Start the server on all of its network interfaces:

```bash
python3 tcp_file_server.py --host 0.0.0.0
```

5. On the client computer, use the server's actual IP address:

```bash
python3 tcp_file_client.py hello.txt --host 192.168.1.20
```

Replace `192.168.1.20` with the real server address. Do not use `0.0.0.0` as the client destination.

If port `5001` is unavailable, pass the same different port to both:

```bash
# Server
python3 tcp_file_server.py --host 0.0.0.0 --port 6000

# Client
python3 tcp_file_client.py hello.txt --host 192.168.1.20 --port 6000
```

## 13. Expected behavior and common problems

| Situation | Expected behavior or solution |
| --- | --- |
| Server has started but no client is connected | It prints the listening message and waits. This is normal. |
| Existing file requested | The server sends `OK`, the byte count, and the file; the client displays or saves it. |
| Missing file requested | The server sends `ERR file not found`; the client displays it. |
| Client starts before server | Connection fails, commonly with "connection refused." Start the server first. |
| Wrong server IP | Connection fails or times out. Use `127.0.0.1` only on the same machine. |
| Different client and server ports | They do not connect. Supply the same port to both. |
| Port already occupied | The server fails at `bind()`. Stop the other process or choose another port. |
| Firewall blocks the port | The connection fails or times out. Permit incoming TCP traffic to that server port. |
| Output file already exists | Opening it with `wb` overwrites its previous contents. |
| Server uses `--once` | It exits after serving one client; otherwise it waits for more. |
| Client disconnects during transfer | The server catches a broken-pipe or reset error. |
| Large file requested | It is sent in 65,536-byte chunks rather than loaded completely into memory. |

## 14. Why the design works this way

### Why send the size before the file?

TCP does not mark a file boundary. The size tells the client when the complete file has arrived and lets it detect an early disconnection.

### Why use a receiving loop?

A TCP read can return fewer bytes than requested even when more bytes are coming. The loop continues until the announced size has arrived.

### Why use `sendall()`?

A low-level socket send may accept only part of the supplied data. `sendall()` continues until all bytes are sent or an error occurs.

### Why use binary mode?

Binary mode preserves exact bytes and supports text files, images, archives, and other types. Text mode might perform newline or encoding conversions.

### Why send chunks?

Chunking keeps memory use bounded. A large file does not have to fit completely in program memory.

### Why restrict the shared directory?

Without validation, a client might request `../private.txt` and access an unintended file. This server accepts only direct filenames within `shared`.

### Why does the server use two sockets?

The original socket keeps listening. `accept()` returns a new socket for communication with one client, allowing the server to return to listening after that request.

## 15. Exam and viva points

- Server sequence: `socket()` -> `bind()` -> `listen()` -> `accept()` -> receive -> send.
- Client sequence: connect -> send filename -> read header -> read the exact file size.
- `AF_INET` means IPv4.
- `SOCK_STREAM` means TCP.
- `127.0.0.1` reaches only the same computer.
- The IP address identifies the computer; the port identifies the program.
- TCP is reliable and ordered, but it is a byte stream and does not preserve application message boundaries.
- The newline frames a text header; the byte count frames the file body.
- One receive operation is not guaranteed to return all requested bytes.
- A missing file produces an error, not a successful empty file.
- `bind()`, `listen()`, and `accept()` are server operations; connecting is a client operation.

### Short viva explanation

This program demonstrates TCP client-server file transfer. The server creates an IPv4 stream socket, binds it to an address and port, listens, and accepts a client. The client connects and sends a filename terminated by a newline. The server validates the name and checks its shared directory. If the file exists, it sends a success header containing the byte count and then sends the file in chunks; otherwise, it sends an error. Because TCP is a byte stream, the client reads repeatedly until it has received the announced number of bytes. Binary mode preserves the file's original contents.
