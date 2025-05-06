import socket as st

sock = st.socket(st.AF_INET,st.SOCK_STREAM)
sock.connect(('192.168.50.94',1111))
while True:
    cmd = sock.recv(1024).decode()
    if cmd == '':
        pass
