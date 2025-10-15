import tkinter as tk

from sectorfile_installer.util import Config, get_logger
from sectorfile_installer.managers import SectorfileManager
from ._translate import translate
from ._settings_window import settings_window
from ._error_window import error_window
from ._install_sectorfile_action import install_sectorfile_action
from ._util import center_on_screen, open_folder
from ._choose_profile_window import choose_profile_window

logger = get_logger(__file__)

def main_window() -> tk.Tk:
    config = Config.get()

    # Hauptfenster erstellen
    root = tk.Tk()
    root.withdraw()
    root.title(f"{config.FIR_fullname} Sectorfile Updater")
    #root.geometry("550x300")
    root.iconbitmap(config.icon_path)

    # Logo in der Mitte anzeigen
    logo_img = tk.PhotoImage(file=config.logo_path)
    logo_label = tk.Label(root, image=logo_img)
    logo_label.image = logo_img
    logo_label.pack(pady=50, padx=40)

    sct_mgr = SectorfileManager()

    # # Buttons unten hinzufügen
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.BOTTOM, pady=20)

    def button_setting():
        settings_window(root)
    settings_button = tk.Button(button_frame, text=translate("setting"), command=button_setting)
    settings_button.grid(row=0, column=0, padx=20)

    custom_files_button = tk.Button(
        button_frame, 
        text=translate("custom_files"),
        command=lambda: open_folder(sct_mgr.custom_files_folder)
    )
    custom_files_button.grid(row=0, column=1, padx=20)

    sectorfile_button = tk.Button(
        button_frame, 
        text=translate("import_sectorfile"),
        command=install_sectorfile_action,
    )
    sectorfile_button.grid(row=0, column=2, padx=20)

    def button_start():
        check_result = sct_mgr.check_install_prerequisites()
        if check_result is not True:
            logger.warning("check_install_prerequisites: %s", check_result)
            error_window(root, check_result)
            return
        logger.info("starting install")
        sct_mgr.install()
        choose_profile_window(root)



    start_button = tk.Button(
        button_frame, 
        text=translate("start"), 
        command=button_start
    )
    start_button.grid(row=0, column=3, padx=20)

    center_on_screen(root, root)

    root.update_idletasks()        
    
    root.update()
    root.deiconify()

    return root
