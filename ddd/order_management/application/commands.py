import uuid
from abc import ABC
from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
from ddd.order_management.infrastructure import dtos

class Command(BaseModel, frozen=True):
    pass

class CheckoutCommand(Command):
    customer_details: dtos.CustomerDetailsDTO
    address: dtos.AddressDTO
    line_items: List[dtos.LineItemDTO]

class ConfirmOrderCommand(Command):
    order_id: str

class ShipOrderCommand(Command):
    order_id: str

class CancelOrderCommand(Command):
    order_id: str

class CompleteOrderCommand(Command):
    order_id: str

class ApplyPaymentCommand(Command):
    order_id: str
    payment: dtos.PaymentDetailsDTO