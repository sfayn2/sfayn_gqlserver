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

class CheckoutItemsCommand(Command):
    customer_details: dtos.CustomerDetailsDTO
    address: dtos.AddressDTO
    product_skus: List[dtos.ProductSkusDTO]

class PlaceOrderCommand(Command):
    order_id: str
    
class AddShippingTrackingReferenceCommand(Command):
    order_id: str
    shipping_reference: str

class AddCouponCommand(Command):
    order_id: str
    coupon_code: str

class RemoveCouponCommand(Command):
    order_id: str
    coupon_code: str

class ConfirmOrderCommand(Command):
    order_id: str
    transaction_id: str
    payment_method: enums.PaymentMethod
    provider: str

class SelectShippingOptionCommand(Command):
    order_id: str
    shipping_details: dtos.ShippingOptionDTO

class ShipOrderCommand(Command):
    order_id: str

class CancelOrderCommand(Command):
    order_id: str
    cancellation_reason: str

class CompleteOrderCommand(Command):
    order_id: str

class ApplyPaymentCommand(Command):
    order_id: str
    payment: dtos.PaymentDetailsDTO

class ChangeDestinationCommand(Command):
    order_id: str
    address: dtos.AddressDTO

class ChangeOrderQuantityCommand(Command):
    order_id: constr(min_length=1, strip_whitespace=True)
    product_skus: List[dtos.ProductSkusDTO]
    #product_sku: constr(min_length=1, strip_whitespace=True)
    #new_quantity: int

class AddLineItemsCommand(Command):
    order_id: constr(min_length=1, strip_whitespace=True)
    product_skus: List[dtos.ProductSkusDTO]

class RemoveLineItemsCommand(Command):
    order_id: constr(min_length=1, strip_whitespace=True)
    product_skus: List[dtos.ProductSkusDTO]



