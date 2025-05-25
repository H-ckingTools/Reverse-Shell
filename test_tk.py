import tkinter as tk
from tkinter import ttk

def start_download():
    progress['value'] = 0
    max_steps = 100
    step_delay = 50  # milliseconds

    def step():
        if progress['value'] < max_steps:
            progress['value'] += 1
            root.after(step_delay, step)
        else:
            label.config(text="Download Complete!")

    step()

root = tk.Tk()
root.title("Download Progress Bar")

label = tk.Label(root, text="Click 'Start Download' to begin")
label.pack(pady=10)

progress = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
progress.pack(pady=10)

start_button = tk.Button(root, text="Start Download", command=start_download)
start_button.pack(pady=10)

root.mainloop()
