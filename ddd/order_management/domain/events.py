from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING
from dataclasses import dataclass, asdict
from pydantic import BaseModel
from ddd.order_management.domain import value_objects, enums

if TYPE_CHECKING:
    from ddd.order_management.domain import models

class DomainEvent(ABC):

    def event_type(self) -> str:
        return f"order_management.events.{self.__class__.__name__}"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> DomainEvent:
        return cls(**data)



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
class OrderPaymentAppliedEvent(DomainEvent):
    order_id: str
    amount: value_objects.Money

@dataclass
class OrderOffersAppliedEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus

@dataclass
class OrderDraftEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus
