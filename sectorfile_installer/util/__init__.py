import logging
import os
import shutil
from pathlib import Path

import requests
import win32api

from ._config import Config
from ._logging import LOG_LEVELS, get_log_file_path, get_logger, set_log_level
from ._os import get_app_data_folder
from ._runtime_vars import RuntimeVars
from ._settings import Settings

logger = get_logger(__file__)


def copy_ownfolder(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isdir(src_path):
            # Wenn der Zielordner existiert, rekursiv in ihn kopieren
            if not os.path.exists(dst_path):
                os.makedirs(dst_path)
            shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
            # copy_folder(src_path, dst_path)  # Rekursiver Aufruf
        else:
            # Dateien kopieren
            shutil.copy2(src_path, dst_path)


def is_dir_empty(path: Path | str) -> bool:
    if isinstance(path, str):
        path = Path(str)

    if not path.is_dir():
        raise ValueError("path is not a directory")

    return not bool(next(path.iterdir(), None))


type Version = tuple[int]


def version_tuple(version) -> Version:
    return tuple(map(int, (version.split("."))))


def get_fileinfo(path: Path | str, field) -> str | None:
    path = str(path)

    try:
        language, codepage = win32api.GetFileVersionInfo(
            path, "\\VarFileInfo\\Translation"
        )[0]
        stringFileInfo = "\\StringFileInfo\\%04X%04X\\%s" % (language, codepage, field)
        return win32api.GetFileVersionInfo(path, stringFileInfo)
    except Exception:
        return None


def get_online_versions() -> tuple[Version, tuple[Version, str]]:
    config = Config.get()

    try:
        response = requests.get(config.URL + "versions.json")
        data = response.json()

        latest_installer_version = version_tuple(data["installer"])
        latest_euroscope_version = version_tuple(data["euroscope"])
        euroscope_upgrade_url = data["euroscope_url"]

        logger.info("found available installer version %s", latest_installer_version)
        logger.info("found available euroscope version %s", latest_euroscope_version)

        return (
            latest_installer_version,
            (latest_euroscope_version, euroscope_upgrade_url),
        )
    except Exception:
        return ("", ("", ""))
