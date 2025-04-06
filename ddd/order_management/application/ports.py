from __future__ import annotations
from abc import ABC, abstractmethod
from ddd.order_management.domain import enums

class PaymentGatewayAbstract(ABC):

    @abstractmethod
    def get_payment_details(self):
        raise NotImplementedError("Subclasses must implement this method")

class PaymentGatewayFactoryAbstract(ABC):

    @abstractmethod
    def get_payment_gateway(payment_method: enums.PaymentMethod):
        raise NotImplementedError("Subclasses must implement this method")

