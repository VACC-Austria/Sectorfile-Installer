import json
from typing import Any, ClassVar, overload
from pathlib import Path

from pydantic import BaseModel
from ._logging import get_logger

logger = get_logger(__file__)

class ValueStore(BaseModel):
    _path: ClassVar[Path | None] = None
    _instance: ClassVar[ValueStore | None] = None
    _editable: ClassVar[bool] = False

    @classmethod
    def set_path(cls, path: Path | str, check: bool=False) -> bool:
        if isinstance(path, str):
            path = Path(path)

        if check and (not path.exists() or not path.is_file()):
            return False

        cls._path = path
        return True

    @classmethod
    def load(cls):
        if cls._path is None:
            cls._instance = cls()
            return
        try:
            logger.info(f"loading {cls.__name__} from {str(cls._path)}")
            with cls._path.open("r") as f:
                cls._instance = cls.model_validate(json.load(f))
        except Exception as e:
            logger.info(f"failed - falling back to default")
            cls._instance = cls()
        
    @classmethod
    def save(cls):
        if cls._path is None:
            raise RuntimeError(f"{cls.__name__} is in-memory")
        if cls._editable is not True:
            raise ValueError(f"{cls.__name__} is not editable")
        config = cls.get()
        try:
            logger.info(f"saving {cls.__name__} to {str(cls._path)}")
            cls._path.parent.mkdir(exist_ok=True)

            with cls._path.open("w") as f:
                f.write(config.model_dump_json(indent=4) + "\n")
        except Exception as e:
            logger.warning("save failed")
            pass

    @overload
    @classmethod
    def get(cls) -> ValueStore:
        ...
        
    @overload
    @classmethod
    def get(cls, key: str) -> Any:
        ...

    @classmethod
    def get(cls, key: str | None = None) -> ValueStore | Any:
        if cls._instance is None:
            raise ValueError(f"{cls.__name__} has not been loaded")
        
        if key is None:
            return cls._instance
    
        return getattr(cls._instance, key)
    
    @classmethod
    def set(cls, key: str, value: Any, force: bool=False):
        if cls._editable is not True and force is False:
            raise ValueError(f"{__class__.__name__} is not editable")
        config = cls.get()
        setattr(config, key, value)
