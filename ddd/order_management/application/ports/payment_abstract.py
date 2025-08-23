from __future__ import annotations
from abc import ABC, abstractmethod
from ddd.order_management.domain import value_objects, enums

# ========
# Payment contract
# ==========
class PaymentGatewayAbstract(ABC):

    @abstractmethod
    def is_eligible(self, order: models.Order) -> bool:
        """
            Determine if payment option is eligible for the given package.
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def get_payment_details(self) -> value_objects.PaymentDetails:
        raise NotImplementedError("Subclasses must implement this method")

