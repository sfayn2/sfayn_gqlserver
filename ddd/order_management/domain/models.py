from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Tuple
from dataclasses import dataclass, field
from order_management.domain import value_objects, enums, exceptions


@dataclass
class Order:
    _order_id: str
    _customer_full_name: str
    _customer_email: str
    _address: value_objects.Address
    line_items: List[value_objects.LineItem]
    _status: enums.OrderStatus = enums.OrderStatus.DRAFT.name
    _shipping_method: enums.ShippingMethod = enums.ShippingMethod.STANDARD.name
    _shipping_note: str
    _shipping_cost: value_objects.Money
    _shipping_reference: str
    _total_amount: value_objects.Money
    _coupon_codes: Optional[List[str]] = field(default_factory=list, init=False)
    _shipping_policy: Optional[str] = field(default_factory=None, init=False) #TODO should not be str
    _offer_policy: Optional[str] = field(default_factory=None, init=False) #TODO should not be str
    _payments: List[value_objects.Payment] = field(default_factory=list)
    _date_created: datetime = field(default_factory=datetime.now)
    _date_modified: Optional[datetime] = None

    #VALID_STATUS_TRANSITIONS = {
    #    enums.OrderStatus.DRAFT.name : [enums.OrderStatus.PENDING.name],
    #    enums.OrderStatus.PENDING.name : [enums.OrderStatus.CONFIRMED.name],
    #    enums.OrderStatus.CONFIRMED.name : [enums.OrderStatus.SHIPPED.name, enums.OrderStatus.CANCELLED.name],
    #    enums.OrderStatus.SHIPPED.name : [enums.OrderStatus.COMPLETED.name, enums.OrderStatus.CANCELLED.name],
    #}

    def update_modified_date(self):
        self._date_modified = datetime.now()

    #def change_state(self, new_status: enums.OrderStatus):
    #    if new_status not in self.VALID_STATUS_TRANSITIONS[self._status]:
    #        raise exceptions.InvalidStatusTransitionError(f"Cannot transition from {self._status} to {new_status}")
    #    self._status = new_status
    #    self.update_modified_date()

    def add_line_item(self, line_item: value_objects.OrderLine) -> None:
        if not line_item:
            raise "No item to add in order!"
        self.line_items.add(line_item)

    def set_offer_policy(self, offer_policy):
        if self._offer_policy:
            raise ValueError("Offer policy already set.")
        self._offer_policy = offer_policy

    def checkout(self):
        discounts_amount, free_gifts, free_shipping = self._offer_policy.get_offers()
        #TODO: free gifts need to insert in line items?

    def place(self):
        if not self.line_items:
            raise exceptions.InvalidOrderOperation("Order must have at least one line item.")
        if not self._shipping_method:
            raise exceptions.InvalidOrderOperation("Order must have a selected Shipping method")
        self._status = enums.OrderStatus.PENDING.name
        self.update_modified_date()

    def confirm(self):
        if self.status != enums.OrderStatus.PENDING.name:
            raise exceptions.InvalidOrderOperation("Only pending orders can be confirmed.")
        if not self._payment or self._payment.get_amount() < self.get_total_amount():
            raise exceptions.InvalidOrderOperation("Order cannot be confirmed without a full payment.")
        if not self._shipping_reference:
            raise exceptions.InvalidOrderOperation("Shipping reference is missing.")
        self._status = enums.OrderStatus.CONFIRMED.name
        self.update_modified_date()

    def ship(self):
        if self._status != enums.OrderStatus.CONFIRMED.name:
            raise exceptions.InvalidOrderOperation("Only confirm order can be ship.")
        self._status = enums.OrderStatus.SHIPPED.name
        self.update_modified_date()

    def cancel(self):
        if self._status in (enums.OrderStatus.COMPLETED.name, enums.OrderStatus.CANCELLED.name):
            raise exceptions.InvalidOrderOperation("Cannot cancel a completed or already cancelled order")
        self._status = enums.OrderStatus.CANCELLED.name
        self.update_modified_date()
    
    def complete(self):
        if self._status != enums.OrderStatus.SHIPPED.name:
            raise exceptions.InvalidOrderOperation("Only shipped order can be completed")
        self._status = enums.OrderStatus.COMPLETED.name
        self.update_modified_date()

    @property
    def is_fully_paid(self):
        return self.get_total_paid >= self.get_total_amount()
    
    def apply_payment(self, payment: value_objects.Payment):
        self._payments.append(payment)
        if self.is_fully_paid:
            self._status = enums.OrderStatus.PAID.name

    def apply_coupon(self, coupon_code: str, coupon_service):
        #TODO: need to validate coupon_code if not expired ?? expired_date & usage_limit
        coupon = coupon_service.validate(coupon_code)
        if coupon:
            self._coupon_codes.append(coupon_code)
        else:
            raise ValueError("Invalid or expired coupon code")

    def set_shipping_policy(self, shipping_policy):
        if self._shipping_policy:
            raise ValueError("Vendor Shipping policy already set.")
        self._shipping_policy = shipping_policy

    def get_total_amount(self):
        return sum(line.total_price for line in self.line_items)

    def get_total_paid(self):
        return sum(payment.get_amount() for payment in self.payments)

    def get_total_weight(self) -> Decimal:
        return sum(item.get_total_weight() for item in self.get_line_items())

    def get_combined_dimensions(self) -> Tuple[int, int, int]:
        total_length = sum(item.get_dimensions()[0] for item in self.get_line_items())
        max_width = max(item.get_dimensions()[1] for item in self.get_line_items())
        max_height = max(item.get_dimensions()[2] for item in self.get_line_items())
        return total_length, max_width, max_height

    def get_shipping_options(self, order: Order) -> List[dict]:
        return self._shipping_policy.get_shipping_options(order)

    def get_line_items(self):
        return self.line_items

    def get_customer_coupons(self):
        return self._coupon_codes

    

