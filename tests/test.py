import psutil


a = psutil.net_if_addrs()
# print(a.values())

# for geti in a.keys():
#     print(geti)

# print('interface name :',a['lo'])
getaddr = str(a['lo']).split()
# for i in getaddr.split():
#     print(i)

b = getaddr[2]
c = b[b.index('=')+1:]
d = c.replace('\'','')
print(d.replace(',',''))
# print(psutil.net_connections(kind='inet'))
# print(psutil.net_if_addrs())