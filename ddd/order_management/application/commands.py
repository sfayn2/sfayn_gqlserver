import uuid
from abc import ABC
from dataclasses import dataclass
from typing import Union, List, Optional
from datetime import datetime
from ddd.order_management.domain import enums, value_objects, models

class Command(ABC):
    pass

@dataclass
class CheckoutCommand(Command):
    customer_id: Optional[bool]
    first_name: str
    last_name: str
    email: str
    address: value_objects.Address
    line_items: List[models.LineItem]


@dataclass
class ConfirmOrderCommand:
    order_id: str

@dataclass
class ShipOrderCommand:
    order_id: str

@dataclass
class CancelOrderCommand:
    order_id: str

@dataclass
class CompleteOrderCommand:
    order_id: str

@dataclass
class ApplyPaymentCommand:
    order_id: str
    payment: value_objects.Payment