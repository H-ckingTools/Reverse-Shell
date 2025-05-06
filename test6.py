import psutil
import socket as st

def get_network_infos():
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
                    mac = getinfo.address
                
            return f"""
        Interface name : {interface}
        IP address : {ip}
        MAC address : {mac}
        Net mask address : {netmask}
        Broadcast address : {broadcast} 
            """
        

print(get_network_infos())