import uuid
from abc import ABC
from pydantic import BaseModel, constr
from typing import Union, List, Optional
from datetime import datetime
from ddd.order_management.application import dtos
from ddd.order_management.domain import enums

class Command(BaseModel, frozen=True):
    pass

class AddShippingTrackingReferenceCommand(Command):
    order_id: str
    shipping_reference: str

class ShipOrderCommand(Command):
    order_id: str

class CancelOrderCommand(Command):
    order_id: str
    cancellation_reason: str

class CompleteOrderCommand(Command):
    order_id: str


class AddShipmentCommand(Command):
    order_id: str
    shipment_id: str
    shipment_address: dict
    shipment_amount: Optional[dict] = None
    shipment_tax_amount: Optional[dict] = None
    shipment_items: list[dict]

