from glob import glob
import os
from pathlib import Path
import re
import shutil
from typing import Literal
from tempfile import NamedTemporaryFile, TemporaryDirectory

from bs4 import BeautifulSoup
import requests

from sectorfile_installer.util import Config, Settings, get_logger, is_dir_empty, get_app_data_folder

logger = get_logger(__file__)

_CUSTOMFILE_DIRS = [
    "Alias",
    "ASR",
    "Plugins",
    "Settings",
    "Sounds",
]

_RATING_MAP = dict(
    OBS=0,
    S1=1,
    S2=2,
    S3=3,
    C1=4,
    C3=6,
    I1=7,
    I3=9,
    SUP=10,
)

class SectorfileManager:
    @property
    def custom_files_folder(self) -> Path:
        return self.app_data_dir / "Customfiles"
    
    @property
    def sectorfile_folder(self) -> Path:
        return self.app_data_dir / "Sectorfile"
    
    @property
    def sectorfile_backup_folder(self) -> Path:
        return self.app_data_dir / "Sectorfile_Backup"
    
    @property
    def hoppie_config_file(self) -> Path:
        return self.sectorfile_folder / "LOVV" / "Plugins" / "Topsky" / "TopSkyCPDLChoppieCode.txt"

    @property
    def app_data_dir(self) -> Path:
        fir = Config.get("FIR")
        return get_app_data_folder() / fir

    @property
    def airac_lookup_url(self):
        return "https://files.aero-nav.com/" + Config.get("FIR")

    @property
    def _version_0(self) -> str:
        return "000000-0000"
    
    def ensure_custom_files_folder(self):
        custom_files_path = self.custom_files_folder
        
        custom_files_path.mkdir(exist_ok=True, parents=True)

        for dir_ in _CUSTOMFILE_DIRS:
            (custom_files_path / dir_).mkdir(exist_ok=True, parents=True)

    def ensure_sectorfile_folder(self):
        self.sectorfile_folder.mkdir(exist_ok=True, parents=True)

    def check_update_available(self):
        installed_version, _ = self.get_installed_airac_version()
        result = installed_version < self.get_available_airac_version()
        logger.info("airac update available" if result else "no airac update available")
        return result
    
    def get_available_profiles(self) -> dict[str, Path]:
        profiles = {}

        for path in self.sectorfile_folder.iterdir():
            if path.is_file() and path.name.endswith(".prf"):
                profiles[".".join(path.name.split(".")[:-1])] = path
        return profiles

    def get_installed_airac_version(self, dir_: str | Path | None=None) -> tuple[str, str | None]:
        # Alle Dateien im Ordner durchgehen
        highest_version = self._version_0
        ese_file_path = None

        if dir_ is None:
            dir_ = self.sectorfile_folder
        else:
            if not isinstance(dir_, Path):
                dir_ = Path(dir_)

        logger.info("checking Sectorfile version in directory %s", str(dir_))

        for path in dir_.iterdir():
            m = re.match(r".+-(\d{6}-\d{4}).ese", path.name)
            if m:
                version = m.group(1)
                if version > highest_version:
                    highest_version = version
                    ese_file_path = path
        logger.info("found sectorfile version %s", highest_version)
        return highest_version, ese_file_path
    
    def get_available_airac_version(self) -> str:
        try:
            url = self.airac_lookup_url
            logger.info("retrieving available airac version from %s", url)
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table", class_="table table-striped table-hover table-bordered")
        except Exception as e:
            logger.warning("could not retrieve airac info: %s", str(e))
            return self._version_0
        
        for row in table.find_all("tr")[1:]:  # Header überspringen
            cols = [c.get_text(strip=True) for c in row.find_all("td")]
            if not cols:
                continue
            if Config.get("Packagename") in cols[1]:
                airac = cols[2]
                version = cols[3]
                version = version.zfill(4)
                online_airac = airac.translate(str.maketrans("", "", " /")) + "-" + version
                logger.info(f"sectorfile available: %s", online_airac)
                return online_airac
        return self._version_0
    
    def start_import(self) -> TemporaryDirectory:
        temp_dir = TemporaryDirectory(prefix="sct_installer_")
        logger.debug("created temporary directors %s for import", temp_dir.name)
        return temp_dir
    
    def finish_import(self, temp_dir: TemporaryDirectory) -> tuple[bool, str]:
        is_ok, msg = self._check_import(temp_dir)
        if not is_ok:
            return False, msg
        
        if self.sectorfile_folder.exists() and not is_dir_empty(self.sectorfile_folder):
            logger.info("making backup of sectorfile folder")
            self._move_sectorfile_to_backup()

        if self.sectorfile_folder.exists():
            shutil.rmtree(self.sectorfile_folder)

        logger.info("moving new Sectorfile data into %s", str(self.sectorfile_folder))
        shutil.move(temp_dir.name, self.sectorfile_folder)

        self._copy_special_files_from_backup()

        return True, msg

    def clean_up_import(self, temp_dir: TemporaryDirectory):
        path = Path(temp_dir.name)
        if path.exists():
            logger.debug("removing temporary import directory %s", str(path))
            shutil.rmtree(path)
    
    def install(self):
        self._install_hoppie_code()
        self._install_profile_files()
        self._install_custom_files()

    def check_install_prerequisites(self) -> str | Literal[True]:
        settings = Settings.get()

        if not settings.name:
            return "name_not_set"
        
        if not settings.vatsim_id:
            return "vatsim_id_not_set"

        if not settings.rating:
            return "rating_not_set"

        return True


    def _install_hoppie_code(self):
        self.hoppie_config_file.parent.mkdir(parents=True, exist_ok=True)

        with self.hoppie_config_file.open("w") as f:
            f.write(Settings.get("hoppie_code"))

    def _install_profile_files(self):
        profile_files = (
            glob(os.path.join(str(self.sectorfile_folder), "*.prf"))
            + glob(os.path.join(str(self.sectorfile_folder), "**", "*.prf"))
        )

        for path in profile_files:
            self._update_profile_file(path)

    def _install_custom_files(self):
        shutil.copytree(
            self.custom_files_folder, 
            self.sectorfile_folder,
            dirs_exist_ok=True
        )

    def _update_profile_file(self, path: Path):
        settings = Settings.get()
        logger.info("modifying profile file: %s", path)

        rating_code = _RATING_MAP.get(settings.rating, 1)

        with NamedTemporaryFile(mode="w", delete=False, delete_on_close=False) as temp_f:
            with open(path, "r") as f:
                for line in f:
                    if not (line.startswith("LastSession	realname") or
                            line.startswith("LastSession	certificate") or
                            line.startswith("LastSession	password") or
                            line.startswith("LastSession	rating")):
                        temp_f.write(line)
            temp_f.write(f"\nLastSession	realname	{settings.name}")
            temp_f.write(f"\nLastSession	certificate	{settings.vatsim_id}")
            temp_f.write(f"\nLastSession	password	{settings.vatsim_password}")
            temp_f.write(f"\nLastSession	rating	{rating_code}")
            temp_filename = temp_f.file.name

        os.unlink(path)
        shutil.move(temp_filename, str(path))
    
    def _copy_special_files_from_backup(self):
        if (
            not self.sectorfile_folder.exists() 
            or not self.sectorfile_backup_folder.exists()
            or is_dir_empty(self.sectorfile_backup_folder)
        ):
            return
        
        for path in Config.get("special_files"):
            src_abs_path = self.sectorfile_backup_folder / path

            dst_abs_path = self.sectorfile_folder / path

            if src_abs_path.is_file():
                logger.info("copying special file %s to %s", str(src_abs_path), str(dst_abs_path))
                dst_abs_path.parent.mkdir(exist_ok=True, parents=True)
                shutil.copy2(src_abs_path, dst_abs_path)

    def _move_sectorfile_to_backup(self):
        if self.sectorfile_backup_folder.exists():
            logger.info("removing previous sectorfile backup folder %s", str(
                self.sectorfile_backup_folder)
            )
            shutil.rmtree(self.sectorfile_backup_folder)

        shutil.move(self.sectorfile_folder, self.sectorfile_backup_folder)

    def _check_import(self, temp_dir: TemporaryDirectory) -> tuple[bool, str]:
        logger.info("checking import")
        version, _ = self.get_installed_airac_version(temp_dir.name)

        if version <= self._version_0:
            return False, "could_not_find_valid_sectorfile_in_directory"
        return True, "import_ok"