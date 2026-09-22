"""Receive hexadecimal segments and verify their checksum."""

import socket

from checksum import checksum


server = socket.socket()
server.bind(("localhost", 5002))
server.listen(1)
print("Server waiting...")

connection, address = server.accept()
values = connection.recv(1024).decode().split()
segments = [int(value, 16) for value in values[:-1]]
received_checksum = int(values[-1], 16)
calculated_checksum = checksum(segments)

print("Received checksum:", hex(received_checksum))
print("Calculated checksum:", hex(calculated_checksum))
result = "Checksum CORRECT" if received_checksum == calculated_checksum else "Checksum WRONG"
print(result)

connection.sendall(result.encode())
connection.close()
server.close()
