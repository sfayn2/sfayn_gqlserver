from __future__ import annotations
import uuid
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Tuple
from dataclasses import dataclass, field
from ddd.order_management.domain import value_objects, enums, exceptions

@dataclass
class LineItem:
    _id: uuid.uuid4
    _product_sku: str
    _product_name: str
    _product_category: str
    _options: dict
    _product_price: value_objects.Money
    _order_quantity: int
    package: value_objects.Package
    _is_free_gift: bool = False
    _is_taxable: bool = True

    def set_options(self, options):
        self._options = options

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

    def get_product_category(self):
        return self._product_category

    def get_order_quantity(self):
        return self._order_quantity

    def get_product_sku(self):
        return self._product_sku

    def get_id(self):
        return self._id

    def get_options(self):
        return self._options

    def get_product_price(self):
        return self._product_price

    @property
    def is_free_gift(self):
        return self._is_free_gift

    @property
    def is_taxable(self):
        return self._is_taxable



@dataclass
class Order:
    _order_id: str
    destination: value_objects.Address
    line_items: List[LineItem]
    customer_details: value_objects.CustomerDetails
    shipping_details: value_objects.ShippingDetails
    payment_details: value_objects.PaymentDetails
    _cancellation_reason: str
    _total_discounts_fee: value_objects.Money
    _offer_details: List[str]
    _tax_details: List[str]
    _tax_amount: Optional[value_objects.Money]
    _total_amount: value_objects.Money
    _final_amount: value_objects.Money
    _shipping_reference: Optional[str]
    _currency: str
    _coupon_codes: Optional[List[str]] = field(default_factory=list, init=False)
    _status: enums.OrderStatus = enums.OrderStatus.DRAFT.name

    _date_created: datetime = field(default_factory=datetime.now)
    _date_modified: Optional[datetime] = None

    def update_modified_date(self):
        self._date_modified = datetime.now()

    def add_line_item(self, line_item: value_objects.OrderLine) -> None:
        if not line_item:
            raise ValueError("Please provide line item to add.")
        self.line_items.add(line_item)

    def remove_line_item(self, line_item: value_objects.OrderLine) -> None:
        if not line_item:
            raise ValueError("Please provide line item to remove.")
        self.line_items.remove(line_item)

    def update_line_item_details(self, line_item: value_objects.OrderLine):
        #use to update specific item quantity or other item info
        if not line_item:
            raise ValueError("Please provide line item to update details.")
        self.line_items.remove(line_item)
        self.line_items.add(line_item)

    def place_order(self):
        if not self.line_items:
            raise exceptions.InvalidOrderOperation("Order must have at least one line item.")
        if not self.shipping_details:
            raise exceptions.InvalidOrderOperation("Order must have a selected Shipping method")
        self._status = enums.OrderStatus.PENDING.name
        self.update_modified_date()

    def confirm_order(self, payment_verified: bool):
        if self.status != enums.OrderStatus.PENDING.name:
            raise exceptions.InvalidOrderOperation("Only pending orders can be confirmed.")
        if not payment_verified:
            raise exceptions.InvalidOrderOperation("Order cannot be confirmed without verified payment.")

        self._status = enums.OrderStatus.CONFIRMED.name
        self.update_modified_date()

    def update_payment_details(self, payment_details: value_objects.PaymentDetails):
        self.payment_details = payment_details

    def update_customer_details(self, customer_details: value_objects.CustomerDetails):
        self.customer_details = customer_details

    def mark_as_shipped(self):
        if self._status != enums.OrderStatus.CONFIRMED.name:
            raise exceptions.InvalidOrderOperation("Only confirm order can mark as shipped.")
        self._status = enums.OrderStatus.SHIPPED.name
        self.update_modified_date()

    def cancel_order(self, cancellation_reason: str):
        if not self._status in (enums.OrderStatus.PENDING.name, enums.OrderStatus.CONFIRMED.name):
            raise exceptions.InvalidOrderOperation("Cannot cancel a completed or already cancelled order or shipped order")
        self._status = enums.OrderStatus.CANCELLED.name
        self._cancellation_reason = cancellation_reason
        self.update_modified_date()
    
    def mark_as_completed(self):
        if self._status != enums.OrderStatus.SHIPPED.name:
            raise exceptions.InvalidOrderOperation("Only shipped order can mark as completed.")

        if self.payment_details.method == enums.PaymentMethod.COD and not self.payment_details:
            raise exceptions.InvalidOrderOperation("Cannot mark as completed with outstanding payments.")

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

    #def apply_offers(self, offer_service: offer_service.OfferStrategyService):
    #    if not self.shipping_details:
    #        raise exceptions.InvalidOrderOperation("Only when shipping option is selected.")
    #    offer_service.apply_offers(self)

    #def apply_taxes(self, tax_service: tax_service.TaxStrategyService):
    #    tax_service.apply_taxes(self)

    def apply_coupon(self, coupon_code: str):
        self._coupon_codes.append(coupon_code)

    def remove_coupon(self, coupon_code: str):
        self._coupon_codes.remove(coupon_code)
    
    def update_shipping_details(self, shipping_details: value_objects.ShippingDetails):
        self.shipping_details = shipping_details
    
    def select_shipping_option(self, shipping_option: enums.ShippingMethod, shipping_options: List[dict]):
        for ship_opt in shipping_options:
            if ship_opt.name == shipping_option:
                self.update_shipping_details(value_objects.ShippingDetails(
                        method=ship_opt.name,
                        delivery_time=ship_opt.delivery_time,
                        cost=ship_opt.cost,
                        orig_cost=ship_opt.cost
                    )
                )
                return
        raise ValueError(f"Shipping option not supported: {shipping_option}")

    def calculate_total_amount(self):
        self._total_amount = value_objects.Money(
            amount=sum(line.total_price for line in self.line_items),
            currency=self.get_currency()
        )

    def update_total_discounts_fee(self, total_discounts: value_objects.Money):
        self._total_discounts_fee = total_discounts

    def reset_values(self):
        #reset offers free shipping + discounts + free gifts
        self.update_shipping_details(
                self.shipping_details.reset_cost()
            )
        self.calculate_total_amount()
        self.update_total_discounts_fee(
                self.get_total_discounts_fee.reset_amount()
            )
        #TODO: reset free gifts??

    def calculate_final_amount(self):
        #make sure to call apply_offers & apply_taxes
        self._final_amount = (
                self.get_total_amount() - self.get_total_discounts_fee()
            ) + self.tax_details.tax_amount + self.shipping_details.cost

    def get_total_amount(self) -> value_objects.Money:
        return self._total_amount

    def get_total_discounts_fee(self) -> value_objects.Money:
        return self._total_discounts_fee

    def get_total_weight(self) -> Decimal:
        return sum(item.get_total_weight() for item in self.line_items)

    def get_combined_dimensions(self) -> Tuple[int, int, int]:
        total_length = sum(item.package.dimensions[0] for item in self.line_items)
        max_width = max(item.package.dimensions[1] for item in self.line_items)
        max_height = max(item.package.dimensions[2] for item in self.line_items)
        return total_length, max_width, max_height

    def get_customer_coupons(self) -> List[str]:
        return self._coupon_codes

    def get_currency(self) -> str:
        return self._currency

    def get_tax_details(self) -> str:
        return self._tax_details

    def get_tax_amount(self) -> value_objects.Money:
        return self._tax_amount

    def get_final_amount(self) -> value_objects.Money:
        return self._final_amount

    def get_order_id(self) -> str:
        return self._order_id

    def get_date_created(self) -> datetime:
        return self._date_created

    def get_date_modified(self) -> datetime:
        return self._date_modified




