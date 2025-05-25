import urllib3
import tkinter as tk
from tkinter import messagebox
from importlib import import_module
import subprocess

class Dependencies_Installer:
    def __init__(self):
        self.deps = ['tk','urllib3',"socket","os","shutil","platform","psutil","stat","sys"]
        self.main_window = tk.Tk()

    def internet_con(self):
        make_req = urllib3.PoolManager()
        try:
            make_req.request('GET','www.google.com')
            return True
        except Exception:
            return False

    def install_dependencies(self,module_name):
        for installing in self.deps:
            try:
                import_module(installing)
            except ModuleNotFoundError:
                subprocess.check_call(['pip','install',module_name],creationflags=subprocess.CREATE_NO_WINDOW)
                self.main_window.withdraw()
            messagebox.showinfo(title='Antivirus App(Installer)',message='Dependencies installed so,be patient')

a = Dependencies_Installer()
a.install_dependencies()