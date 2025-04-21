from os import popen

def command_handler(cmd):
    getcmd = f'powershell -Command {cmd}'
    output = popen(getcmd)
    return output.read().strip()