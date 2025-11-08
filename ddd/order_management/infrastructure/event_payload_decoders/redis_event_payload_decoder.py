from __future__ import annotations
import json
from typing import Dict, Any, Type, Optional, Union
from ddd.order_management.application import ports, dtos
from ddd.order_management.domain import exceptions

# ports.EventPayloadDecoderAbstract
class RedisEventPayloadDecoder:

    def __init__(self, event_models: Dict[str, Type[dtos.IntegrationEvent]]):
        self.event_models = event_models

    def decode(self, raw_event: Dict[str, Any]) -> dtos.IntegrationEvent:
        # Explicitly type the result to help the type checker understand the potential None
        event_type: Optional[str] = raw_event.get("event_type")
         # Explicitly check that event_type is not None before using it as a key
        if event_type is None:
            raise exceptions.IntegrationException("[RedisEventPayloadDecoder] Missing required 'event_type' in raw event.")

        event_model = self.event_models.get(event_type)
        if not event_model:
            raise exceptions.IntegrationException(f"[RedisEventPayloadDecoder] No model registered for event type {event_type}.")

        raw_data_value: Optional[Union[str, bytes]] = raw_event.get("data")

        if raw_data_value is None:
             raise exceptions.IntegrationException(f"[RedisEventPayloadDecoder] Missing required 'data' field for event {event_type}.")

        # If data is a byte string (very likely from Redis), decode it first
        if isinstance(raw_data_value, bytes):
            json_string = raw_data_value.decode('utf-8')
        elif isinstance(raw_data_value, str):
            json_string = raw_data_value
        else:
            raise exceptions.IntegrationException(f"Invalid 'data' format: Expected bytes or string, got {type(raw_data_value)}.")


        try:
            event1 = {
                "event_type": raw_event.get("event_type"),
                "data": json.loads(json_string) 
            }
            event_payloads = event_model(**event1)
        except Exception as e:
            raise exceptions.IntegrationException(f"[RedisEventPayloadDecoder] Payload validation failed for {event_type} {e}")

        return event_payloads
