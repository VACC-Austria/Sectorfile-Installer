import webbrowser

from tkinter import messagebox

from sectorfile_installer.managers import SectorfileManager
from sectorfile_installer.util import get_logger
from ._util import open_folder
from ._translate import translate

logger = get_logger(__file__)

def install_sectorfile_action():
        messagebox.showinfo(translate("hint"), translate("sectorfile_version"))
        sct_mgr = SectorfileManager()
        webbrowser.open(sct_mgr.airac_lookup_url)

        import_folder = sct_mgr.start_import()
        open_folder(import_folder.name)

        user_msg = "press_ok_to_continue_import_or_cancel_to_abort"

        try:
            while True:
                result = messagebox.askokcancel(
                    translate("import_sectorfile"),
                    translate(user_msg),
                )

                if result:
                    import_ok, user_msg = sct_mgr.finish_import(import_folder)
                    if import_ok:
                        break
                else:
                    logger.warning("aborting sectorfile import due to user cancelling")
                    break
        finally:
            sct_mgr.clean_up_import(import_folder)
