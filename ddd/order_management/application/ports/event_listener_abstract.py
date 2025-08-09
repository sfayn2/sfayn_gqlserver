from __future__ import annotations
import uuid
from abc import ABC, abstractmethod

class EventListenerAbstract(ABC):

    @abstractmethod
    def listen(event):
        raise NotImplementedError("Subclasses must implement this method")