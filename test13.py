# from os import stat

# if stat('/usr/bin/code'):
#     print('Its ran now')
# else:
#     print('Not')

import psutil
import time

# Continuously list all running processes with windows in real-time
try:
    while True:
        output = ""
        # Get the list of all processes
        for proc in psutil.process_iter(['pid', 'name', 'status']):
            try:
                # Only include processes with windows (foreground applications)
                if proc.info['status'] == 'running':
                    output += f"PID: {proc.info['pid']}, Name: {proc.info['name']}, Status: {proc.info['status']}   "
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass  # Ignore processes that terminate or are inaccessible

        # Clear the screen (overwrite the previous output) before printing new output
        print(f"\r{output}{' ' * (100 - len(output))}", end='', flush=True)

        time.sleep(1)  # Wait for a second before refreshing the list

except KeyboardInterrupt:
    print("\nProcess monitoring stopped.")
