import os

class commands:
    cmds = ['ls','cd','remove','add','remove all']
    def _help():
        hlp = """
        ls - list all files and folders from the target device\n
        cd [source directory] - change current directory into source directory on the target device
        """
        print(hlp,end='\n',flush=True)

    def list_files():
        gettdir = os.getcwd()
        return os.listdir(gettdir)
    
    def change_dir(cd_path:str):
        if os.path.isdir(cd_path):
            if os.path.exists(cd_path):
                os.chdir(cd_path)
                return True
            else:
                return 'Error : directory doesnt exist'
        else:
            return f'\'{cd_path}\' is not a directory'
    
