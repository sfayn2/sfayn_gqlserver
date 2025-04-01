import uuid
from abc import ABC
from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
from ddd.order_management.domain import enums
from ddd.order_management.infrastructure import order_dtos

class Command(BaseModel, frozen=True):
    pass

class PlaceOrderCommand(Command):
    #order_id: str
    customer_details: order_dtos.CustomerDetailsDTO
    shipping_address: order_dtos.AddressDTO
    line_items: List[order_dtos.LineItemDTO]
    shipping_details: order_dtos.ShippingDetailsDTO
    coupons: List[order_dtos.CouponDTO]

class ConfirmOrderCommand(Command):
    order_id: str
    transaction_id: str
    payment_method: enums.PaymentMethod

class SelectShippingOptionCommand(Command):
    order_id: str
    shipping_details: order_dtos.ShippingDetailsDTO

class ShipOrderCommand(Command):
    order_id: str

class CancelOrderCommand(Command):
    order_id: str

class CompleteOrderCommand(Command):
    order_id: str

class ApplyPaymentCommand(Command):
    order_id: str
    payment: order_dtos.PaymentDetailsDTO