from __future__ import annotations
import uuid
from abc import ABC, abstractmethod

class EventPayloadDecoderAbstract(ABC):

    @abstractmethod
    def decode(self, raw_event: Dict[str, Any]):
        raise NotImplementedError("Subclasses must implement this method")