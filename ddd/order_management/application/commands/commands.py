import uuid
from abc import ABC
from pydantic import BaseModel, constr
from typing import Union, List, Optional
from datetime import datetime
from ddd.order_management.application import dtos
from ddd.order_management.domain import enums

class Command(BaseModel, frozen=True):

    @property
    def step_name(self) -> str:
        return self.__class__.__name__.replace("Command", "").lower()

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
