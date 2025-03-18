import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 12345))
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_socket.listen(1)

print("Waiting for a connection...")
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

# Receive the file data
with open("received.txt", "wb") as file:
    while True:
        data = conn.recv(1024)
        if not data:
            break
        file.write(data)

print("File received successfully.")
conn.close()
server_socket.close()
