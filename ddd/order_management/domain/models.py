from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Tuple
from dataclasses import dataclass, field
from order_management.domain import value_objects, enums, exceptions
from order_management.domain.services import tax_calculation_policies, shipping_option_policies, offer_policies


@dataclass
class Order:
    _order_id: str
    customer: value_objects.Customer
    destination: value_objects.Address
    line_items: List[value_objects.LineItem]
    _status: enums.OrderStatus = enums.OrderStatus.DRAFT.name
    _shipping_reference: str
    _total_amount: value_objects.Money
    _total_tax: value_objects.Money
    _tax_desc: str
    _currency: str
    _coupon_codes: Optional[List[str]] = field(default_factory=list, init=False)
    _payments: List[value_objects.Payment] = field(default_factory=list)
    _date_created: datetime = field(default_factory=datetime.now)
    _date_modified: Optional[datetime] = None

    VALID_STATUS_TRANSITIONS = {
        enums.OrderStatus.DRAFT.name : [enums.OrderStatus.PENDING.name],
        enums.OrderStatus.PENDING.name : [enums.OrderStatus.CONFIRMED.name],
        enums.OrderStatus.CONFIRMED.name : [enums.OrderStatus.SHIPPED.name, enums.OrderStatus.CANCELLED.name],
        enums.OrderStatus.SHIPPED.name : [enums.OrderStatus.COMPLETED.name, enums.OrderStatus.CANCELLED.name],
        enums.OrderStatus.COMPLETED.name : []
    }

    def update_modified_date(self):
        self._date_modified = datetime.now()

    def change_state(self, new_status: enums.OrderStatus):
        if new_status not in self.VALID_STATUS_TRANSITIONS[self._status]:
            raise exceptions.InvalidStatusTransitionError(f"Cannot transition from {self._status} to {new_status}")
        self._status = new_status
        self.update_modified_date()

    def add_line_item(self, line_item: value_objects.OrderLine) -> None:
        if not line_item:
            raise "No item to add in order!"
        self.line_items.add(line_item)

    def checkout(self, offer_policy: offer_policies.OfferPolicy):
        discounts_amount, free_gifts, free_shipping = offer_policy.get_offers()
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
        if not self._payment or self._payment.get_amount() < self.get_total_amount().get_amount():
            raise exceptions.InvalidOrderOperation("Order cannot be confirmed without a full payment.")
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

    def calculate_tax(self, tax_service: tax_calculation_policies.TaxCalculationPolicy) -> value_objects.Money:
        total_tax, tax_desc = tax_service.calculate_tax(self)
        self._total_tax = value_objects.Money(
            _amount=total_tax,
            _currency=self.get_currency()
        )
        self._tax_desc = tax_desc

    @property
    def is_fully_paid(self):
        return self.get_total_paid.get_amount() >= self.get_total_amount().get_amount()
    
    def apply_payment(self, payment: value_objects.Payment):
        self._payments.append(payment)
        if self.is_fully_paid:
            self._status = enums.OrderStatus.PAID.name

    def apply_coupon(self, coupon_code: str):
        #right now validation is handled in offer policy
        self._coupon_codes.append(coupon_code)

    def get_total_amount(self) -> value_objects.Money:
        return value_objects.Money(
            _amount=sum(line.total_price for line in self.line_items),
            _currency=self.get_currency()
        )

    def get_total_paid(self) -> value_objects.Money:
        return value_objects.Money(
            _amount=sum(payment.get_amount() for payment in self.payments),
            _currency=self.get_currency()
        )

    def get_total_weight(self) -> Decimal:
        return sum(item.get_total_weight() for item in self.get_line_items())

    def get_combined_dimensions(self) -> Tuple[int, int, int]:
        total_length = sum(item.get_dimensions()[0] for item in self.get_line_items())
        max_width = max(item.get_dimensions()[1] for item in self.get_line_items())
        max_height = max(item.get_dimensions()[2] for item in self.get_line_items())
        return total_length, max_width, max_height

    def get_shipping_options(self, order: Order, shipping_option_policy: shipping_option_policies.ShippingOptionPolicy) -> List[dict]:
        return shipping_option_policy.get_shipping_options(order)

    def get_line_items(self):
        return self.line_items

    def get_customer_coupons(self):
        return self._coupon_codes

    def get_total_tax(self):
        return self._total_tax

    def get_currency(self):
        return self._currency

    

