# import subprocess

# proc = subprocess.Popen(['cat server.py'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE,shell=True)
# a,b = proc.communicate()
# print(a.decode())

import json

name = {'ifhnsdg','aisdfhnosidfb'}

name = json.loads(name)

print(name)