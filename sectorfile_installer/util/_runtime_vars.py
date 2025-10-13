from typing import ClassVar, Literal

from ._value_store import ValueStore

class RuntimeVars(ValueStore):
    version: str | None = None
    executable_path: str | None = None
    executable_dir: str | None = None
    
    _editable: ClassVar[bool] = True
    