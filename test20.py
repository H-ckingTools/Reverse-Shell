# import sys
# import io
# from os import system
# from threading import Thread
# import time

# def clear():
#     while True:
#         buffer = io.StringIO()
#         sys.stdout = buffer
#         if sys.stdout:
#             system('clear')
#             time.sleep(1)
#         else:
#             pass
# Thread(target=clear,daemon=True).start()

# while True:
#     print('hello')
#     time.sleep(1)

import subprocess

powershell_command = '''
Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*, HKLM:\\Software\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* |
Where-Object { $_.DisplayName -and $_.DisplayName -notmatch "Test Suite|Documentation|Development Libraries|Tcl/Tk|Bootstrap|Executables" } |
Select-Object DisplayName, DisplayVersion, Publisher |
Sort-Object DisplayName
'''

# Run the PowerShell command
get_all = subprocess.check_output(
    ["powershell", "-Command", powershell_command],
    universal_newlines=True,
    creationflags=subprocess.CREATE_NO_WINDOW
)

print(get_all)

