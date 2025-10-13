import tkinter as tk

from ._translate import translate

def restart_window(root: tk.Tk) -> tk.Tk:
    window = tk.Toplevel(root)
    window.title("Restart required")
    window.geometry("300x100")
    tk.Label(
        window, 
        text=translate("language_changed_after_reload")
    ).pack(pady=10)

    button_frame = tk.Frame(window)
    button_frame.pack(side=tk.BOTTOM, pady=15)

    tk.Button(
        button_frame, 
        text=translate("quit"), 
        command=root.destroy
    ).grid(row=0, column=0, padx=20)
    
    window.transient(root)
    window.grab_set()
    root.wait_window(window)

    return window

