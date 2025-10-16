import webbrowser

import tkinter as tk

from sectorfile_installer.util import Config
from ._translate import translate

def about_window(root: tk.Tk) -> tk.Tk:
    window = tk.Toplevel(root)
    window.title(translate("about"))
    window.iconbitmap(Config.get("icon_path"))
    tk.Label(
        window, 
        text=translate("about_message")
    ).grid(row=0, column=0, pady=10, padx=20)

    link = tk.Label(
        window,
        text="https://github.com/VACC-Austria/Sectorfile-Installer",
        fg="blue",
        cursor="hand2",
    )
    link.grid(row=1, column=0, pady=0, ipady=5, padx=20, sticky="new")
    link.bind(
        "<Button-1>", lambda e: webbrowser.open_new_tab("https://github.com/VACC-Austria/Sectorfile-Installer")
    )

    button_frame = tk.Frame(window)
    button_frame.grid(row=2, column=0, pady=10, padx=20)

    tk.Button(
        button_frame, 
        text=translate("ok"), 
        command=window.destroy
    ).grid(row=0, column=0, padx=20)
    
    window.transient(root)
    window.grab_set()
    root.wait_window(window)

    return window
