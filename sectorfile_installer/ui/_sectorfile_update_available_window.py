import tkinter as tk

from ._translate import translate
from ._util import center_in_parent, open_folder
from ._install_sectorfile_action import install_sectorfile_action

def sectorfile_update_available_window(root: tk.Tk) -> tk.Tk:
    window = tk.Toplevel(root)
    window.title(translate("update_available"))

    msg_label = tk.Label(window, text=translate("sectorfile_update_available"))
    msg_label.pack(pady=10, padx=20)

    button_frame = tk.Frame(window)
    button_frame.pack(side=tk.BOTTOM, pady=15)

    tk.Button(
        button_frame, 
        text=translate("ok"), 
        command=window.destroy
    ).grid(row=0, column=0, padx=20)

    def button_download():
        install_sectorfile_action()
        window.destroy()

    tk.Button(
        button_frame, 
        text=translate("download"), 
        command=button_download
    ).grid(row=0, column=1, padx=20)

    center_in_parent(root, window)

    window.transient(root)
    window.grab_set()
    root.wait_window(window)
