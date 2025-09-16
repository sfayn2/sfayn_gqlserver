from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from ddd.order_management.domain import enums, exceptions
from .money import Money


@dataclass(frozen=True)
class ShippingDetails:
    #customer shipping option
    method: str
    delivery_time: str
    cost: Money

    def __post_init__(self):
        if not self.method:
            raise exceptions.ShippingDetailsException("Shipping method is required.")

        if not self.cost:
            raise exceptions.ShippingDetailsException("Shipping cost is required.")

        if not self.delivery_time:
            raise exceptions.ShippingDetailsException("Delivery time is required.")

        if self.cost and self.cost.amount < Decimal("0"):
            raise exceptions.ShippingDetailsException("Shipping cost cannot be negative.")
