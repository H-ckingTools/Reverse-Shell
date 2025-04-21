from threading import Thread


def printf(string):
    global getvalue
    getvalue = string+' is fucking'

a = Thread(target=printf,args=('hathim',)).start()
print(getvalue)