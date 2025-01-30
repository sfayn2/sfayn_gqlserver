from __future__ import annotations
import uuid
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Tuple
from dataclasses import dataclass, field
from ddd.order_management.domain import value_objects, enums, exceptions

@dataclass
class LineItem:
    product_sku: str
    product_name: str
    product_price: value_objects.Money
    order_quantity: int
    vendor_name: str
    product_category: str
    options: dict
    package: value_objects.Package
    is_free_gift: bool = False
    is_taxable: bool = True

    
    def __post_init__(self):

        if self.order_quantity <= 0:
            raise ValueError("Order quantity must be greater than zero.")

        if self.product_price.amount < 0:
            raise ValueError("Product price cannot be negative.")

        if any(d <= 0 for d in self.package.dimensions):
            raise ValueError("Package dimensions must be positive value.")

        #TODO? really?
        if self.is_free_gift and self.is_taxable:
            raise ValueError("Free gift is not taxable.")

    def update_order_quantity(self, new_quantity: int):
        if new_quantity <= 0:
            raise ValueError("Order quantity must be greater than zero.")
        self.order_quantity = new_quantity

    @property
    def total_price(self) -> value_objects.Money:
        return self.product_price.multiply(self.order_quantity)

    @property
    def total_weight(self) -> Decimal:
        return self.package.weight * self.order_quantity

@dataclass
class Order:
    order_id: str
    date_created: datetime
    destination: value_objects.Address
    line_items: List[LineItem]
    customer_details: value_objects.CustomerDetails
    order_status: enums.OrderStatus
    shipping_details: Optional[value_objects.ShippingDetails] = None
    payment_details: Optional[value_objects.PaymentDetails] = None
    cancellation_reason: Optional[str] = None
    shipping_reference: Optional[str] = None
    offer_details: Optional[List[str]] = field(default_factory=list)
    tax_details: Optional[List[str]] = field(default_factory=list)
    coupons: Optional[List[value_objects.Coupon]] = field(default_factory=list)
    total_discounts_fee: value_objects.Money = value_objects.Money.default()
    tax_amount: value_objects.Money = value_objects.Money.default()
    total_amount: value_objects.Money = value_objects.Money.default()
    final_amount: value_objects.Money = value_objects.Money.default()
    date_modified: Optional[datetime] = None


    @classmethod
    def create_draft_order(cls, customer_details: value_objects.CustomerDetails, 
                     destination: value_objects.Address, line_items: List[LineItem]):

        if not customer_details:
            raise exceptions.InvalidOrderOperation("Customer details must be provided.")

        if not line_items:
            raise exceptions.InvalidOrderOperation("Order must have at least one line item.")
        
        if any(item.product_price.currency != line_items[0].product_price.currency for item in line_items):
            raise exceptions.InvalidOrderOperation("All line items must have the same currency.")

        if len(set(item.vendor_name for item in line_items)) > 1:
            raise exceptions.InvalidOrderOperation("All line items must belong to the same vendor.")

        return cls(
            order_id=f"ORD-{uuid.uuid4().hex[:8].upper()}",
            order_status=enums.OrderStatus.DRAFT.value,
            date_created=datetime.now(),
            customer_details=customer_details,
            line_items=line_items,
            destination=destination
        )

    def _validate_line_item(self, line_item: LineItem):
        if self.currency != line_item.product_price.currency:
            raise exceptions.InvalidOrderOperation("Currency mismatch between order and line item.")

        if self.vendor_name and self.vendor_name != line_item.vendor_name:
            raise exceptions.InvalidOrderOperation("Vendor mismatch between order and line item.")


    def update_modified_date(self):
        self.date_modified = datetime.now()

    def add_line_item(self, line_item: LineItem) -> None:
        if not line_item:
            raise ValueError("Please provide line item to add.")

        self._validate_line_item(line_item)

        self.line_items.add(line_item)
        self._update_totals()

    def remove_line_item(self, line_item: LineItem) -> None:
        if not line_item:
            raise ValueError("Line item does not exists in the order.")
        self.line_items.remove(line_item)
        self._update_totals()

    def update_line_items(self, line_items: List[LineItem]) -> None:
        if not line_items:
            raise exceptions.InvalidOrderOperation("Line items cannot be none.")
        self.line_items =line_items
        self._update_totals()

    def update_order_quantity(self, product_sku: str, new_quantity: int):
        for line_item in self.line_items:
            if line_item.product_sku == product_sku:
                line_item.update_order_quantity(new_quantity)
                self._update_totals()
                return
        raise exceptions.InvalidOrderOperation(f"Product w Sku {product_sku} not found in the order.")

    def place_order(self):
        if not self.line_items:
            raise exceptions.InvalidOrderOperation("Cannot place an order without line items.")
        if not self.shipping_details:
            raise exceptions.InvalidOrderOperation("Order must have a selected Shipping method")
        self.order_status = enums.OrderStatus.PENDING.value
        self.update_modified_date()

    def confirm_order(self, payment_verified: bool):
        if self.order_status != enums.OrderStatus.PENDING.value:
            raise exceptions.InvalidOrderOperation("Only pending orders can be confirmed.")
        if not payment_verified:
            raise exceptions.InvalidOrderOperation("Order cannot be confirmed without verified payment.")

        self.order_status = enums.OrderStatus.CONFIRMED.value
        self.update_modified_date()

    def update_payment_details(self, payment_details: value_objects.PaymentDetails):
        if not payment_details:
            raise exceptions.InvalidOrderOperation("Payment details cannot be none.")
        self.payment_details = payment_details

    def update_customer_details(self, customer_details: value_objects.CustomerDetails):
        if not customer_details:
            raise exceptions.InvalidOrderOperation("Customer details cannot be none.")
        self.customer_details = customer_details

    def mark_as_shipped(self):
        if self.order_status != enums.OrderStatus.CONFIRMED.value:
            raise exceptions.InvalidOrderOperation("Only confirm order can mark as shipped.")
        self.order_status = enums.OrderStatus.SHIPPED.value
        self.update_modified_date()

    def cancel_order(self, cancellation_reason: str):
        if not self.order_status in (enums.OrderStatus.PENDING.value, enums.OrderStatus.CONFIRMED.value):
            raise exceptions.InvalidOrderOperation("Cannot cancel a completed or already cancelled order or shipped order")
        self.order_status = enums.OrderStatus.CANCELLED.value
        self.cancellation_reason = cancellation_reason
        self.update_modified_date()
    
    def mark_as_completed(self):
        if self.order_status != enums.OrderStatus.SHIPPED.value:
            raise exceptions.InvalidOrderOperation("Only shipped order can mark as completed.")

        if self.payment_details.method == enums.PaymentMethod.COD and not self.payment_details:
            raise exceptions.InvalidOrderOperation("Cannot mark as completed with outstanding payments.")

        self.order_status = enums.OrderStatus.COMPLETED.value
        self.update_modified_date()

    def add_shipping_tracking_reference(self, shipping_reference: str):
        self.shipping_reference = shipping_reference

    def update_tax_amount(self, amount: value_objects.Money):
        self.tax_amount = amount
    
    def update_offer_details(self, offer_details: List[str]):
        self.offer_details = offer_details

    def update_tax_details(self, tax_details: List[str]):
        self.tax_details = tax_details

    def apply_coupon(self, coupon_code: value_objects.Coupon):
        if not coupon_code:
            raise exceptions.InvalidOrderOperation("Coupon code cannot be none.")
        self.coupons.append(coupon_code)

    def remove_coupon(self, coupon_code: value_objects.Coupon):
        if not coupon_code:
            raise exceptions.InvalidOrderOperation("Coupon code cannot be none.")
        self.coupons.remove(coupon_code)

    def update_destination(self, destination: value_objects.Address):
        if not destination:
            raise exceptions.InvalidOrderOperation("Destination cannot be none.")
        self.destination = destination
        self.update_modified_date()
    
    def update_shipping_details(self, shipping_details: value_objects.ShippingDetails):
        if not shipping_details:
            raise exceptions.InvalidOrderOperation("Shipping details cannot be none.")
        self.shipping_details = shipping_details
        self.update_modified_date()
    
    def select_shipping_option(self, shipping_option: enums.ShippingMethod, shipping_options: List[dict]):
        for option in shipping_options:
            if option.get("name") == shipping_option:
                self.update_shipping_details(value_objects.ShippingDetails(
                        method=option.get("name"),
                        delivery_time=option.get("delivery_time"),
                        cost=option.get("cost")
                    )
                )
                return
        raise exceptions.InvalidOrderOperation(f"Shipping option not supported: {shipping_option}")

    def _update_totals(self):
        self.total_amount = value_objects.Money(
            amount=sum(line.total_price.amount for line in self.line_items),
            currency=self.currency
        )

    def update_total_discounts_fee(self, total_discounts: value_objects.Money):
        self.total_discounts_fee = total_discounts

    def reset_order_details(self):
        #reset offers free shipping + discounts + free gifts
        self.update_shipping_details(
                self.shipping_details.reset_cost()
            )
        self.update_total_discounts_fee(
                self.total_discounts_fee.reset_amount()
            )
        self.update_tax_amount(
            value_objects.Money(
                amount=0,
                currency=self.currency
            )
        )
        self._update_totals()
        #TODO: reset free gifts??

    def calculate_final_amount(self):
        if not self.tax_details:
            raise exceptions.InvalidOrderOperation("No tax calculation has been applied.")

        #TODO revisit calculation
        self.final_amount = (
                self.total_amount.subtract(self.total_discounts_fee).add(self.shipping_details.cost if self.shipping_details else value_objects.Money(0, self.currency))
        ).add(self.tax_amount)

    @property
    def total_weight(self) -> Decimal:
        return sum(item.total_weight for item in self.line_items)

    @property
    def combined_dimensions(self) -> Tuple[int, int, int]:
        total_length = sum(item.package.dimensions[0] for item in self.line_items)
        max_width = max(item.package.dimensions[1] for item in self.line_items)
        max_height = max(item.package.dimensions[2] for item in self.line_items)
        return total_length, max_width, max_height

    @property
    def currency(self) -> str:
        #assuming invariants
        return self.line_items[0].product_price.currency

    @property
    def vendor_name(self) -> str:
        #assuming invariant
        return self.line_items[0].vendor_name





