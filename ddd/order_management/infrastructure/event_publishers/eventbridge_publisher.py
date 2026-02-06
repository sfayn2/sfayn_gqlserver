from __future__ import annotations
import boto3
import json
import redis
from typing import List
from decimal import Decimal

from ddd.order_management.application import ports

#EventPublisherAbstract
class EventBridgePublisher:
    def __init__(self, event_bus_name: str, source_list: List[str]):
        self.event_bus_name = event_bus_name
        self.source_list = source_list # Get from environment
        self.client = boto3.client("events")

    def publish(self, event):
        for source in self.source_list:
            try:
                # Pydantic's model_dump_json() automatically converts 
                # datetimes to ISO format strings.
                detail_json = event.data.model_dump_json()

                response = self.client.put_events(
                    Entries=[{
                        "Source": source,
                        "DetailType": event.event_type,
                        "Detail": detail_json,
                        "EventBusName": self.event_bus_name
                    }]
                )
                print("Evenbridge publish response:", response)
                # CRITICAL: Check for failed entries in the response
                if response.get("FailedEntryCount", 0) > 0:
                    errors = [entry.get("ErrorMessage") for entry in response["Entries"] if "ErrorCode" in entry]
                    print(f"[EventBridgePublisher] Partial failure: {errors}")
            except Exception as e:
                print(f"[EventBridgePublisher] Critical error: {e}")
