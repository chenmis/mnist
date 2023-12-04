import logging
import traceback

class Logger:
    def __init__(self, name: str, level: int = logging.INFO):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    def _log(self, level, message):
        if self._logger.isEnabledFor(level):
            self._logger.log(level, message)

    def debug(self, message: str):
        self._log(logging.DEBUG, message)

    def info(self, message: str):
        self._log(logging.INFO, message)

    def warning(self, message: str):
        self._log(logging.WARNING, message)

    def error(self, message: str):
        self._log(logging.ERROR, message)

    def exception(self, message: str):
        self._log(logging.ERROR, message)
        self._log(logging.ERROR, traceback.format_exc())