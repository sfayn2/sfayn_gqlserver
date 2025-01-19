from __future__ import annotations
import uuid
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Tuple
from dataclasses import dataclass, field
from ddd.order_management.domain import value_objects, enums, exceptions

class LineItem:
    
    def __init__(self, 
                 product_sku: str, 
                 product_name: str, 
                 vendor_name: str,
                 product_category: str, 
                 options: dict, 
                 product_price: value_objects.Money, 
                 order_quantity: int, 
                 package: value_objects.Package,
                 is_free_gift: bool = False,
                 is_taxable: bool = True):

        if order_quantity <= 0:
            raise ValueError("Order quantity must be greater than zero.")

        if product_price.amount < 0:
            raise ValueError("Product price cannot be negative.")

        if any(d <= 0 for d in package.dimensions):
            raise ValueError("Package dimensions must be positive value.")

        #TODO? really?
        if is_free_gift and is_taxable:
            raise ValueError("Free gift is not taxable.")

        self._product_sku = product_sku
        self._product_name = product_name
        self._product_category = product_category
        self._options = options
        self._product_price = product_price
        self._order_quantity = order_quantity
        self._vendor_name = vendor_name
        self.package = package
        self._is_free_gift = is_free_gift
        self._is_taxable = is_taxable


    
    def set_options(self, options):
        self._options = options

    #def add(self, quantity: int):
    #    if quantity < 0:
    #        raise ValueError("Value must be greater than current quantity.")

    #    self._order_quantity += quantity

    #def subtract(self, quantity: int):
    #    if quantity < 0 or quantity > self.order_quantity:
    #        raise ValueError("Value must be less than or equal to the current quantity.")

    #    self._order_quantity -= quantity

    @property
    def total_price(self) -> value_objects.Money:
        return (self.product_price * self.order_quantity)

    @property
    def total_weight(self) -> Decimal:
        return self.package.weight * self.order_quantity

    @property
    def product_name(self):
        return self._product_name

    @property
    def product_category(self):
        return self._product_category

    @property
    def order_quantity(self):
        return self._order_quantity

    @property
    def product_sku(self):
        return self._product_sku

    @property
    def options(self):
        return self._options

    @property
    def product_price(self):
        return self._product_price

    @property
    def is_free_gift(self):
        return self._is_free_gift

    @property
    def is_taxable(self):
        return self._is_taxable

    @property
    def vendor_name(self):
        return self._vendor_name



class Order:

    def __init__(self,
                order_id: str,
                date_created: datetime, 
                destination: value_objects.Address,
                line_items: List[LineItem],
                customer_details: value_objects.CustomerDetails,
                shipping_details: Optional[value_objects.ShippingDetails] = None,
                payment_details: Optional[value_objects.PaymentDetails] = None,
                cancellation_reason: Optional[str] = None,
                total_discounts_fee: Optional[value_objects.Money] = None,
                offer_details: Optional[List[str]] = field(default_factory=list),
                tax_details: Optional[List[str]]= field(default_factory=list),
                tax_amount: Optional[value_objects.Money] = None,
                total_amount: Optional[value_objects.Money] = None,
                final_amount: Optional[value_objects.Money] = None,
                shipping_reference: Optional[str] = None,
                coupon_codes: Optional[List[str]] = field(default_factory=list),
                status: Optional[enums.OrderStatus] = enums.OrderStatus.DRAFT,
                date_modified: Optional[datetime] = None,
                 ):


        #this is for rehydrate loading from repository only?

        self._order_id = order_id
        self._date_created = date_created
        self.destination = destination
        self.line_items = line_items
        self.customer_details = customer_details
        self.shipping_details = shipping_details
        self.payment_details = payment_details
        self._cancellation_reason = cancellation_reason
        self._total_discounts_fee = total_discounts_fee
        self._offer_details = offer_details
        self._tax_details = tax_details
        self._tax_amount = tax_amount
        self._total_amount = total_amount
        self._final_amount = final_amount
        self._shipping_reference = shipping_reference
        self._coupon_codes = coupon_codes
        self._status = status
        self._date_modified = date_modified

    @classmethod
    def create_order(cls, customer_details: value_objects.CustomerDetails, 
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
            status=enums.OrderStatus.DRAFT.name,
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
        self._date_modified = datetime.now()

    def add_line_item(self, line_item: LineItem) -> None:
        if not line_item:
            raise ValueError("Please provide line item to add.")

        self._validate_line_item(line_item)

        self.line_items.add(line_item)
        self.update_totals()

    def remove_line_item(self, line_item: LineItem) -> None:
        if not line_item:
            raise ValueError("Line item does not exists in the order.")
        self.line_items.remove(line_item)
        self.update_totals()

    #NA just make use of add_line_item and remove_line_item
    #def update_line_item(self, line_item: LineItem):
    #    #use to update specific item quantity or other item info
    #    if not line_item:
    #        raise ValueError("Please provide line item to update details.")
    #    self._validate_line_item(line_item)
    #    #TODO remove wont work since this line_item is not the existing item
    #    self.line_items.remove(line_item)
    #    self.line_items.add(line_item)
    #    self.update_totals()

    def place_order(self):
        if not self.line_items:
            raise exceptions.InvalidOrderOperation("Canno place an order without line items.")
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
        if self.status != enums.OrderStatus.CONFIRMED.name:
            raise exceptions.InvalidOrderOperation("Only confirm order can mark as shipped.")
        self._status = enums.OrderStatus.SHIPPED.name
        self.update_modified_date()

    def cancel_order(self, cancellation_reason: str):
        if not self.status in (enums.OrderStatus.PENDING.name, enums.OrderStatus.CONFIRMED.name):
            raise exceptions.InvalidOrderOperation("Cannot cancel a completed or already cancelled order or shipped order")
        self._status = enums.OrderStatus.CANCELLED.name
        self._cancellation_reason = cancellation_reason
        self.update_modified_date()
    
    def mark_as_completed(self):
        if self.status != enums.OrderStatus.SHIPPED.name:
            raise exceptions.InvalidOrderOperation("Only shipped order can mark as completed.")

        if self.payment_details.method == enums.PaymentMethod.COD and not self.payment_details:
            raise exceptions.InvalidOrderOperation("Cannot mark as completed with outstanding payments.")

        self._status = enums.OrderStatus.COMPLETED.name
        self.update_modified_date()

    def add_shipping_tracking_reference(self, shipping_reference: str):
        self._shipping_reference = shipping_reference

    def update_tax_amount(self, amount: value_objects.Money):
        self._tax_amount = amount
        self.calculate_final_amount()
    
    def update_offer_details(self, offer_details: List[str]):
        self._offer_details = offer_details

    def update_tax_details(self, tax_details: List[str]):
        self._tax_details = tax_details

    def apply_coupon(self, coupon_code: str):
        self._coupon_codes.append(coupon_code)

    def remove_coupon(self, coupon_code: str):
        self._coupon_codes.remove(coupon_code)
    
    def update_shipping_details(self, shipping_details: value_objects.ShippingDetails):
        if not shipping_details:
            raise exceptions.InvalidOrderOperation("Shipping details cannot be none.")
        self.shipping_details = shipping_details
        self.calculate_final_amount()
        self.update_modified_date()
    
    def select_shipping_option(self, shipping_option: enums.ShippingMethod, shipping_options: List[dict]):
        for option in shipping_options:
            if option.get("name") == shipping_option:
                self.update_shipping_details(value_objects.ShippingDetails(
                        method=option.get("name"),
                        delivery_time=option.get("delivery_time"),
                        cost=option.get("cost"),
                        orig_cost=option.get("cost")
                    )
                )
                return
        raise exceptions.InvalidOrderOperation(f"Shipping option not supported: {shipping_option}")

    def update_totals(self):
        self._total_amount = value_objects.Money(
            amount=sum(line.total_price for line in self.line_items),
            currency=self.currency
        )
        self.calculate_final_amount()

    def update_total_discounts_fee(self, total_discounts: value_objects.Money):
        self._total_discounts_fee = total_discounts
        self.calculate_final_amount()

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
        self.update_totals()
        #TODO: reset free gifts??

    def calculate_final_amount(self):
        #make sure to call apply_offers & apply_taxes
        self._final_amount = (
                self.total_amount 
                - self.total_discounts_fee
                - self.tax_amount
            ) + (self.shipping_details.cost if self.shipping_details else value_objects.Money(0, self.currency))

    @property
    def total_amount(self) -> value_objects.Money:
        return self._total_amount

    @property
    def total_discounts_fee(self) -> value_objects.Money:
        return self._total_discounts_fee

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
    def customer_coupons(self) -> List[str]:
        return self._coupon_codes

    @property
    def currency(self) -> str:
        #assuming invariants
        return self.line_items[0].product_price.currency
        #return self._currency

    @property
    def tax_details(self) -> str:
        return self._tax_details

    @property
    def tax_amount(self) -> value_objects.Money:
        return self._tax_amount

    @property
    def final_amount(self) -> value_objects.Money:
        return self._final_amount

    @property
    def order_id(self) -> str:
        return self._order_id

    @property
    def date_created(self) -> datetime:
        return self._date_created

    @property
    def date_modified(self) -> datetime:
        return self._date_modified

    @property
    def order_status(self) -> str:
        return self._status

    @property
    def cancellation_reason(self) -> str:
        return self._cancellation_reason

    @property
    def offer_details(self) -> str:
        return self._offer_details

    @property
    def vendor_name(self) -> str:
        #assuming invariant
        return self.line_items[0].vendor_name





