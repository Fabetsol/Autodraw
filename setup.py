from cx_Freeze import setup, Executable
base = None

executables = [Executable("Autodraw.py", base=base)]

packages = ["time", "requests", "PIL", "pynput", "pyperclip", "pickle", "tkinter", "math"]
options = {
    'build_exe': {    
        'packages':packages,
    },
}

setup(
    name = "Autodraw",
    options = options,
    version = "1.5",
    description = """Little program that draws for you.""",
    executables = executables
)