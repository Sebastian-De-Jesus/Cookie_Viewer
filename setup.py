import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [Executable("cookie.py", base=base)]

options = {
    "build_exe": {
        "include_files": ["cookie-database.csv"],
    }
}

setup(
    name="Cookie Scanner",
    version="1.0",
    description="Cookie Scanner Application",
    executables=executables,
    options=options,
)