cmd = '''
Git                                     2.49.0         The Git Development Community
Google Chrome                           136.0.7103.114 Google LLC                   
Microsoft Edge                          136.0.3240.50  Microsoft Corporation        
Microsoft Edge WebView2 Runtime         136.0.3240.50  Microsoft Corporation        
Microsoft Update Health Tools           3.74.0.0       Microsoft Corporation        
Oracle VirtualBox Guest Additions 7.1.6 7.1.6.167084   Oracle and/or its affiliates 
Python 3.13.1 Add to Path (64-bit)      3.13.1150.0    Python Software Foundation   
Python 3.13.1 Core Interpreter (64-bit) 3.13.1150.0    Python Software Foundation   
Python 3.13.1 Standard Library (64-bit) 3.13.1150.0    Python Software Foundation   
Python 3.13.2 Add to Path (64-bit)      3.13.2150.0    Python Software Foundation   
Python 3.13.2 Core Interpreter (64-bit) 3.13.2150.0    Python Software Foundation   
Python 3.13.2 Standard Library (64-bit) 3.13.2150.0    Python Software Foundation   
Python Launcher                         3.13.2150.0    Python Software Foundation  
'''


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

for a,b in enumerate(cmd.splitlines()):
    if a == 0:
        pass
    else:
        d = getappinfo(b)
        for x,y in d:
            if 'chrome' in str(y).lower():
                print('yeah')
                break
