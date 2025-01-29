import uuid
from abc import ABC
from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
from ddd.order_management.infrastructure import dtos

class Command(BaseModel, frozen=True):
    pass

class DraftOrderCommand(Command):
    customer_details: dtos.CustomerDetailsDTO
    address: dtos.AddressDTO
    line_items: List[dtos.LineItemDTO]

class PlaceOrderCommand(Command):
    order_id: str
    customer_details: dtos.CustomerDetailsDTO
    shipping_address: dtos.AddressDTO
    line_items: List[dtos.LineItemDTO]
    shipping_details = dtos.ShippingDetailsDTO
    coupons: List[dtos.CouponDTO]

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