import uuid
from abc import ABC
from decimal import Decimal
from pydantic import BaseModel, constr
from typing import Union, List, Optional
from datetime import datetime
from ddd.order_management.application import dtos
from ddd.order_management.domain import enums

class Command(BaseModel):
    pass

class AddShippingTrackingReferenceCommand(Command):
    order_id: str
    tracking_reference: str

class ShipOrderCommand(Command):
    order_id: str

class CancelOrderCommand(Command):
    order_id: str
    #cancellation_reason: str

class CompleteOrderCommand(Command):
    order_id: str


class AddShipmentCommand(Command):
    order_id: str

    shipment_mode: str # pickup, dropoff, warehouse
    shipment_provider: str #easypost, fedex, etc

    # package
    package_weight_kg: Optional[Decimal] = None
    package_length_cm: Optional[Decimal] = None
    package_width_cm: Optional[Decimal] = None
    package_height_cm: Optional[Decimal] = None

    # pickup mode
    pickup_address: Optional[dtos.AddressDTO] = None
    pickup_window_start: Optional[datetime] = None
    pickup_window_end: Optional[datetime] = None
    pickup_instructions: Optional[str] = None

    shipment_address: dtos.AddressDTO
    shipment_items: list[dtos.ShipmentItemDTO]



class ConfirmShipmentCommand(Command):
    order_id: str
    shipment_id: str

class DeliverShipmentCommand(Command):
    order_id: str
    shipment_id: str

class CancelShipmentCommand(Command):
    order_id: str
    shipment_id: str

class AddOrderCommand(Command, dtos.AddOrderDTO):
    pass