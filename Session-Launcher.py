import os
import logging
from pathlib import Path
from argparse import ArgumentParser
import sys

from sectorfile_installer.ui import Ui, select_language
from sectorfile_installer.util import (
    Config, Settings, RuntimeVars, LOG_LEVELS, 
    set_log_level, get_logger, get_app_data_folder,
    get_log_file_path
)

logging.basicConfig()

if __name__ == '__main__':
    parser = ArgumentParser(description="Sectorfile installer")
    parser.add_argument("--config", type=str, help="path of configuration to use", default="vacc\\config.json")
    parser.add_argument("--log-level", choices=list(LOG_LEVELS.keys()), default="INFO")
    parser.add_argument("--settings-file", type=str, default=None)

    args = parser.parse_args()

    set_log_level(args.log_level)

    RuntimeVars.load()
    RuntimeVars.set("executable_path", __file__)

    executable_dir = os.path.dirname(__file__)
    RuntimeVars.set("executable_dir", executable_dir)

    try:
        with open(Path(executable_dir) / "VERSION", "r") as f:
            version = f.readline()
    except Exception:
        version = "0.0.1"
        
    RuntimeVars.set("version", version)

    logger = get_logger(__file__)
    logger.info("Sectorfile Installer version %s", version)
    logger.info("logfile path: %s", get_log_file_path())
    logger.info("working directory: %s", os.getcwd())
    logger.info("executable dir: %s", executable_dir)

    config_path = args.config
    if hasattr(sys, "_MEIPASS") and len(sys._MEIPASS) > 0:
        logger.info("_MEIPASS: %s", sys._MEIPASS)
        config_path = os.path.join(sys._MEIPASS, config_path)

    if not Config.set_path(config_path, check=True):
        logger.error("could not load config '%s'", args.config)
        sys.exit(1)
    Config.load()
    if hasattr(sys, "_MEIPASS") and len(sys._MEIPASS) > 0:
        Config.apply_asset_path(sys._MEIPASS)


    if args.settings_file is None:
        settings_file = get_app_data_folder() / "settings.json"
    else:
        settings_file = Path(args.settings_file)

    settings_file.parent.mkdir(exist_ok=True, parents=True)
    Settings.set_path(settings_file)
    Settings.load()

    select_language(Settings.get("selected_language"))

    Ui().init().mainloop()
