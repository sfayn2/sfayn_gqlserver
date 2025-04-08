from __future__ import annotations
import uuid
from typing import TypeVar
from abc import ABC, abstractmethod
from ddd.order_management.domain import models

T = TypeVar("T")

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

class CustomerAbstract(ABC):

    @abstractmethod
    def get_customer_details(self, customer_id: str):
        raise NotImplementedError("Subclasses must implement this method")

class VendorAbstract(ABC):

    @abstractmethod
    def get_offers(self):
        raise NotImplementedError("Subclasses must implement this method")

    #@abstractmethod
    #def get_vendor_details(self):
    #    raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def get_shipping_options(self):
        raise NotImplementedError("Subclasses must implement this method")

class UnitOfWorkAbstract(ABC):

    def __enter__(self) -> T:
        return self

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def rollback(self):
        raise NotImplementedError("Subclasses must implement this method")