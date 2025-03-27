import netifaces,os

os.system('clear')

ifaces = netifaces.interfaces()
IPv4 = netifaces.AF_INET
IPv6 = netifaces.AF_LINK
for no,inet in enumerate(ifaces):
    addr = netifaces.ifaddresses(inet)
    if IPv4 in addr and IPv6 in addr:
        print('interface',no+1)
        print('name:',inet)
        print("ipv4",addr[2][0]['addr'])
        print("ipv6",addr[17][0]['addr'])
        print('\n')
