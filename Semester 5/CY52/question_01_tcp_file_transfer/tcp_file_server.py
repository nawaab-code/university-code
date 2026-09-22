"""Send a requested text file to one TCP client."""

import socket


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 5001))
server.listen(1)
print("Server waiting...")

connection, address = server.accept()
filename = connection.recv(1024).decode()
print("Client requested:", filename)

try:
    with open("shared/" + filename, "r") as file:
        data = file.read()
except FileNotFoundError:
    data = "File not found"

connection.sendall(data.encode())
connection.close()
server.close()
