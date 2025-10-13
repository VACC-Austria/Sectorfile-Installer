import tkinter as tk

from ._translate import translate
from ._util import center_in_parent

def error_window(root: tk.Tk, message: str, title: str = "error"):    
    window = tk.Toplevel(root)
    window.title(translate(title))

    msg_label = tk.Label(window, text=translate(message))
    msg_label.pack(pady=10, padx=20)

    button_frame = tk.Frame(window)
    button_frame.pack(side=tk.BOTTOM, pady=15)
    tk.Button(
        button_frame, 
        text=translate("ok"), 
        command=window.destroy
    ).grid(row=0, column=0, padx=20)

    center_in_parent(root, window)
    
    window.transient(root)
    window.grab_set()
    root.wait_window(window)
