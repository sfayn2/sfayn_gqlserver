from __future__ import annotations
from abc import ABC
from typing import List, TYPE_CHECKING
from dataclasses import dataclass
from pydantic import BaseModel
from ddd.order_management.domain import value_objects, enums

if TYPE_CHECKING:
    from ddd.order_management.domain import models

class DomainEvent(ABC):
    pass

@dataclass
class OrderPlacedEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus

@dataclass
class OrderConfirmedEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus

@dataclass
class OrderShippedEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus

@dataclass
class OrderCanceledEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus

@dataclass
class OrderCompletedEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus

@dataclass
class PaymentAppliedEvent(DomainEvent):
    order_id: str
    amount: value_objects.Money

@dataclass
class OffersAppliedEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus

@dataclass
class OrderDraftEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus
