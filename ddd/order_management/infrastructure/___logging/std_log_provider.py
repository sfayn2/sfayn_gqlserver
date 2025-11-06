from __future__ import annotations
import logging


#Protocol from port.LogProviderAbstract
class StdLogProvider:

    def __init__(self, name: str = "app"):
        self.logger = logging.getLogger(name)
        self._configure_default_handler()

    def _configure_default_handler(self) -> None:
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def info(self, message: str, **kwargs: Any) -> None:
        self.logger.info(message, extra=kwargs or None)

    def warning(self, message: str, **kwargs: Any) -> None:
        self.logger.warning(message, extra=kwargs or None)

    def error(self, message: str, **kwargs: Any) -> None:
        self.logger.error(message, extra=kwargs or None)
