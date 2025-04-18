from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, TypeVar
from ddd.order_management.domain import enums, models, value_objects, repositories
T = TypeVar("T")

# ========
# Payment contract
# ==========
class PaymentGatewayAbstract(ABC):

    @abstractmethod
    def get_payment_details(self):
        raise NotImplementedError("Subclasses must implement this method")

class PaymentGatewayFactoryAbstract(ABC):

    @abstractmethod
    def get_payment_gateway(self, payment_method: enums.PaymentMethod) -> PaymentGatewayAbstract:
        raise NotImplementedError("Subclasses must implement this method")




# ===
# UOW
# ===
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

# ===
# Email Service
# ===
class EmailServiceAbstract(ABC):
    @abstractmethod
    def send_email(self, message: str):
        raise NotImplementedError("Subclasses must implement this method")

# ===
# Log service
# ==
class LoggingServiceAbstract(ABC):
    @abstractmethod
    def log(self, message: str):
        raise NotImplementedError("Subclasses must implement this method")