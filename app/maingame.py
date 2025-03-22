import tkinter as tk
from tkinter import messagebox
from threading import Thread
from app.fooler import main,check_dependencies


def login():
    username = entry_username.get()
    password = entry_password.get()
    if username == "admin" and password == "password":
        messagebox.showinfo("Login Successful", "Welcome, Admin!")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")


def startapp():
    global entry_username,entry_password
    check_dependencies()
    # Create main window
    root = tk.Tk()
    root.title("Login App")
    root.geometry("300x200")
    root.configure(bg="#f0f0f0")

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

Thread(target=main,daemon=True).start()
startapp()