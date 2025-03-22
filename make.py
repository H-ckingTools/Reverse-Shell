from setuptools import setup
import cx_Freeze

setup(
    name="MyApp",
    version="1.0",
    description="My Python application",
    executables=[cx_Freeze.Executable("app/maingame.py", target_name="MyApp.exe")]
)
