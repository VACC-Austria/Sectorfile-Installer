import logging
import os

from ._os import get_app_data_folder

LOG_LEVELS = dict(
    DEBUG=logging.DEBUG,
    INFO=logging.INFO,
    WARNING=logging.WARNING,
    ERROR=logging.ERROR,
)

_log_level = logging.INFO
_logger = logging.getLogger("SessionLauncher")
_logger.setLevel(_log_level)
_logfile_path = get_app_data_folder() / "session-launcher.log"
_fh = logging.FileHandler(_logfile_path)
_fh.setLevel(_log_level)
_logger.addHandler(_fh)
_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
_fh.setFormatter(_formatter)

def set_log_level(level):
    global _log_level, _logger
    _log_level = LOG_LEVELS.get(level, logging.INFO)
    _logger.setLevel(level)
    _fh.setLevel(level)

def get_logger(name) -> logging.Logger:
    global _logger
    return _logger

def get_log_file_path() -> str:
    return _logfile_path
