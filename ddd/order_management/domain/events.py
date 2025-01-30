from abc import ABC
from typing import List
from dataclasses import dataclass
from pydantic import BaseModel
from ddd.order_management.domain import value_objects, models, enums
from ddd.order_management.infrastructure import order_dtos

class DomainEvent(ABC):
    pass

@dataclass
class ProductCheckedout(DomainEvent):
    order_id: str
    destination: value_objects.Address
    customer_details: value_objects.CustomerDetails
    line_items: List[models.LineItem]

@dataclass
class OrderPlaced(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus
    customer_details: value_objects.CustomerDetails
    shipping_details: value_objects.ShippingDetails
    line_items: List[models.LineItem]
    tax_details: List[str]
    tax_amount: value_objects.Money
    offer_details: List[str]
    total_discounts_fee: value_objects.Money
    final_amount: value_objects.Money


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
