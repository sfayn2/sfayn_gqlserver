from __future__ import annotations


#Protocol from porst.LoggingAbstract
class StdLogProvider:

    def __init__(self, name: str = "app"):
        self.logger = logging.getlogger(name)
        self._configure_default_handler()

    def _configure_default_handler(self) -> None:
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log(self, message: str, **kwargs: Any) -> None:
        self.logger.info(message, extra=kwargs or None)
