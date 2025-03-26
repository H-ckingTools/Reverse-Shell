import psutil

getinets = psutil.net_if_addrs()
for a,b in getinets.items():
    print(a)
    # print(b[0][1])