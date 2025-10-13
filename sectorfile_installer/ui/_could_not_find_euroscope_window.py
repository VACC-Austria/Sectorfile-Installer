import webbrowser

import tkinter as tk
from tkinter import filedialog

from sectorfile_installer.util import Settings, Config
from sectorfile_installer.managers import EuroscopeManager
from ._translate import translate
from ._error_window import error_window
from ._util import center_in_parent

def could_not_find_euroscope_window(root: tk.Tk) -> tk.Tk:
    settings = Settings.get()

    window = tk.Toplevel(root)
    window.title(translate("euroscope_not_found"))

    frame = tk.Frame(window)
    msg_label = tk.Label(
        frame, 
        text=translate("could_not_find_euroscope"),
        justify="left"
    )
    msg_label.grid(row=0, pady=10)

    euroscope_path_entry = tk.Entry(frame, width=50)
    euroscope_path_entry.grid(row=1, column=0, padx=4)
    euroscope_path_entry.insert(0, settings.euroscope_path)

    def browse_euroscope_path():
        file_path = filedialog.askopenfilename(
            title="select Euroscope.exe",
            filetypes=[("Executable Files", "*.exe")]
        )

        if file_path:
            if EuroscopeManager().check_euroscope_location(file_path):
                Settings.set("euroscope_path", file_path)
                Settings.save()
                window.destroy()
            else:
                window.focus_set()
                error_window(window, "file_is_not_euroscope")

    tk.Button(
        frame, 
        text=translate("browse"), 
        command=browse_euroscope_path
    ).grid(row=1, column=1, padx=2)

    def button_download():
        webbrowser.open(Config.get("euroscope_URL"))
        window.destroy()

    tk.Button(
        frame, 
        text=translate("download_euroscope"),
        command=button_download
    ).grid(row=2, column=0, padx=20, pady=10)

    frame.pack(padx=10, pady=10)

    center_in_parent(root, window)
    
    window.transient(root)
    window.grab_set()
    root.wait_window(window)
