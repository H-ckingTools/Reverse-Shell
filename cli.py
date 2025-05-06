import socket as st

sock = st.socket(st.AF_INET,st.SOCK_STREAM)
sock.bind(('192.168.50.94',1111))
sock.setsockopt(st.SOL_SOCKET,st.SO_REUSEPORT,1)
sock.listen()

con,addr = sock.accept()
while True:
    cmd = input('>>>')
    if cmd == 'say':
        con.send('hello'.encode())
        continue
    else:
        continue