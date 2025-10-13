import requests

from sectorfile_installer.util import Config, RuntimeVars, version_tuple, Settings, get_logger

logger = get_logger(__file__)

class InstallerManager:
    def check_upgrade_available(self):
        config = Config.get()

        self_version = self.get_self_version()

        try:
            ####################################
            # get the online Installer version #
            ####################################
            response = requests.get(config.URL + "installerversion.txt")
            data = response.text.splitlines()

            online_installer_version = data[0].strip()

            logger.info("found available installer version %s", online_installer_version)

            if version_tuple(self_version) < version_tuple(online_installer_version):
                logger.info("installer upgrade available")
                return True

        except Exception as e:
            return False

    def get_self_version(self) -> str:
        return RuntimeVars.get("version")
    
    def get_update_url(self) -> str:
        config = Config.get()
        language_parameter = (
            "&language=de" 
            if Settings.get("selected_language") == "Deutsch" 
            else "&language=en"
        )
        return config.installer_update_URL + language_parameter
    