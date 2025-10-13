from pathlib import Path
import re
import subprocess
import win32api
import requests

from sectorfile_installer.util import Settings, Config, version_tuple, get_logger, get_fileinfo

logger = get_logger(__file__)

class EuroscopeManager:
    def check_euroscope_location(self, location: str | None = None) -> bool:
        if location is None:
            location = self._get_es_path()
        logger.info("checking for euroscope at %s", str(location))
        if get_fileinfo(location, "ProductName") == "EuroScope Application":
            return True

        return False
    
    def check_euroscope_version(self) -> tuple[bool, str | None]:
        installed_version = self.get_installed_version()

        result = self.get_available_version()

        if result is None:
            return False, None
        
        available_version, upgrade_url = result

        if installed_version < available_version:
            logger.info("euroscope upgrade available")
            return True, upgrade_url

        return False, None
    
    def get_available_version(self) -> tuple[tuple[int], str] | None:
        url = Config.get("euroscope_version_URL")
        logger.info("fetching available euroscope version from %s", url)

        try:
            r = requests.get(url)
            r.raise_for_status()
        except Exception as e:
            return None
        
        if r.status_code != 200:
            return None
        
        try:
            first_line = r.text.split("\r\n")[0]
            fields = first_line.split("\t")
            if fields[0] != "public":
                return None
            version = fields[1]
            upgrade_url = fields[3]
        except Exception as e:
            return None
        
        if not (
            upgrade_url.startswith("https://euroscope.hu/")
            or upgrade_url.startswith("https://www.euroscope.hu/")
        ):
            raise RuntimeError("unexpected upgrade url: '%s'" % upgrade_url)
        
        m = re.match(r"\d+\.\d+\.\d+\.\d+", version)

        if not m:
            return None
        
        logger.info("found available euroscope version %s", version)
        logger.info("upgrade url: %s", upgrade_url)
        
        return version_tuple(version), upgrade_url

    def get_installed_version(self) -> tuple[int]:
        version = get_fileinfo(self._get_es_path(), "ProductVersion") 
        if version is None:
            raise RuntimeError("could not fetch Euroscope version")
        logger.info("found euroscope version %s", version)
        return version_tuple(version)
    
    def start(self, profile: str | Path | None = None) -> tuple[bool, str | None]:
        if not self.check_euroscope_location():
            return False, "euroscope_not_found"

        command = [str(self._get_es_path())]

        if profile is not None:
            command.append(str(profile))
        
        logger.info("starting Euroscope: '%s'", " ".join(command))
        subprocess.Popen(
            command, 
            cwd=str(self._get_es_path().parent),
            start_new_session=True,
        )

        return True, "ok"

    def _get_es_path(self) -> Path | None:
        es_path = Settings.get("euroscope_path")
        if not es_path:
            return None
        return Path(es_path)
    
        