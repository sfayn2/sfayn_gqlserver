import uuid
from abc import ABC
from dataclasses import dataclass
from typing import Union, List
from datetime import datetime
from ddd.order_management.domain import enums, value_objects

class Command(ABC):
    pass

@dataclass
class CreateOrderCommand(Command):
    customer_id: str
    address: value_objects.Address
    order_lines: List[value_objects.OrderLine]

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