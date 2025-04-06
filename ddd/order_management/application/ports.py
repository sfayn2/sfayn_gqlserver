from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from ddd.order_management.domain import enums, value_objects, models, repositories

class PaymentGatewayAbstract(ABC):

    @abstractmethod
    def get_payment_details(self):
        raise NotImplementedError("Subclasses must implement this method")

class PaymentGatewayFactoryAbstract(ABC):

    @abstractmethod
    def get_payment_gateway(self, payment_method: enums.PaymentMethod) -> PaymentGatewayAbstract:
        raise NotImplementedError("Subclasses must implement this method")


class ShippingOptionStrategyAbstract(ABC):

    def __init__(self, strategy: value_objects.ShippingOptionStrategy):
        self.strategy = strategy

    @abstractmethod
    def is_eligible(self, order: models.Order) -> bool:
        """
            Determine if shipping option is eligible for the given package.
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def calculate_cost(self, order: models.Order) -> value_objects.Money:
        """
            Calculate the cost of shipping based on weight and dimensions
        """
        raise NotImplementedError("Subclasses must implement this method")

class ShippingOptionStrategyServiceAbstract:

    def __init__(self, vendor_repository: repositories.VendorAbstract):
        self.vendor_repository = vendor_repository

    @abstractmethod
    def get_shipping_options(self, order: models.Order) -> List[value_objects.ShippingDetails]:
        raise NotImplementedError("Subclasses must implement this method")