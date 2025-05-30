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
parse = cmd.splitlines()[1].split(' ')
get_details = []
for i in parse:
    if i != '':
        get_details.append(i)
    else:
        pass


comments = ''        
for j,k in enumerate(get_details):
    if j >= 2:
        comments += k + ' '
    else:
        pass
print(get_details)