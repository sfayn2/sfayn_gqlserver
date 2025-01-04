from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Tuple
from dataclasses import dataclass, field
from ddd.order_management.domain.services import offer_handler_service, offer_handler_service, shipping_option_handler
from order_management.domain import value_objects, enums, exceptions
from order_management.domain.services import  (tax_handler)

@dataclass
class LineItem:
    _product_sku: str
    _product_name: str
    _options: str
    _product_price: value_objects.Money
    _order_quantity: int
    _is_free_gift: bool = False
    _is_taxable: bool = True
    _package: value_objects.Package

    def add(self, quantity: int):
        if quantity < 0:
            raise ValueError("Value must be greater than current quantity.")

        self._order_quantity += quantity

    def subtract(self, quantity: int):
        if quantity < 0 or quantity > self._order_quantity:
            raise ValueError("Value must be less than or equal to the current quantity.")

        self._order_quantity -= quantity

    def get_total_price(self) -> value_objects.Money:
        return (self._product_price * self._order_quantity)

    def get_total_weight(self) -> Decimal:
        return self._weight * self._order_quantity

    def get_product_name(self):
        return self._product_name

    def get_order_quantity(self):
        return self._order_quantity



@dataclass
class Order:
    _order_id: str
    customer: value_objects.Customer
    destination: value_objects.Address
    line_items: List[LineItem]
    shipping_details: value_objects.ShippingDetails
    _status: enums.OrderStatus = enums.OrderStatus.DRAFT.name
    _total_discounts_fee: value_objects.Money
    _offer_details: List[str]
    _tax_details: List[str]
    _tax_amount: value_objects.Money
    _total_amount: value_objects.Money
    _final_amount: value_objects.Money
    _total_payments: value_objects.Money
    _shipping_reference: str
    _currency: str
    _coupon_codes: Optional[List[str]] = field(default_factory=list, init=False)
    _payments: List[value_objects.Payment] = field(default_factory=list)

    _applied_offers: List[offer_handler_service.OfferHandler] = field(default_factory=list, init=False)

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
            raise ValueError("Please provide line item to add.")
        self.line_items.add(line_item)
        self.calculate_final_amount()

    def remove_line_item(self, line_item: value_objects.OrderLine) -> None:
        if not line_item:
            raise ValueError("Please provide line item to remove.")
        self.line_items.remove(line_item)
        self.calculate_final_amount()

    def place(self):
        if not self.line_items:
            raise exceptions.InvalidOrderOperation("Order must have at least one line item.")
        if not self.shipping_details:
            raise exceptions.InvalidOrderOperation("Order must have a selected Shipping method")
        self._status = enums.OrderStatus.PENDING.name
        self.update_modified_date()

    def confirm(self):
        if self.status != enums.OrderStatus.PENDING.name:
            raise exceptions.InvalidOrderOperation("Only pending orders can be confirmed.")
        if not self._payment or self._payment.paid_amount < self.get_total_amount():
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

    def add_shipping_tracking_reference(self, shipping_reference: str):
        self._shipping_reference = shipping_reference

    def update_tax_amount(self, amount: value_objects.Money):
        self._tax_amount = amount
    
    def update_offer_details(self, offer_details: List[str]):
        self._offer_details = offer_details

    def update_tax_details(self, tax_details: List[str]):
        self._tax_details = tax_details

    def apply_offers(self, offer_service: offer_handler_service.OfferHandlerService):
        offer_service.apply_offers(self)

    def apply_taxes(self, tax_service: tax_handler.TaxHandlerMain):
        tax_service.apply_taxes(self)

    @property
    def is_fully_paid(self):
        return self.get_total_payments() >= self.get_total_amount()
    
    def apply_payment(self, payment: value_objects.Payment):
        self._payments.append(payment)
        if self.is_fully_paid:
            self._status = enums.OrderStatus.PAID.name

    def apply_coupon(self, coupon_code: str, offer_service: offer_handler_service.OfferHandlerService):
        self._coupon_codes.append(coupon_code)
        offer_service.apply_offers(self)

        #always recalculate?
        self.calculate_final_amount()

    def remove_coupon(self, coupon_code: str, offer_service: offer_handler_service.OfferHandlerService):
        self._coupon_codes.remove(coupon_code)
        offer_service.apply_offers(self)

        #always recalculate?
        self.calculate_final_amount()
    
    def update_shipping_details(self, shipping_details: value_objects.ShippingDetails):
        self.shipping_details = shipping_details
    
    def select_shipping_option(self, shipping_option: enums.ShippingMethod, shipping_options ):
        for ship_opt in shipping_options:
            if ship_opt.name == shipping_option:
                self.update_shipping_details(value_objects.ShippingDetails(
                        method=ship_opt.name,
                        delivery_time=ship_opt.delivery_time,
                        cost=ship_opt.cost
                    )
                )
                return
        raise ValueError(f"Shipping option not supported: {shipping_option}")

    def calculate_total_amount(self):
        self._total_amount = value_objects.Money(
            amount=sum(line.total_price for line in self.line_items),
            currency=self.get_currency()
        )

    def calculate_total_payments(self):
        self._total_payments = value_objects.Money(
            amount=sum(payment.paid_amount for payment in self.payments),
            currency=self.get_currency()
        )

    def update_total_discounts_fee(self, total_discounts: value_objects.Money):
        self._total_discounts_fee = total_discounts

    def calculate_final_amount(self):
        self.calculate_total_amount()
        #make sure to call apply_offers & apply_taxes
        self._final_amount = (
                self.get_total_amount() - self.get_total_discounts_fee()
            ) + self.tax_details.tax_amount + self.shipping_details.cost

    def get_shipping_options(self, shipping_option_service: shipping_option_handler.ShippingOptionHandlerMain) -> List[dict]:
        return shipping_option_service.get_shipping_options(self)

    def get_total_amount(self) -> value_objects.Money:
        return self._total_amount

    def get_total_payments(self) -> value_objects.Money:
        return self._total_payments

    def get_total_discounts_fee(self) -> value_objects.Money:
        return self._total_discounts_fee

    def get_total_weight(self) -> Decimal:
        return sum(item.get_total_weight() for item in self.line_items)

    def get_combined_dimensions(self) -> Tuple[int, int, int]:
        total_length = sum(item.get_dimensions()[0] for item in self.line_items)
        max_width = max(item.get_dimensions()[1] for item in self.line_items)
        max_height = max(item.get_dimensions()[2] for item in self.line_items)
        return total_length, max_width, max_height

    def get_customer_coupons(self):
        return self._coupon_codes

    def get_currency(self):
        return self._currency

    def get_tax_amount(self):
        return self._tax_amount

