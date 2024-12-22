from abc import ABC
from dataclasses import dataclass
from ddd.order_management.domain import value_objects

class DomainEvent(ABC):
    pass

@dataclass
class OrderPlaced(DomainEvent):
    order_id: str
    customer_id: str

@dataclass
class OrderConfirmed(DomainEvent):
    order_id: str

@dataclass
class OrderShipped(DomainEvent):
    order_id: str

@dataclass
class OrderCancelled(DomainEvent):
    order_id: str

@dataclass
class OrderCompleted(DomainEvent):
    order_id: str

@dataclass
class PaymentApplied(DomainEvent):
    order_id: str
    amount: value_objects.Money