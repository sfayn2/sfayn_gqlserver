from __future__ import annotations
from datetime import time
from abc import ABC, abstractmethod

class ClockAbstract(ABC):

    @abstractmethod
    def now(self) -> time:
        raise NotImplementedError("Subclasses must implement this method")