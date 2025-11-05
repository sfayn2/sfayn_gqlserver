from __future__ import annotations

class LoggingFactory:

    @classmethod
    def configure(cls, provider: ports.LoggingAbstract) -> None:
        cls._provider = provider

    @classmethod
    def get_logger(cls) -> ports.LoggingAbstract:
        # Prep for multi logger based on Tenant?
        if cls._provider is None:
            raise RuntimeError("Logging provider not configured")
        return cls._provider
