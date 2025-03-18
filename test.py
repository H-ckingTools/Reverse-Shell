import socket

server_ip = "127.0.0.1"
server_port = 12345

# Create a socket and connect
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# Open a file in binary mode and send it
with open("example.txt", "rb") as file:
    print(file)
    client_socket.sendfile(file)

client_socket.close()
