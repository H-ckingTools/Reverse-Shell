from pynput import keyboard
import win32api, win32con, time

# print("Press Ctrl+C to exit...\n")

def getcaps_state():
    while True:
        caps = win32api.GetKeyState(win32con.VK_CAPITAL)
        print("CapsLock is", "ON" if caps else "OFF")
        time.sleep(1)

caps = False
def caps(key):
    global caps
    if key == keyboard.Key.caps_lock:
        if caps == False:
            caps = True
        else:
            caps = False
    else:
        if caps == True:
            print(str(key).upper())
        else:
            print(str(key).lower())

with keyboard.Listener(on_press=caps) as kl:
    kl.join()