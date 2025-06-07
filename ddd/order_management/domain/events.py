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



@dataclass
class OrderPlacedEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus

    @classmethod
    def from_dict(cls, data: dict) -> OrderPlacedEvent:
        return cls(**data)


@dataclass
class OrderConfirmedEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus

    @classmethod
    def from_dict(cls, data: dict) -> OrderConfirmedEvent:
        return cls(**data)

@dataclass
class OrderShippedEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus

    @classmethod
    def from_dict(cls, data: dict) -> OrderShippedEvent:
        return cls(**data)

@dataclass
class OrderCanceledEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus

    @classmethod
    def from_dict(cls, data: dict) -> OrderCanceledEvent:
        return cls(**data)

@dataclass
class OrderCompletedEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus

    @classmethod
    def from_dict(cls, data: dict) -> OrderCompletedEvent:
        return cls(**data)

@dataclass
class PaymentAppliedEvent(DomainEvent):
    order_id: str
    amount: value_objects.Money

    @classmethod
    def from_dict(cls, data: dict) -> PaymentAppliedEvent:
        return cls(**data)

@dataclass
class OffersAppliedEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus

    @classmethod
    def from_dict(cls, data: dict) -> OffersAppliedEvent:
        return cls(**data)

@dataclass
class OrderDraftEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus

    @classmethod
    def from_dict(cls, data: dict) -> OrderDraftEvent:
        return cls(**data)
