import os
from pathlib import Path

def get_app_data_folder() -> Path:
    return Path(os.getenv("LOCALAPPDATA")) / "SectorfileInstaller"