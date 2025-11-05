from __future__ import annotations

class LoggingFactory:

    @classmethod
    def configure(cls, provider: LogProviderAbstract) -> None:
        cls._provider = provider

    @classmethod
    def info(cls, message: str, **kwargs: Any) -> None:
        if cls._provider is None:
            raise RuntimeError("Logging provider not configured")
        return cls._provider.info(message, **kwargs or None)

    @classmethod
    def error(cls, message: str, **kwargs: Any) -> None:
        if cls._provider is None:
            raise RuntimeError("Logging provider not configured")
        return cls._provider.error(message, **kwargs or None)

    @classmethod
    def warning(cls, message: str, **kwargs: Any) -> None:
        if cls._provider is None:
            raise RuntimeError("Logging provider not configured")
        return cls._provider.warning(message, **kwargs or None)