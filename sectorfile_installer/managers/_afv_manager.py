import ctypes
from pathlib import Path
from contextlib import chdir

from sectorfile_installer.util import Settings, get_fileinfo, get_logger

logger = get_logger(__file__)

class AfvManager:
    def check_afv(self) -> tuple[bool, str]:
        afv_path = self._get_afv_path()

        if afv_path is None:
            return False, "afv_not_configured"

        logger.info("checking afv application at %s", str(afv_path))

        if not afv_path.exists() or not afv_path.is_file():
            return False, "could_not_find_afv"

        try:
            file_description = get_fileinfo(afv_path, "FileDescription")
        except Exception as e:
            logger.warning("error retrieving file info - %s", str(e))
            return False, "error_fetching_file_info"

        logger.info("found File Description: %s", file_description)

        if (
            file_description == "Audio For VATSIM Client"
            or file_description == "VectorAudio"
        ):
            return True, "ok"
        
        return False, "error"

    def start(self, workdir: str | Path | None = None):
        if workdir is None:
            workdir = Path.cwd()
        elif isinstance(workdir, str):
            workdir = Path(workdir)
        elif isinstance(workdir, Path):
            pass
        else:
            raise ValueError("expected workdir to be a string or a Path")
        
        is_ok, msg = self.check_afv()

        if not is_ok:
            return is_ok, msg

        logger.info("starting afv application (as admin): %s", self._get_afv_path())
        with chdir(workdir):
            ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas", 
                str(self._get_afv_path()), 
                None, 
                None, 
                3
            )

        return True, "ok"


    def _get_afv_path(self) -> Path | None:
        path = Settings.get("afv_path")

        if not path:
            return None
        return Path(path)
        
        
            