import os
from pathlib import Path
from typing import ClassVar

from pydantic import Field
from ._value_store import ValueStore
from ._runtime_vars import RuntimeVars

class Config(ValueStore):
    URL: str
    FIR: str
    Packagename: str
    FIR_fullname: str
    logo_path: str
    euroscope_URL: str
    installer_update_URL: str
    euroscope_version_URL: str
    special_files: list[str] = Field(default_factory=list)
    
    icon_path: str = "icon.ico"
    Testing: bool = False

    def abs_path(self, key: str) -> str:
        return os.path.join(
            RuntimeVars.get("executable_dir"),
            getattr(self, key)
        )
    
    @classmethod
    def apply_asset_path(cls, asset_path: str):
        config = cls.get()
        cls.set("logo_path", os.path.join(asset_path, config.logo_path), force=True)
        cls.set("icon_path", os.path.join(asset_path, config.icon_path), force=True)
