from __future__ import annotations
import boto3
import json
import redis
from typing import List
from decimal import Decimal

from ddd.order_management.application import ports

#EventPublisherAbstract
class EventBridgePublisher:
    def __init__(self, event_bus_name: str, source: str = "saas.oms", aws_region: str = "us-east-1"):
        self.event_bus_name = event_bus_name
        self.source = source # Get from environment
        self.client = boto3.client("events", region_name=aws_region)

    def publish(self, event):
        try:
            response = self.client.put_events(
                Entries=[{
                    "Source": self.source,
                    "DetailType": event.event_type,
                    "Detail": json.dumps(event.data.model_dump()),
                    "EventBusName": self.event_bus_name
                }]
            )
            # CRITICAL: Check for failed entries in the response
            if response.get("FailedEntryCount", 0) > 0:
                errors = [entry.get("ErrorMessage") for entry in response["Entries"] if "ErrorCode" in entry]
                print(f"[EventBridgePublisher] Partial failure: {errors}")
        except Exception as e:
            print(f"[EventBridgePublisher] Critical error: {e}")
