import time
import tkinter as tk
from tkinter import messagebox

from sectorfile_installer.util import get_logger, get_app_data_folder
from sectorfile_installer.managers import SectorfileManager, EuroscopeManager, AfvManager
from ._translate import translate
from ._util import center_in_parent

logger = get_logger(__file__)

def choose_profile_window(root: tk.Tk):
    window = tk.Toplevel(root)
    window.title(translate("choose_a_profile"))

    label = tk.Label(window, text=translate("choose_a_profile"))
    label.grid(row=0, column=0, padx=10, pady=10)

    listbox = tk.Listbox(window)
    listbox.grid(row=1, column=0, padx=10, pady=10)

    profiles = SectorfileManager().get_available_profiles()

    if len(profiles) == 0:
        messagebox.showerror(translate("error"), translate("no_profiles_found"))
        window.destroy()
        return

    for profile in profiles.keys():
        listbox.insert(tk.END, profile)

    button_frame = tk.Frame(window)
    button_frame.grid(row=2, column=0)

    def button_start_action():
        selected = listbox.get(listbox.curselection())
        if selected is not None:
            profile_path = profiles[selected]
            es_mgr = EuroscopeManager()
            success, msg = es_mgr.start(profile=profile_path)
            if success:
                try:
                    AfvManager().start(workdir=get_app_data_folder())
                except Exception as e:
                    logger.warning("exception while starting afv - %s", str(e))
                    pass
                logger.info("closing application ...")
                root.destroy()
                return
            else:
                messagebox.showerror(translate("error"), translate(msg))
                window.destroy()
                return
        messagebox.showerror(translate("error"), translate("please_select_a_profile"))

    tk.Button(
        button_frame, 
        text=translate("start"), 
        command=button_start_action
    ).grid(row=0, column=0, padx=10, pady=10)

    center_in_parent(root, window)
    
    window.transient(root)
    window.grab_set()
    root.wait_window(window)


