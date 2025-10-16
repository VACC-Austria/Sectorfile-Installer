import subprocess
from pathlib import Path

from sectorfile_installer.util import (
    Settings,
    get_fileinfo,
    get_logger,
    version_tuple,
)

logger = get_logger(__file__)


class EuroscopeManager:
    def check_euroscope_location(self, location: str | None = None) -> bool:
        if location is None:
            location = self.es_path
        logger.info("checking for euroscope at %s", str(location))
        if get_fileinfo(location, "ProductName") == "EuroScope Application":
            return True

        return False

    def check_euroscope_version(self, latest) -> tuple[bool, str | None]:
        available_version, upgrade_url = latest
        if available_version == "":
            return False, None

        installed_version = self.get_installed_version()

        if installed_version < available_version:
            logger.info("euroscope upgrade available")
            return True, upgrade_url

        return False, None

    def get_installed_version(self) -> tuple[int]:
        version = get_fileinfo(self.es_path, "ProductVersion")
        if version is None:
            raise RuntimeError("could not fetch Euroscope version")
        logger.info("found euroscope version %s", version)
        return version_tuple(version)

    def start(self, profile: str | Path | None = None) -> tuple[bool, str | None]:
        if not self.check_euroscope_location():
            return False, "euroscope_not_found"

        command = [str(self.es_path)]

        if profile is not None:
            command.append(str(profile))

        logger.info("starting Euroscope: '%s'", " ".join(command))
        subprocess.Popen(
            command,
            cwd=str(self.es_path.parent),
            start_new_session=True,
        )

        return True, "ok"

    @property
    def es_path(self) -> Path | None:
        es_path = Settings.get("euroscope_path")
        if not es_path:
            return None
        return Path(es_path)
