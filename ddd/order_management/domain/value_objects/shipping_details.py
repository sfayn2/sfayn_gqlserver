from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from ddd.order_management.domain import enums, exceptions
from .money import Money


@dataclass(frozen=True)
class ShippingDetails:
    #customer shipping option
    method: enums.ShippingMethod

    delivery_time: str
    cost: Money
    #orig_cost: Money

    def __post_init__(self):
        if not self.method:
            raise exceptions.ShippingDetailsException("Shipping method is required.")

        if not self.cost:
            raise exceptions.ShippingDetailsException("Shipping cost is required.")

        if not self.delivery_time:
            raise exceptions.ShippingDetailsException("Delivery time is required.")

        if not self.method.value in [item.value for item in enums.ShippingMethod]:
            raise exceptions.ShippingDetailsException(f"Shipping method {self.method.value} not supported.")

        if self.cost and self.cost.amount < Decimal("0"):
            raise exceptions.ShippingDetailsException("Shipping cost cannot be negative.")

        
    #make use of order.update_shipping_details to take effect
    #def reset_cost(self):
    #    return ShippingDetails(method=self.method, 
    #                           delivery_time=self.delivery_time, 
    #                           cost=self.orig_cost, 
    #                           orig_cost=self.orig_cost
    #                        )

    #make use of order.update_shipping_details to take effect
    def update_cost(self, new_cost: Money):
        return ShippingDetails(method=self.method, 
                               delivery_time=self.delivery_time, 
                               cost=new_cost
                            )