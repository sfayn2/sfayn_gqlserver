from abc import ABC, abstractmethod
from datetime import datetime

class ClockAbstract(ABC):
    @abstractmethod
    def now(self) -> datetime:
        raise NotImplementedError("Subclasses must implement this method")


class DomainClock:
    _provider: ClockAbstract | None = None

    @classmethod
    def configure(cls, provider: ClockAbstract) -> None:
        cls._provider = provider

    @classmethod
    def now(cls) -> datetime:
        if cls._provider is None:
            raise RuntimeError("DomainClock provider not configured")
        return cls._provider.now()