from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING
from dataclasses import dataclass, asdict
from pydantic import BaseModel
from ddd.order_management.domain import value_objects, enums


@dataclass(frozen=True)    
class DomainEvent(ABC):
    tenant_id: str
    order_id: str
    order_status: enums.OrderStatus
    activity_status: str

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
    pass

@dataclass(frozen=True)    
class ConfirmedOrderEvent(DomainEvent):
    pass

@dataclass(frozen=True)    
class ShippedOrderEvent(DomainEvent):
    pass

@dataclass(frozen=True)    
class DeliveredOrderEvent(DomainEvent):
    pass

@dataclass(frozen=True)    
class CanceledOrderEvent(DomainEvent):
    pass

@dataclass(frozen=True)    
class CompletedOrderEvent(DomainEvent):
    pass

@dataclass(frozen=True)    
class AppliedPaymentEvent(DomainEvent):
    pass

@dataclass(frozen=True)    
class CheckedOutEvent(DomainEvent):
    pass

@dataclass(frozen=True)    
class SelectedShippingOptionEvent(DomainEvent):
    pass

@dataclass(frozen=True)    
class AppliedOffersEvent(DomainEvent):
    pass

@dataclass(frozen=True)    
class AppliedCouponEvent(DomainEvent):
    pass

@dataclass(frozen=True)    
class RemovedCouponEvent(DomainEvent):
    pass

@dataclass(frozen=True)    
class ChangedDestinationEvent(DomainEvent):
    pass

@dataclass(frozen=True)    
class AppliedTaxesEvent(DomainEvent):
    pass

@dataclass(frozen=True)    
class ActivityEvent(DomainEvent):
    step_name: str