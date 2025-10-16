import tkinter as tk
from typing import Self

from sectorfile_installer.managers import (
    EuroscopeManager,
    InstallerManager,
    SectorfileManager,
)
from sectorfile_installer.util import get_online_versions

from ._could_not_find_euroscope_window import could_not_find_euroscope_window
from ._main_window import main_window
from ._sectorfile_update_available_window import sectorfile_update_available_window
from ._update_available_window import update_available_window


class Ui:
    def __init__(self):
        self._root: tk.TK | None = None

    def init(self) -> Self:
        self._root = main_window()

        installer_mgr = InstallerManager()
        es_mgr = EuroscopeManager()
        sct_mgr = SectorfileManager()

        sct_mgr.ensure_sectorfile_folder()
        sct_mgr.ensure_custom_files_folder()

        latest_installer_version, latest_euroscope = get_online_versions()

        if installer_mgr.check_upgrade_available(latest_installer_version):
            update_available_window(
                self._root,
                "installer_upgrade_available",
                installer_mgr.get_update_url(),
            )

        if not es_mgr.check_euroscope_location():
            could_not_find_euroscope_window(self._root)
        else:
            upgrade_available, upgrade_url = es_mgr.check_euroscope_version(
                latest_euroscope
            )
            if upgrade_available:
                update_available_window(
                    self._root, "euroscope_upgrade_available", upgrade_url
                )

        if sct_mgr.check_update_available():
            sectorfile_update_available_window(self._root)

        return self

    def mainloop(self):
        if self._root is None:
            raise ValueError("Ui has not been initialized")
        return self._root.mainloop()
