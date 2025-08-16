from __future__ import annotations
from abc import ABC, abstractmethod

#Snapshot from external event payloads
class SnapshotRepoAbstract(ABC):

    @abstractmethod
    def sync(self, event):
        raise NotImplementedError("Subclasses must implement this method")