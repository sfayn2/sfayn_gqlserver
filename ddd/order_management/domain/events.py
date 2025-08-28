from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING
from dataclasses import dataclass, asdict
from pydantic import BaseModel
from ddd.order_management.domain import value_objects, enums

if TYPE_CHECKING:
    from ddd.order_management.domain import models

@dataclass(frozen=True)    
class DomainEvent(ABC):
    tenant_id: str

    def event_type(self) -> str:
        return f"order_management.events.{self.__class__.__name__}"

    def internal_event_type(self) -> str:
        return f"order_management.internal_events.{self.__class__.__name__}"

    def external_event_type(self) -> str:
        return f"order_management.external_events.{self.__class__.__name__}"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> DomainEvent:
        return cls(**data)



@dataclass(frozen=True)    
class PlacedOrderEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus

@dataclass(frozen=True)    
class ConfirmedOrderEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus

@dataclass(frozen=True)    
class ShippedOrderEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus

@dataclass(frozen=True)    
class CanceledOrderEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus

@dataclass(frozen=True)    
class CompletedOrderEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus

@dataclass(frozen=True)    
class AppliedPaymentEvent(DomainEvent):
    order_id: str
    amount: value_objects.Money

@dataclass(frozen=True)    
class CheckedOutEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus

@dataclass(frozen=True)    
class SelectedShippingOptionEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus

@dataclass(frozen=True)    
class AppliedOffersEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus

@dataclass(frozen=True)    
class AppliedCouponEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus

@dataclass(frozen=True)    
class RemovedCouponEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus

@dataclass(frozen=True)    
class ChangedDestinationEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus
    #TODO destination payload?

@dataclass(frozen=True)    
class AppliedTaxesEvent(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus
