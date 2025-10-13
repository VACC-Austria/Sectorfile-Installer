import os
from pathlib import Path
from typing import ClassVar

from ._value_store import ValueStore

class Settings(ValueStore):
    name: str = ""
    vatsim_id: str = ""
    vatsim_password: str = ""
    rating: str = "S1"
    hoppie_code: str = ""
    afv_path: str = ""
    selected_language: str = "English"
    euroscope_path: str = r"C:\Program Files (x86)\EuroScope2\EuroScope.exe"

    _path: ClassVar[Path] = Path("settings.json")
    _editable: ClassVar[bool] = True

    @property
    def euroscope_dir(self) -> str:
        return os.path.dirname(self.euroscope_path)
