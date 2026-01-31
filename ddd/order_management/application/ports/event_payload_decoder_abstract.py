from __future__ import annotations
from abc import abstractmethod
from typing import Protocol, Dict, Any
from ddd.order_management.application import dtos

class EventPayloadDecoderAbstract(Protocol):
    def decode(self, raw_event: Dict[str, Any]) -> dtos.IntegrationEvent: ...