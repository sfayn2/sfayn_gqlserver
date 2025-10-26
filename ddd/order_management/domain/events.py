from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING, Dict, Any
from dataclasses import dataclass, asdict, field
from ddd.order_management.domain import value_objects, enums


@dataclass(frozen=True)    
class DomainEvent(ABC):
    tenant_id: str
    order_id: str
    order_status: enums.OrderStatus

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
class CanceledOrderEvent(DomainEvent):
    pass

@dataclass(frozen=True)    
class CompletedOrderEvent(DomainEvent):
    pass

@dataclass(frozen=True)    
class ShippedShipmentEvent(DomainEvent):
    shipment_id: str

@dataclass(frozen=True)    
class DeliveredShipmentEvent(DomainEvent):
    shipment_id: str

@dataclass(frozen=True)    
class CanceledShipmentEvent(DomainEvent):
    shipment_id: str

@dataclass(frozen=True)    
class TrackingReferenceAssignedEvent(DomainEvent):
    shipment_id: str

@dataclass(frozen=True)    
class ShipmentAddedEvent(DomainEvent):
    shipment_id: str