"""Request and display a text file from the TCP server."""

import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 5001))

filename = input("Enter file name: ")
client.sendall(filename.encode())

print("File contents:")
while True:
    data = client.recv(1024)
    if not data:
        break
    print(data.decode(), end="")

print()
client.close()
