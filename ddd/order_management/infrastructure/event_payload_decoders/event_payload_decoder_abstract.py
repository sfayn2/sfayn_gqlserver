from __future__ import annotations
from typing import Protocol

class EventPayloadDecoderAbstract(Protocol):

    @abstractmethod
    def decode(self, raw_event: Dict[str, Any]) -> dtos.IntegrationEvent: ...