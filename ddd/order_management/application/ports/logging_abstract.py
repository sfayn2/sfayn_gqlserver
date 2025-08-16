from __future__ import annotations
from abc import ABC, abstractmethod

class LoggingAbstract(ABC):
    @abstractmethod
    def log(self, message: str):
        raise NotImplementedError("Subclasses must implement this method")