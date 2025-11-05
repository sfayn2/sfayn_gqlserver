from __future__ import annotations
import json
from typing import Dict, Any, Type
from ddd.order_management.application import ports, dtos
from ddd.order_management.domain import exceptions

# EventPayloadDecoderAbstract
class RedisEventPayloadDecoder:

    def __init__(self, event_models: Dict[str, Type[dtos.IntegrationEvent]]):
        self.event_models = event_models

    def decode(self, raw_event: Dict[str, Any]) -> dtos.IntegrationEvent:
        event_type = raw_event.get("event_type")
        event_model = self.event_models.get(event_type)
        if not event_model:
            raise exceptions.IntegrationException(f"[RedisEventPayloadDecoder] No model registered for event type {event_type}.")

        try:
            event1 = {
                "event_type": raw_event.get("event_type"),
                "data": json.loads(raw_event.get("data"))
            }
            event_payloads = event_model(**event1)
        except Exception as e:
            raise exceptions.IntegrationException(f"[RedisEventPayloadDecoder] Payload validation failed for {event_type} {e}")

        return event_payloads
