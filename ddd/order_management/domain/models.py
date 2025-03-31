from __future__ import annotations
import uuid
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Tuple
from dataclasses import dataclass, field
from ddd.order_management.domain import value_objects, enums, exceptions, events
from ddd.order_management.domain.services import offer_service, tax_service

@dataclass
class LineItem:
    product_sku: str
    product_name: str
    product_price: value_objects.Money
    order_quantity: int
    vendor: value_objects.VendorDetails
    #vendor_name: str
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
    customer_details: value_objects.CustomerDetails
    order_status: enums.OrderStatus
    shipping_details: value_objects.ShippingDetails
    line_items: List[LineItem] = None
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
    _events: List[events.DomainEvent] = field(default_factory=list, init=False)

    def _validate_line_item(self, line_item: LineItem):
        if self.currency != line_item.product_price.currency:
            raise exceptions.InvalidOrderOperation("Currency mismatch between order and line item.")

        if self.vendor_name and self.vendor_name != line_item.vendor.name:
            raise exceptions.InvalidOrderOperation("Vendor mismatch between order and line item.")


    def update_modified_date(self):
        self.date_modified = datetime.now()

    def add_line_item(self, line_item: LineItem) -> None:
        if not line_item:
            raise ValueError("Please provide line item to add.")
        if self.order_status != enums.OrderStatus.DRAFT:
            raise exceptions.InvalidOrderOperation("Only draft order can add line item.")
        if line_item.is_free_gift and line_item.product_price.amount > 0:
            raise exceptions.InvalidOrderOperation("Free gifts must have a price of zero.")

        self._validate_line_item(line_item)

        self.line_items.add(line_item)
        self._update_totals()

    def remove_line_item(self, line_item: LineItem) -> None:
        if not line_item:
            raise ValueError("Line item does not exists in the order.")
        if self.order_status != enums.OrderStatus.DRAFT:
            raise exceptions.InvalidOrderOperation("Only draft order can remove line items.")
        self.line_items.remove(line_item)
        self._update_totals()

    def update_line_items(self, line_items: List[LineItem]) -> None:
        if not line_items:
            raise exceptions.InvalidOrderOperation("Line items cannot be none.")
        if self.order_status != enums.OrderStatus.DRAFT:
            raise exceptions.InvalidOrderOperation("Only draft order can update line items.")
        self.line_items =line_items
        self._update_totals()

    def update_shipping_details(self, shipping_details: value_objects.ShippingDetails) -> None:
        if not shipping_details:
            raise exceptions.InvalidOrderOperation("Shipping details must be provided.")
        if self.order_status != enums.OrderStatus.DRAFT:
            raise exceptions.InvalidOrderOperation("Only draft order can update shipping details.")
        self.shipping_details = shipping_details
        self.update_modified_date()

    def update_order_quantity(self, product_sku: str, new_quantity: int):
        if self.order_status != enums.OrderStatus.DRAFT:
            raise exceptions.InvalidOrderOperation("Only draft order can update order quantity.")
        for line_item in self.line_items:
            if line_item.product_sku == product_sku:
                line_item.update_order_quantity(new_quantity)
                self._update_totals()
                return
        raise exceptions.InvalidOrderOperation(f"Product w Sku {product_sku} not found in the order.")

    def raise_event(self, event: events.DomainEvent):
        self._events.append(event)


    def place_order(self):
        if self.order_status != enums.OrderStatus.DRAFT:
            raise exceptions.InvalidOrderOperation("Only draft order can be place order.")
        if not self.line_items:
            raise exceptions.InvalidOrderOperation("Cannot place an order without line items.")
        if not self.customer_details:
            raise exceptions.InvalidOrderOperation("Customer details must be provided.")
        if any(item.product_price.currency != self.line_items[0].product_price.currency for item in self.line_items):
            raise exceptions.InvalidOrderOperation("All line items must have the same currency.")

        if len(set(item.vendor.name for item in self.line_items)) > 1:
            raise exceptions.InvalidOrderOperation("All line items must belong to the same vendor.")

        if not self.shipping_details:
            raise exceptions.InvalidOrderOperation("Order must have a selected shipping option")

        self.order_status = enums.OrderStatus.PENDING
        self.update_modified_date()

        event = events.OrderPlaced(
            order_id=self.order_id,
            order_status=self.order_status,
        )

        self.raise_event(event)

    def confirm_order(self, payment_verified: bool):
        if self.order_status != enums.OrderStatus.PENDING:
            raise exceptions.InvalidOrderOperation("Only pending orders can be confirmed.")
        if not payment_verified:
            raise exceptions.InvalidOrderOperation("Order cannot be confirmed without verified payment.")

        self.order_status = enums.OrderStatus.CONFIRMED
        self.update_modified_date()

        event = events.OrderConfirmed(
            order_id=self.order_id,
            order_status=self.order_status,
        )

        self.raise_event(event)

    def apply_offers(self, offer_service: offer_service.OfferStrategyService):
        if self.order_status != enums.OrderStatus.DRAFT:
            raise exceptions.InvalidTaxOperation("Only draft order can apply offers (Free shipping, Free gifts, etc)")
        if self.offer_details:
            raise exceptions.InvalidTaxOperation("Offers have already been applied.")
        if not self.shipping_details:
            raise exceptions.InvalidOfferOperation("Only when shipping option is selected.")
        offer_service.apply_offers(self)

    def apply_taxes(self, tax_strategies: List[tax_service.TaxStrategy]):
        if self.order_status != enums.OrderStatus.DRAFT:
            raise exceptions.InvalidTaxOperation("Only draft order can calculate taxes.")
        if not self.destination:
            raise exceptions.InvalidTaxOperation("Shipping address is required for tax calculation.")
        if self.tax_details:
            raise exceptions.InvalidTaxOperation("Taxes have already been applied.")
        if not any(item.is_taxable for item in self.line_items):
            return #Skip tax if no taxable items
        if self.sub_total.amount == 0:
            raise #Skip tax for zero subtotal

        tax_amount = value_objects.Money.default()
        tax_details = []

        for tax_strategy in tax_strategies:
            tax_results = tax_strategy.apply(self)
            if tax_results:
                tax_details.append(tax_results.desc)
                tax_amount.add(tax_results.amount)

        if tax_amount.amount < Decimal("0"):
            raise exceptions.InvalidTaxOperation("Tax amount cannot be negative.")

        self.tax_amount = tax_amount
        self.tax_details = tax_details


    def update_payment_details(self, payment_details: value_objects.PaymentDetails):
        if not payment_details:
            raise exceptions.InvalidOrderOperation("Payment details cannot be none.")
        if self.order_status != enums.OrderStatus.PENDING:
            raise exceptions.InvalidOrderOperation("Only pending order can update payment details.")
        self.payment_details = payment_details

    def mark_as_shipped(self):
        if self.order_status != enums.OrderStatus.CONFIRMED:
            raise exceptions.InvalidOrderOperation("Only confirm order can mark as shipped.")
        self.order_status = enums.OrderStatus.SHIPPED
        self.update_modified_date()

    def cancel_order(self, cancellation_reason: str):
        if not self.order_status in (enums.OrderStatus.PENDING, enums.OrderStatus.CONFIRMED):
            raise exceptions.InvalidOrderOperation("Cannot cancel a completed or already cancelled order or shipped order")
        self.order_status = enums.OrderStatus.CANCELLED
        self.cancellation_reason = cancellation_reason
        self.update_modified_date()
    
    def mark_as_completed(self):
        if self.order_status != enums.OrderStatus.SHIPPED:
            raise exceptions.InvalidOrderOperation("Only shipped order can mark as completed.")

        if self.payment_details.method == enums.PaymentMethod.COD and not self.payment_details:
            raise exceptions.InvalidOrderOperation("Cannot mark as completed with outstanding payments.")

        self.order_status = enums.OrderStatus.COMPLETED
        self.update_modified_date()

    def add_shipping_tracking_reference(self, shipping_reference: str):
        if self.order_status != enums.OrderStatus.SHIPPED:
            raise exceptions.InvalidOrderOperation("Only shipped order can add tracking reference.")
        self.shipping_reference = shipping_reference

    def update_offer_details(self, offer_details: List[str]):
        if self.order_status != enums.OrderStatus.DRAFT:
            raise exceptions.InvalidTaxOperation("Only draft order can update offer details.")
        self.offer_details = offer_details

    def apply_coupon(self, coupon: value_objects.Coupon):
        if not coupon:
            raise exceptions.InvalidOrderOperation("Coupon cannot be none.")
        if self.order_status != enums.OrderStatus.DRAFT:
            raise exceptions.InvalidTaxOperation("Only draft order can apply coupon.")
        self.coupons.append(coupon)

    def remove_coupon(self, coupon: value_objects.Coupon):
        if not coupon:
            raise exceptions.InvalidOrderOperation("Coupon cannot be none.")
        if self.order_status != enums.OrderStatus.DRAFT:
            raise exceptions.InvalidTaxOperation("Only draft order can remove coupon.")
        self.coupons.remove(coupon)

    def update_destination(self, destination: value_objects.Address):
        if not destination:
            raise exceptions.InvalidOrderOperation("Destination cannot be none.")
        if self.order_status != enums.OrderStatus.DRAFT:
            raise exceptions.InvalidTaxOperation("Only draft order can update destination.")
        self.destination = destination
        self.update_modified_date()
    
    def select_shipping_option(self, shipping_option: value_objects.ShippingDetails, shipping_options: List[value_objects.ShippingDetails]):
        if self.order_status != enums.OrderStatus.DRAFT:
            raise exceptions.InvalidTaxOperation("Only draft order can select shipping option.")
        for option in shipping_options:
            if option == shipping_option:
                self.update_shipping_details(option)
                return
        raise exceptions.InvalidOrderOperation(f"Shipping option not supported: {shipping_option}")

    def _update_totals(self):
        self.total_amount = value_objects.Money(
            amount=sum(line.total_price.amount for line in self.line_items),
            currency=self.currency
        )

    def update_total_discounts_fee(self, total_discounts: value_objects.Money):
        if self.order_status != enums.OrderStatus.DRAFT:
            raise exceptions.InvalidTaxOperation("Only draft order can update total discount fees.")
        self.total_discounts_fee = total_discounts

    #def reset_order_details(self):
    #    #reset offers free shipping + discounts + free gifts
    #    self.update_shipping_details(
    #            self.shipping_details.reset_cost()
    #        )
    #    self.update_total_discounts_fee(
    #            self.total_discounts_fee.reset_amount()
    #        )
    #    self.update_tax_amount(
    #        value_objects.Money(
    #            amount=0,
    #            currency=self.currency
    #        )
    #    )
    #    self._update_totals()
    #    #TODO: reset free gifts??

    @property
    def sub_total(self):
        return self.total_amount.subtract(self.total_discounts_fee).add(self.shipping_details.cost if self.shipping_details else value_objects.Money(0, self.currency))

    def calculate_final_amount(self):
        if self.order_status != enums.OrderStatus.DRAFT:
            raise exceptions.InvalidTaxOperation("Only draft order can calculate final amount.")

        #TODO revisit calculation
        self.final_amount = self.sub_total.add(self.tax_amount)

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
        return self.line_items[0].vendor.name

    @property
    def vendor_country(self) -> str:
        #assuming invariant
        if not self.line_items[0].vendor.country:
            raise exceptions.InvalidOrderOperation("Vendor country is missing, its crucial in determining domestic shipment.")
        return self.line_items[0].vendor.country





