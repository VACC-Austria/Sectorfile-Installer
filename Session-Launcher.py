import logging
import os
import sys
from argparse import ArgumentParser
from pathlib import Path

from sectorfile_installer.ui import Ui, select_language
from sectorfile_installer.util import (
    LOG_LEVELS,
    Config,
    RuntimeVars,
    Settings,
    get_app_data_folder,
    get_log_file_path,
    get_logger,
    set_log_level,
)

logging.basicConfig()

if __name__ == "__main__":
    parser = ArgumentParser(description="Sectorfile installer")
    parser.add_argument(
        "--config",
        type=str,
        help="path of configuration to use",
        default="vacc-austria\\config.json",
    )
    parser.add_argument("--log-level", choices=list(LOG_LEVELS.keys()), default="INFO")
    parser.add_argument("--settings-file", type=str, default=None)

    args = parser.parse_args()

    set_log_level(args.log_level)

    RuntimeVars.load()
    RuntimeVars.set("executable_path", __file__)

    executable_dir = os.path.dirname(__file__)
    RuntimeVars.set("executable_dir", executable_dir)

    logger = get_logger(__file__)

    config_path = args.config
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        logger.info("_MEIPASS: %s", sys._MEIPASS)
        config_path = Path(sys._MEIPASS) / config_path
        version_file_path = Path(sys._MEIPASS) / "VERSION"
    else:
        version_file_path = Path(executable_dir) / "VERSION"

    try:
        with open(version_file_path, "r") as f:
            version = f.readline()
    except Exception as e:
        logger.warning("could not load VERSION file - %s", str(e))
        version = "0.0.1"

    RuntimeVars.set("version", version)

    logger.info("Sectorfile Installer version %s", version)
    logger.info("logfile path: %s", get_log_file_path())
    logger.info("working directory: %s", os.getcwd())
    logger.info("executable dir: %s", executable_dir)

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
