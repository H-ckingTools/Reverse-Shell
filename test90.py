# import psutil

# battery = psutil.sensors_battery()

# if battery is not None:
#     print(f"Battery Percentage: {battery.percent}%")
# else:
#     print("Battery info not available on this system.")

import json

with open('path.json') as pathfile:
    get_content = pathfile.read()
    print(json.loads(get_content)['update'])