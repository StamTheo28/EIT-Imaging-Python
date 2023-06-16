import sys

from cx_Freeze import Executable, setup


base = None
if sys.platform == 'win32':
    base = "Win32GUI"

build_exe_options = {
    "packages": ["tkinter", "matplotlib", "webbrowser", "pandas", "visualisation", "openpyxl", "typing",
                 "pyeit.eit.greit", "pyeit.mesh", "pyeit.eit.fem", "pyeit.eit.utils", "pyeit.mesh.shape",
                 "numpy", "matplotlib.pyplot"],
    "include_files": ["vascusens_logo_icon.ico"]
}

setup(
    name="VascuSens-CLIENT",
    options={"build_exe": build_exe_options},
    version="1.0",
    description="VasuSens Client Application",
    executables=[Executable("main.py", base=base, icon="vascusens_logo_icon.ico", target_name="VascuSensVis.exe")]
)
