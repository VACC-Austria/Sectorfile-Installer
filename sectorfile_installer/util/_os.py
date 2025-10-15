import os
from pathlib import Path


def get_app_data_folder() -> Path:
    app_data_folder = Path(os.getenv("LOCALAPPDATA")) / "SectorfileInstaller"
    app_data_folder.mkdir(parents=True, exist_ok=True)
    return app_data_folder
