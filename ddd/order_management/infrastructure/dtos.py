import datetime
from pydantic import BaseModel
from typing import List, Optional
from ddd.order_management.domain import value_objects, models, enums

class DjangoToDomainOrderDTO(BaseModel):
    order_id: str
    date_created: datetime 
    destination: value_objects.Address
    line_items: List[models.LineItem]
    customer_details: value_objects.CustomerDetails
    shipping_details: value_objects.ShippingDetails
    payment_details: value_objects.PaymentDetails
    cancellation_reason: str
    total_discounts_fee: value_objects.Money
    offer_details: str
    tax_details: str
    tax_amount: value_objects.Money
    total_amount: value_objects.Money
    final_amount: value_objects.Money
    shipping_reference: str
    coupon_codes: List[str]
    status: enums.OrderStatus
    date_modified: datetime

    def to_domain(self):
        return models.Order(**self.dict())