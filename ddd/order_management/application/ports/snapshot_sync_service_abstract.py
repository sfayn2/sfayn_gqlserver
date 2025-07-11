from __future__ import annotations
from abc import ABC, abstractmethod

#Snapshot from external event payloads
class SnapshotSyncServiceAbstract(ABC)
    def sync(self, event: dtos.UserLoggedInIntegrationEvent):
        raise NotImplementedError("Subclasses must implement this method")