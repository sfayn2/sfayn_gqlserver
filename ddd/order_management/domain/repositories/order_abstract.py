from __future__ import annotations
from abc import ABC, abstractmethod
from ddd.order_management.domain import models


class OrderAbstract(ABC):

    def __init__(self):
        #set to make it unique
        self.seen = set() #track loaded entities for event collection

    @abstractmethod
    def save(self, order: models.Order):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def get(self, order_id: str) -> models.Order:
        raise NotImplementedError("Subclasses must implement this method")