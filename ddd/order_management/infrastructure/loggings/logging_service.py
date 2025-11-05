from __future__ import annotations
from typing import Any, Optional

# Define a specific exception
class LoggingConfigurationError(RuntimeError):
    pass

class LoggingService:
    # Initialize as None, but with a type hint that clarifies its intended type
    _provider: Optional[LogProviderAbstract] = None

    @classmethod
    def configure(cls, provider: LogProviderAbstract) -> None:
        if cls._provider is not None:
             # Prevent reconfiguration after the app has started
             raise LoggingConfigurationError("Logging provider already configured.")
        cls._provider = provider

    @classmethod
    def _get_provider_safe(cls) -> LogProviderAbstract:
        """Helper method to check configuration once."""
        if cls._provider is None:
            # Raise an explicit configuration error
            raise LoggingConfigurationError("Logging provider not configured.")
        return cls._provider

    @classmethod
    def info(cls, message: str, **kwargs: Any) -> None:
        # Use the helper method to reduce repetition
        cls._get_provider_safe().info(message, **kwargs)

    @classmethod
    def error(cls, message: str, **kwargs: Any) -> None:
        cls._get_provider_safe().error(message, **kwargs)

    @classmethod
    def warning(cls, message: str, **kwargs: Any) -> None:
        cls._get_provider_safe().warning(message, **kwargs)

