from os import popen

def command_handler(cmd):
    getcmd = f'powershell -Command {cmd}'
    output = popen(getcmd)
    return output.read().strip()

def getappinfo(infos):
    parse = infos.split(' ')
    b = []
    desc = ''
    arr = {}

    for prs in parse:
        if prs != '':
            b.append(prs)

    for index1,content in enumerate(b):
        if index1 > 1:
            desc += content + ' '

    arr.update({'app_name':b[0]})
    arr.update({'app_version':b[1]})
    arr.update({'app_description':desc})

    return arr.items()