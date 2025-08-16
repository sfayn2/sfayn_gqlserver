from __future__ import annotations
from abc import ABC, abstractmethod
from ddd.order_management.domain import value_objects, enums

# ========
# Payment contract
# ==========
class PaymentGatewayAbstract(ABC):

    @abstractmethod
    def get_payment_details(self) -> value_objects.PaymentDetails:
        raise NotImplementedError("Subclasses must implement this method")
