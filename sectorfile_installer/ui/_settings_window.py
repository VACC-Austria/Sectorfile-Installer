import tkinter as tk
from tkinter import filedialog

from sectorfile_installer.util import Config, Settings
from sectorfile_installer.managers import EuroscopeManager
from ._translate import translate, get_languages
from ._restart_window import restart_window

def settings_window(root: tk.Tk) -> tk.Tk:
    config = Config.get()
    settings = Settings.get()

    window = tk.Toplevel(root)
    window.title(translate("setting"))
    window.iconbitmap(config.icon_path)

    tk.Label(window, text=translate("language")).grid(row=0, column=0, padx=10, pady=10)
    selected_language_entry = tk.StringVar(window)
    selected_language_entry.set(settings.selected_language)
    selected_language_menu = tk.OptionMenu(
        window, 
        selected_language_entry, 
        *get_languages()
    )
    selected_language_menu.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(window, text=translate("name")).grid(row=1, column=0, padx=10, pady=10)
    name_entry = tk.Entry(window)
    name_entry.grid(row=1, column=1, padx=10, pady=10)
    name_entry.insert(0, settings.name)

    tk.Label(window, text=translate("vatsim_id")).grid(row=2, column=0, padx=10, pady=10)
    vatsim_id_entry = tk.Entry(window)
    vatsim_id_entry.grid(row=2, column=1, padx=10, pady=10)
    vatsim_id_entry.insert(0, settings.vatsim_id)

    tk.Label(window, text=translate("vatsim_password")).grid(row=3, column=0, padx=10, pady=10)
    vatsim_password_entry = tk.Entry(window, show="*")
    vatsim_password_entry.grid(row=3, column=1, padx=10, pady=10)
    vatsim_password_entry.insert(0, settings.vatsim_password)

    tk.Label(window, text=translate("rating")).grid(row=4, column=0, padx=10, pady=10)
    rating_entry = tk.StringVar(window)
    rating_entry.set(settings.get("rating"))
    rating_options = ["OBS", "S1", "S2", "S3", "C1", "C3", "SUP"]
    rating_menu = tk.OptionMenu(window, rating_entry, *rating_options)
    rating_menu.grid(row=4, column=1, padx=10, pady=10)

    tk.Label(window, text=translate("hoppie_code")).grid(row=5, column=0, padx=10, pady=10)
    hoppie_code_entry = tk.Entry(window, show="*")
    hoppie_code_entry.grid(row=5, column=1, padx=10, pady=10)
    hoppie_code_entry.insert(0, settings.hoppie_code)

    tk.Label(window, text=translate("euroscope_path")).grid(row=6, column=0, padx=10, pady=10)
    euroscope_path_entry = tk.Entry(window, width=50)
    euroscope_path_entry.grid(row=6, column=1, padx=10, pady=10)
    euroscope_path_entry.insert(0, settings.euroscope_path)

    def browse_euroscope_path():
        file_path = filedialog.askopenfilename(
            title="select Euroscope.exe",
            filetypes=[("Executable Files", "*.exe")]
        )

        if file_path:
            euroscope_path_entry.delete(0, tk.END)
            euroscope_path_entry.insert(0, file_path)
        window.focus_set()

    tk.Button(
        window, 
        text=translate("browse"), 
        command=browse_euroscope_path
    ).grid(row=6, column=2, padx=10, pady=10)

    tk.Label(window, text=translate("afv_path")).grid(row=7, column=0, padx=10, pady=10)
    afv_path_entry = tk.Entry(window)
    afv_path_entry.grid(row=7, column=1, padx=10, pady=10)
    afv_path_entry.insert(0, settings.afv_path)

    def browse_afv_path():
        file_path = tk.filedialog.askopenfilename(
            title="select AFV.exe",
            filetypes=[("Executable Files", "*.exe")]
        )
        if file_path:
            afv_path_entry.delete(0, tk.END)
            afv_path_entry.insert(0, file_path)
        window.focus_set()

    tk.Button(
        window, 
        text=translate("browse"), 
        command=browse_afv_path
    ).grid(row=7, column=2, padx=10, pady=10)

    def save_settings():
        old_lang = Settings.get("selected_language")
        new_lang = selected_language_entry.get()

        Settings.set("name", name_entry.get())
        Settings.set("vatsim_id", vatsim_id_entry.get())
        Settings.set("vatsim_password", vatsim_password_entry.get())
        Settings.set("rating", rating_entry.get())
        Settings.set("hoppie_code", hoppie_code_entry.get())
        Settings.set("afv_path", afv_path_entry.get())
        Settings.set("selected_language", new_lang)
        Settings.save()

        if new_lang != old_lang:
            restart_window(root)
        else:
            window.destroy()

    tk.Button(
        window, 
        text=translate("save"), 
        command=save_settings
    ).grid(row=9, column=1, padx=10, pady=10)
    
    window.transient(root)
    window.grab_set()
    root.wait_window(window)
