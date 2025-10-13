import os
import shutil
import logging
from pathlib import Path

import requests
import win32api

from ._logging import LOG_LEVELS, get_logger, set_log_level, get_log_file_path
from ._settings import Settings
from ._config import Config
from ._runtime_vars import RuntimeVars
from ._os import get_app_data_folder

def check_internet(url="https://www.google.com", timeout=3):
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False

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

def version_tuple(version) -> tuple[int]:
    return tuple(map(int, (version.split("."))))


def get_fileinfo(path: Path | str, field) -> str | None:
    path = str(path)

    try:
        language, codepage = win32api.GetFileVersionInfo(
            path,
            '\\VarFileInfo\\Translation'
        )[0]
        stringFileInfo = u'\\StringFileInfo\\%04X%04X\\%s' % (
            language, codepage, field
        )
        return win32api.GetFileVersionInfo(path, stringFileInfo)
    except:
        return None

