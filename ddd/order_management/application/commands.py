import uuid
from abc import ABC
from pydantic import BaseModel, constr
from typing import Union, List, Optional
from datetime import datetime
from ddd.order_management.application import dtos
from ddd.order_management.domain import enums

class Command(BaseModel, frozen=True):
    pass

class Command1(Command):
    token: str

class CheckoutItemsCommand(Command1):
    #customer_id: constr(min_length=1, strip_whitespace=True)
    customer_details: dtos.CustomerDetailsDTO
    vendor_id: constr(min_length=1, strip_whitespace=True)
    address: dtos.AddressDTO
    product_skus: List[dtos.ProductSkusDTO]

class PlaceOrderCommand(Command1):
    order_id: str
    
class AddShippingTrackingReferenceCommand(Command1):
    order_id: str
    shipping_reference: str

class AddCouponCommand(Command1):
    order_id: str
    coupon_code: str

class ConfirmOrderCommand(Command1):
    order_id: str
    transaction_id: str
    payment_method: enums.PaymentMethod
    provider: str

class SelectShippingOptionCommand(Command1):
    order_id: str
    shipping_details: dtos.ShippingOptionDTO

class ShipOrderCommand(Command1):
    order_id: str

class CancelOrderCommand(Command1):
    order_id: str
    cancellation_reason: str

class CompleteOrderCommand(Command1):
    order_id: str

class ApplyPaymentCommand(Command1):
    order_id: str
    payment: dtos.PaymentDetailsDTO

class ChangeDestinationCommand(Command1):
    order_id: str
    address: dtos.AddressDTO

class ChangeOrderQuantityCommand(Command1):
    order_id: constr(min_length=1, strip_whitespace=True)
    product_sku: constr(min_length=1, strip_whitespace=True)
    new_quantity: int

class AddLineItemsCommand(Command1):
    order_id: constr(min_length=1, strip_whitespace=True)
    product_skus: List[dtos.ProductSkusDTO]

class RemoveLineItemsCommand(Command1):
    order_id: constr(min_length=1, strip_whitespace=True)
    product_skus: List[dtos.ProductSkusDTO]

class LoginCallbackCommand(Command1):
    code: constr(min_length=1, strip_whitespace=True)
    redirect_uri: constr(min_length=1, strip_whitespace=True)
    next_path: constr(min_length=1, strip_whitespace=True)

# ----------------
# Applicable to Webhook APIs / Integration events
# -----------
class Command2(Command):
    event_type: str

# {
#    "event_type": "events.ProductUpdateEvent",
#    "tenant_id": "tenant1",
#    "data": { ... }
# }
class PublishProductUpdateCommand(Command2):
    data: dtos.VendorProductSnapshotDTO

class PublishVendorDetailsUpdateCommand(Command2):
    data: dtos.VendorDetailsSnapshotDTO

class PublishVendorCouponUpdateCommand(Command2):
    data: dtos.VendorCouponSnapshotDTO

class PublishVendorOfferUpdateCommand(Command2):
    data: dtos.VendorOfferSnapshotDTO

class PublishVendorShippingOptionUpdateCommand(Command2):
    data: dtos.VendorShippingOptionSnapshotDTO

class PublishVendorPaymentOptionUpdateCommand(Command2):
    data: dtos.VendorPaymentOptionSnapshotDTO

class PublishVendorTaxOptionUpdateCommand(Command2):
    data: dtos.VendorTaxOptionSnapshotDTO