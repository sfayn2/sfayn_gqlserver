from abc import ABC
from typing import List
from dataclasses import dataclass
from ddd.order_management.domain import value_objects, models

class DomainEvent(ABC):
    pass

@dataclass(frozen=True)
class ProductCheckedout(DomainEvent):
    order_id: str
    destination: value_objects.Address
    customer_details: value_objects.CustomerDetails
    line_items: List[models.LineItem]

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
