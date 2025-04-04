from __future__ import annotations
import uuid
from abc import ABC, abstractmethod
from ddd.order_management.domain import models

class OrderRepository(ABC):

    def __init__(self):
        self.seen = [] #track loaded entities for event collection

    @abstractmethod
    def save(self, order: models.Order):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def get(self, order_id: str) -> models.Order:
        raise NotImplementedError("Subclasses must implement this method")

class CustomerRepository(ABC):

    @abstractmethod
    def get_customer_details(self, customer_id: str):
        raise NotImplementedError("Subclasses must implement this method")

class VendorRepository(ABC):

    @abstractmethod
    def get_offers(self):
        raise NotImplementedError("Subclasses must implement this method")

    #@abstractmethod
    #def get_vendor_details(self):
    #    raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def get_shipping_options(self):
        raise NotImplementedError("Subclasses must implement this method")

class PaymentGatewayRepository(ABC):

    @abstractmethod
    def get_payment_details(self):
        raise NotImplementedError("Subclasses must implement this method")

