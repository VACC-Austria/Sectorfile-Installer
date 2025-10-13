import subprocess
from pathlib import Path

import tkinter as tk

def center_on_screen(root: tk.Tk, window: tk.Tk):
    root.eval(f"tk::PlaceWindow {str(window)} center")

def center_in_parent(parent: tk.Tk, window: tk.Tk):
    x = parent.winfo_x() + (parent.winfo_width() - window.winfo_width())//2
    y = parent.winfo_y() + (parent.winfo_height() - window.winfo_height())//2

    window.geometry(f"+{x}+{y}")

def open_folder(path: Path | str):
    subprocess.run(['explorer', str(path)])
