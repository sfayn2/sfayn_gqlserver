from __future__ import annotations
from abc import ABC
from typing import List, TYPE_CHECKING
from dataclasses import dataclass
from pydantic import BaseModel
from ddd.order_management.domain import value_objects, enums
from ddd.order_management.infrastructure import order_dtos

if TYPE_CHECKING:
    from ddd.order_management.domain import models

class DomainEvent(ABC):
    pass

@dataclass
class OrderPlaced(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus

@dataclass
class OrderConfirmed(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus

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
