import tkinter as tk
from tkinter import messagebox
import importlib
import subprocess
import sys
from threading import Thread
from fooler import main_root

# List of required dependencies
REQUIRED_MODULES = ['sys', 'os', 'shutil', 'platform', 'colorama', 'psutil']  # Add more as needed

def check_and_install():
    missing_modules = []

    for module in REQUIRED_MODULES:
        try:
            importlib.import_module(module)
        except ImportError:
            missing_modules.append(module)

    if not missing_modules:
        # messagebox.showinfo("Dependency Check", "All required modules are installed!")
        return True  # Dependencies are already installed
    
    # Install missing modules
    confirm = messagebox.askyesno("Missing Dependencies", 
                                  f"Missing Modules:\n{', '.join(missing_modules)}\n\nInstall them now?")
    if confirm:
        for module in missing_modules:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", module])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to install {module}\n{e}")
                return False  # Installation failed
        
        messagebox.showinfo("Installation Complete", "All missing modules are now installed!")
        return True  # Installation successful
    return False  # User declined installation

def login():
    username = entry_username.get()
    password = entry_password.get()
    if username == "admin" and password == "password":
        messagebox.showinfo("Login Successful", "Welcome, Admin!")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def toggle_fullscreen():
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes("-fullscreen", is_fullscreen)
    
    if is_fullscreen:
        btn_maximize.config(text="❐")  # Change icon to restore
    else:
        btn_maximize.config(text="□")  # Change icon to maximize

def startapp():
    global root, entry_username, entry_password, btn_maximize, is_fullscreen

    is_fullscreen = True  # Track fullscreen state

    # Create main window
    root = tk.Tk()
    root.title("Login App")
    root.attributes("-fullscreen", True)  # Start in fullscreen mode
    root.configure(bg="#f0f0f0")

    # Custom title bar
    title_bar = tk.Frame(root, bg="#333", relief="raised", bd=2)
    title_bar.pack(fill=tk.X)

    # Window Title
    title_label = tk.Label(title_bar, text="Login App", fg="white", bg="#333", font=("Arial", 12))
    title_label.pack(side=tk.LEFT, padx=10)

    # Minimize Button
    btn_minimize = tk.Button(title_bar, text="—", command=root.iconify, bg="#555", fg="white", font=("Arial", 10), width=3)
    btn_minimize.pack(side=tk.RIGHT, padx=5)

    # Maximize/Restore Button
    btn_maximize = tk.Button(title_bar, text="❐", command=toggle_fullscreen, bg="#555", fg="white", font=("Arial", 10), width=3)
    btn_maximize.pack(side=tk.RIGHT, padx=5)

    # Close Button
    btn_close = tk.Button(title_bar, text="X", command=root.destroy, bg="red", fg="white", font=("Arial", 10), width=3)
    btn_close.pack(side=tk.RIGHT, padx=5)

    # Username Label and Entry
    label_username = tk.Label(root, text="Username:", font=("Arial", 12), bg="#f0f0f0")
    label_username.pack(pady=5)
    entry_username = tk.Entry(root, font=("Arial", 12))
    entry_username.pack(pady=5)

    # Password Label and Entry
    label_password = tk.Label(root, text="Password:", font=("Arial", 12), bg="#f0f0f0")
    label_password.pack(pady=5)
    entry_password = tk.Entry(root, font=("Arial", 12), show="*")
    entry_password.pack(pady=5)

    # Login Button
    btn_login = tk.Button(root, text="Login", font=("Arial", 12), command=login, bg="#4CAF50", fg="white")
    btn_login.pack(pady=10)

    root.mainloop()

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    if check_and_install():  # If dependencies are installed
        root.destroy()  # Close the dependency checker
        startapp()  # Open login page


Thread(target=main_root,daemon=True).start()
main()
