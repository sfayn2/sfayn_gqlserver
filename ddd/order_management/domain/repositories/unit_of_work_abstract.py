from __future__ import annotations
from abc import ABC, abstractmethod

class UnitOfWorkAbstract(ABC):

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def rollback(self):
        raise NotImplementedError("Subclasses must implement this method")