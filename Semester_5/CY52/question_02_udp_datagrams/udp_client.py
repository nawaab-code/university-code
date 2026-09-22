"""Send one UDP message and display the server's reply."""

import socket


HOST = "127.0.0.1"
PORT = 5000
BUFFER_SIZE = 1024


client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = "Hello Server"
client_socket.sendto(message.encode("utf-8"), (HOST, PORT))

data, server_address = client_socket.recvfrom(BUFFER_SIZE)
print("Server:", data.decode("utf-8"))

client_socket.close()
