from sectorfile_installer.util import (
    Config,
    RuntimeVars,
    Settings,
    get_logger,
    version_tuple,
)

logger = get_logger(__file__)


class InstallerManager:
    def check_upgrade_available(self, latest_version) -> bool:
        if latest_version == "":
            return False

        self_version = self.get_self_version()

        if self_version < latest_version:
            logger.info("installer upgrade available")
            return True
        return False

    def get_self_version(self) -> str:
        return version_tuple(RuntimeVars.get("version"))

    def get_update_url(self) -> str:
        config = Config.get()
        language_parameter = (
            "&language=de"
            if Settings.get("selected_language") == "Deutsch"
            else "&language=en"
        )
        return config.installer_update_URL + language_parameter
