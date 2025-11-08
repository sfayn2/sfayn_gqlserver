from __future__ import annotations
from typing import Protocol
from ddd.order_management.domain import repositories
#from abc import ABC, abstractmethod

class UnitOfWorkAbstract(Protocol):

    order: repositories.OrderAbstract 

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self): ...

    def rollback(self): ...

    #@abstractmethod
    #def commit(self):
    #    raise NotImplementedError("Subclasses must implement this method")

    #@abstractmethod
    #def rollback(self):
    #    raise NotImplementedError("Subclasses must implement this method")
