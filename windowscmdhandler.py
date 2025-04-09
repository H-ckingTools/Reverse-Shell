import os

def command_handler(cmd):
    getcmd = f'powershell -Command {cmd}'
    output = os.popen(getcmd)
    return output.read().strip()