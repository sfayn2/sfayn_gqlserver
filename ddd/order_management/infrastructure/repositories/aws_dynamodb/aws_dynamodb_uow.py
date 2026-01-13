from __future__ import annotations
import boto3
from typing import List
from ddd.order_management.infrastructure import event_bus, repositories as impl_repositories

class DynamoOrderUnitOfWork:
    def __init__(self, table_name: str):
        # Initialize the DynamoDB repository
        self.order = impl_repositories.DynamoOrderRepositoryImpl(table_name=table_name)
        self.event_publisher = event_bus
        self._events: List = []

    def __enter__(self):
        # In DynamoDB, there is no "begin transaction" session to start.
        # We simply return the UoW instance to start the context.
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # If an exception occurred, we do not commit.
        if exc_type:
            self.rollback()
        # Clean up events/seen entities regardless of success
        self.order.seen.clear()

    def commit(self):
        """
        In DDD, commit() persists all changes tracked by the repository.
        """
        # 1. Persist all seen aggregates to DynamoDB
        for entity in self.order.seen:
            self.order.save(entity)

        # 2. Handle side effects (Domain Events)
        while True:
            self._collect_events()
            if not self._events:
                break
            self._publish_events()

    def rollback(self):
        """
        DynamoDB does not support local rollbacks of already-sent 'put_item' calls.
        In this pattern, rollback simply ensures no further actions are taken.
        """
        # Clear local tracking to prevent accidental commits
        self.order.seen.clear()
        self._events = []

    def _collect_events(self):
        self._events = []
        for entity in self.order.seen:
            if hasattr(entity, "_events"):
                self._events.extend(entity._events)
                entity._events = [] # Clear events from entity after collecting

    def _publish_events(self):
        for event in self._events:
            print(f"Publishing event to EventBridge/SNS: {event}")
            self.event_publisher.publish(event, self)
