import tkinter as tk
from tkinter import ttk, messagebox
import importlib.util
import subprocess
import threading
import sys

REQUIRED_MODULES = ['colorama', 'psutil', 'pynput']

def is_installed(module_name):
    return importlib.util.find_spec(module_name) is not None

def get_missing_modules():
    return [mod for mod in REQUIRED_MODULES if not is_installed(mod)]

def install_missing_modules():
    missing_modules = get_missing_modules()
    total = len(missing_modules)
    for index, module in enumerate(missing_modules):
        status_label.config(text=f"Installing {module}...")
        progress['value'] = ((index + 1) / total) * 100
        root.update_idletasks()
        subprocess.call([sys.executable, '-m', 'pip', 'install', module])

    progress['value'] = 100
    status_label.config(text="✅ All missing modules installed!")
    messagebox.showinfo("Success", "All missing modules installed successfully!")
    root.after(1000, lambda: [root.destroy(), callback()])

def start_installation_thread():
    threading.Thread(target=install_missing_modules, daemon=True).start()

def show_all_good_window():
    """Only show success window if everything is installed."""
    window = tk.Tk()
    window.title("Dependency Check")
    window.geometry("350x120")
    window.resizable(False, False)

    tk.Label(window, text="✅ All dependencies are already installed.", font=("Arial", 12)).pack(pady=20)
    tk.Button(window, text="OK", command=lambda: [window.destroy(), callback()]).pack(pady=10)

    window.mainloop()

def show_installer_window():
    """Show installer window if dependencies are missing."""
    global root, status_label, progress

    root = tk.Tk()
    root.title("Dependency Installer")
    root.geometry("400x200")
    root.resizable(False, False)

    tk.Label(root, text="Missing dependencies found!", font=("Arial", 14)).pack(pady=10)

    progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progress.pack(pady=10)

    status_label = tk.Label(root, text="Ready to install missing modules.")
    status_label.pack()

    install_button = tk.Button(root, text="Install Now", command=start_installation_thread)
    install_button.pack(pady=10)

    root.mainloop()

def check_dependencies_and_continue(user_callback):
    """Entry point to check and handle dependencies."""
    global callback
    callback = user_callback
    missing = get_missing_modules()

    if not missing:
        show_all_good_window()
    else:
        show_installer_window()
