from __future__ import annotations
import uuid
from abc import ABC, abstractmethod

class EventPublisherAbstract(ABC):

    @abstractmethod
    def publish(event):
        raise NotImplementedError("Subclasses must implement this method")