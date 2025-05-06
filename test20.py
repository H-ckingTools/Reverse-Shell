import sys
import io
from os import system
from threading import Thread
import time

def clear():
    while True:
        buffer = io.StringIO()
        sys.stdout = buffer
        if sys.stdout:
            system('clear')
            time.sleep(1)
        else:
            pass
Thread(target=clear,daemon=True).start()

while True:
    print('hello')
    time.sleep(1)


