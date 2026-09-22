"""Read hexadecimal segments, calculate their checksum, and send both."""

import socket

from checksum import checksum


segments = [int(input(f"Enter segment {i + 1} (hex): "), 16) for i in range(10)]
value = checksum(segments)
print("Checksum:", hex(value))

message = " ".join(hex(segment) for segment in segments) + " " + hex(value)

client = socket.socket()
client.connect(("localhost", 5002))
client.sendall(message.encode())
print("Server:", client.recv(1024).decode())
client.close()
