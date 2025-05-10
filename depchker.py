import tkinter as tk
from tkinter import ttk
import importlib.util
import subprocess
import threading
import sys

REQUIRED_MODULES = ['colorama', 'psutil', 'pynput', 'requests']

def is_installed(module_name):
    return importlib.util.find_spec(module_name) is not None

def get_missing_modules():
    return [m for m in REQUIRED_MODULES if not is_installed(m)]

def install_dependencies(on_complete=None):
    def run_installer():
        missing = get_missing_modules()
        if not missing:
            root.after(100, safe_on_complete)  # avoid double trigger
            return

        def install():
            total = len(missing)
            for i, module in enumerate(missing):
                label_var.set(f"Installing {module}...")
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "--user", module],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                progress['value'] = ((i + 1) / total) * 100
                root.update_idletasks()

            label_var.set("All dependencies installed.")
            root.after(1000, safe_on_complete)

        threading.Thread(target=install, daemon=True).start()

    def safe_on_complete():
        if root.winfo_exists():
            root.destroy()
        if on_complete and not getattr(safe_on_complete, "_called", False):
            safe_on_complete._called = True
            on_complete()

    safe_on_complete._called = False  # prevent double call

    root = tk.Tk()
    root.title("Dependency Installer")
    root.geometry("400x150")
    root.resizable(False, False)

    label_var = tk.StringVar(value="Checking dependencies...")
    ttk.Label(root, textvariable=label_var, font=("Segoe UI", 10)).pack(pady=20)

    progress = ttk.Progressbar(root, length=300, mode='determinate')
    progress.pack(pady=10)

    threading.Thread(target=run_installer, daemon=True).start()
    root.mainloop()
