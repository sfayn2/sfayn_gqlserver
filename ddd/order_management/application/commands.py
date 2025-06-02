import uuid
from abc import ABC
from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
from ddd.order_management.application import dtos
from ddd.order_management.domain import enums

class Command(BaseModel, frozen=True):
    pass

class CheckoutItemsCommand(Command):
    customer_details: dtos.CustomerDetailsDTO
    shipping_address: dtos.AddressDTO
    line_items: List[dtos.LineItemDTO]

class PlaceOrderCommand(Command):
    order_id: str
    
class MarkAsShippedOrderCommand(Command):
    order_id: str

class ConfirmOrderCommand(Command):
    order_id: str
    transaction_id: str
    payment_method: enums.PaymentMethod

class SelectShippingOptionCommand(Command):
    order_id: str
    shipping_details: dtos.ShippingDetailsDTO

class ShipOrderCommand(Command):
    order_id: str

class CancelOrderCommand(Command):
    order_id: str

class CompleteOrderCommand(Command):
    order_id: str

class ApplyPaymentCommand(Command):
    order_id: str
    payment: dtos.PaymentDetailsDTO