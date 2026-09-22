"""Receive one UDP message and send a reply."""

import socket


HOST = "127.0.0.1"
PORT = 5000
BUFFER_SIZE = 1024

#Socket creation and binding to the specified host and port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print("Server waiting...")
data, client_address = server_socket.recvfrom(BUFFER_SIZE)
print("Client:", data.decode("utf-8"))

reply = "Hello from Server"
server_socket.sendto(reply.encode("utf-8"), client_address)
server_socket.close()
