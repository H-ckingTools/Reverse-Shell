import socket as s


sock = s.socket(s.AF_INET,s.SOCK_STREAM)
sock.bind(('192.168.81.156',2222))
sock.listen()
con,add = sock.accept()
print(add[0])