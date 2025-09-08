from __future__ import annotations
import uuid
from decimal import Decimal
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, List, Tuple, TYPE_CHECKING
from ddd.order_management.domain.models.line_item import LineItem
from ddd.order_management.domain import enums, exceptions, events, value_objects
from ddd.order_management.domain.services import DomainClock


@dataclass
class Order:
    date_created: datetime
    tenant_id: str
    destination: value_objects.Address
    customer_details: value_objects.CustomerDetails
    order_stage: Optional[enums.OrderStage] = None
    activity_status: str = "NoPendingActions"
    order_id: Optional[str] = None
    activities: List[OrderActivity] = field(default_factory=list)
    shipping_details: Optional[value_objects.ShippingDetails] = None
    line_items: List[LineItem] = field(default_factory=list)
    payment_details: Optional[value_objects.PaymentDetails] = None
    cancellation_reason: Optional[str] = None
    shipping_reference: Optional[str] = None
    offer_details: List[str] = field(default_factory=list)
    tax_details: List[str] = field(default_factory=list)
    coupons: List[value_objects.Coupon] = field(default_factory=list)
    total_discounts_fee: value_objects.Money = field(default_factory=lambda: value_objects.Money.default())
    tax_amount: value_objects.Money = field(default_factory=lambda: value_objects.Money.default())
    total_amount: value_objects.Money = field(default_factory=lambda: value_objects.Money.default())
    final_amount: value_objects.Money = field(default_factory=lambda: value_objects.Money.default())
    date_modified: Optional[datetime] = None
    _events: List[events.DomainEvent] = field(default_factory=list, init=False)

    def _validate_line_item(self, line_item: LineItem):
        if self.currency != line_item.product_price.currency:
            raise exceptions.InvalidOrderOperation("Currency mismatch between order and line item.")

        if self.vendor_id and self.vendor_id != line_item.vendor.vendor_id:
            raise exceptions.InvalidOrderOperation("Vendor mismatch between order and line item.")

    def generate_order_id(self):
        if self.order_id:
            raise exceptions.InvalidOrderOperation("Order Id already generated.")
        self.order_id = f"ORD-{uuid.uuid4().hex[:12].upper()}"

    def _update_modified_date(self):
        self.date_modified = DomainClock.now()

    def add_line_item(self, line_item: LineItem) -> None:
        if not line_item:
            raise exceptions.InvalidOrderOperation("Please provide line item to add.")
        if line_item.is_free_gift and line_item.product_price.amount > 0:
            raise exceptions.InvalidOrderOperation("Free gifts must have a price of zero.")
        if self.order_stage != enums.OrderStage.DRAFT:
            raise exceptions.InvalidOrderOperation("Only draft order can add line item.")

        if self.line_items:
            # this validation is only applicable for those w existing line items
            self._validate_line_item(line_item)
            if line_item.product_sku in [item.product_sku for item in self.line_items]:
                raise exceptions.InvalidOrderOperation(f"Order {self.order_id} Line item with SKU {line_item.product_sku} already exists.")

        self.line_items.append(line_item)
        self._update_totals()

    def remove_line_item(self, line_item: LineItem) -> None:
        if not line_item:
            raise exceptions.InvalidOrderOperation("Please provide line item to remove.")
        if line_item not in self.line_items:
            raise exceptions.InvalidOrderOperation("No line items exist in the order to remove.")
        if self.order_stage != enums.OrderStage.DRAFT:
            raise exceptions.InvalidOrderOperation("Only draft order can remove line items.")

        if len(self.line_items) <= 1:
            raise exceptions.InvalidOrderOperation(
                "Cannot remove the last item. Please cancel the order instead."
            )

        self.line_items.remove(line_item)
        self._update_totals()

    def update_shipping_details(self, shipping_details: value_objects.ShippingDetails) -> None:
        if not shipping_details:
            raise exceptions.InvalidOrderOperation("Shipping details must be provided.")
        if self.order_stage != enums.OrderStage.DRAFT:
            raise exceptions.InvalidOrderOperation("Only draft order can update shipping details.")
        self.shipping_details = shipping_details
        self._update_modified_date()

    def change_order_quantity(self, product_sku: str, new_quantity: int):
        if self.order_stage != enums.OrderStage.DRAFT:
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
        if self.order_stage != enums.OrderStage.DRAFT:
            raise exceptions.InvalidOrderOperation("Only draft order can be place order.")
        if not self.line_items:
            raise exceptions.InvalidOrderOperation("Cannot place an order without line items.")
        if not self.customer_details:
            raise exceptions.InvalidOrderOperation("Customer details must be provided.")

        if not self._all_required_activities_for_stage_done(enums.OrderStage.DRAFT):
            raise exceptions.InvalidOrderOperation(f"Cannot place an order, some activities in {enums.OrderStage.DRAFT} stage are still pending.")

        if any(item.product_price.currency != self.line_items[0].product_price.currency for item in self.line_items):
            raise exceptions.InvalidOrderOperation("All line items must have the same currency.")

        if len(set(item.vendor.vendor_id for item in self.line_items)) > 1:
            raise exceptions.InvalidOrderOperation("All line items must belong to the same vendor.")

        if not self.shipping_details:
            raise exceptions.InvalidOrderOperation("Order must have a selected shipping option")

        self.order_stage = enums.OrderStage.PENDING
        self._update_modified_date()

        event = events.PlacedOrderEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            order_stage=self.order_stage,
            activity_status=self.activity_status
        )

        self.raise_event(event)

    def verify_payment(self, payment_details: value_objects.PaymentDetails) -> bool:
        if payment_details.order_id != self.order_id:
            raise exceptions.InvalidOrderOperation("Payment details verification Order ID mismatch")

        if payment_details.paid_amount < self.final_amount:
            raise exceptions.InvalidOrderOperation(
                f"Payment details paid amount not match with expected amount {self.final_amount.amount} {self.final_amount.currency}"
            )

        if payment_details.status != enums.PaymentStatus.PAID:
            raise exceptions.InvalidOrderOperation(f"Payment details {payment_details.transaction_id} was not success")

        self._update_payment_details(payment_details)

        return True


    def confirm_order(self, is_verified: bool):
        if self.order_stage != enums.OrderStage.PENDING:
            raise exceptions.InvalidOrderOperation("Only pending orders can be confirmed.")

        if not self._all_required_activities_for_stage_done(enums.OrderStage.PENDING):
            raise exceptions.InvalidOrderOperation(f"Order cannot be confirmed, some activities in {enums.OrderStage.PENDING} stage are still pending.")


        if not is_verified:
            raise exceptions.InvalidOrderOperation("Order cannot be confirmed without verified payment.")

        self.order_stage = enums.OrderStage.CONFIRMED
        self._update_modified_date()

        event = events.ConfirmedOrderEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            order_stage=self.order_stage,
            activity_status=self.activity_status
        )

        self.raise_event(event)

    def apply_applicable_offers(self, offers: List[OfferStrategyAbstract]):
        if self.order_stage not in (enums.OrderStage.DRAFT, enums.OrderStage.PENDING):
            raise exceptions.InvalidOrderOperation("Only draft order can apply offers (Free shipping, Free gifts, etc)")
        if self.offer_details:
            raise exceptions.InvalidOrderOperation("Offers have already been applied.")
        if not self.shipping_details:
            raise exceptions.InvalidOrderOperation("Only when shipping option is selected.")

        offer_details = []
        for offer in offers:
            res = offer.apply(self)
            if res:
                offer_details.append(res)


        if offer_details:
            self._update_offer_details(offer_details)

        self._update_modified_date()

        event = events.AppliedOffersEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            order_stage=self.order_stage,
            activity_status=self.activity_status
        )

        self.raise_event(event)


    def apply_tax_results(self, tax_results: List[value_objects.TaxResult]):
        if self.order_stage != enums.OrderStage.DRAFT:
            raise exceptions.InvalidOrderOperation("Only draft order can calculate taxes.")
        if not self.destination:
            raise exceptions.InvalidOrderOperation("Shipping address is required for tax calculation.")

        # No harm to recalculate
        #if self.tax_details:
        #    raise exceptions.InvalidOrderOperation("Taxes have already been applied.")

        if not any(item.is_taxable for item in self.line_items):
            return #Skip tax if no taxable items
        if self.sub_total.amount == 0:
            raise #Skip tax for zero subtotal

        tax_amount = value_objects.Money.default()
        tax_details = []

        for result in tax_results:
            tax_amount = tax_amount.add(result.amount)
            tax_details.append(result.desc)

        if tax_amount.amount < Decimal("0"):
            raise exceptions.InvalidOrderOperation("Tax amount cannot be negative.")

        self.tax_amount = tax_amount.format()
        self.tax_details = tax_details

        self.calculate_final_amount()
        self._update_modified_date()

        event = events.AppliedTaxesEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            order_stage=self.order_stage,
            activity_status=self.activity_status
        )

        self.raise_event(event)

    def _update_payment_details(self, payment_details: value_objects.PaymentDetails):
        if not payment_details:
            raise exceptions.InvalidOrderOperation("Payment details cannot be none.")
        if self.order_stage != enums.OrderStage.PENDING:
            raise exceptions.InvalidOrderOperation("Only pending order can update payment details.")

        self.payment_details = payment_details

    def mark_as_shipped(self):
        if self.order_stage != enums.OrderStage.CONFIRMED:
            raise exceptions.InvalidOrderOperation("Only confirm order can mark as shipped.")

        if not self._all_required_activities_for_stage_done(enums.OrderStage.CONFIRMED):
            raise exceptions.InvalidOrderOperation(f"Order cannot mark as shipped, some activities in {enums.OrderStage.CONFIRMED} stage are still pending.")

        self.order_stage = enums.OrderStage.SHIPPED
        self._update_modified_date()

        event = events.ShippedOrderEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            order_stage=self.order_stage,
            activity_status=self.activity_status
        )

        self.raise_event(event)

    def mark_as_draft(self):
        if self.order_stage != None:
            raise exceptions.InvalidOrderOperation("Only new order w checked-out items can mark as draft.")
        self.order_stage = enums.OrderStage.DRAFT
        self._update_modified_date()

        event = events.CheckedOutEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            order_stage=self.order_stage,
            activity_status=self.activity_status
        )

        self.raise_event(event)

    def cancel_order(self, cancellation_reason: str):
        if not self.order_stage in (enums.OrderStage.PENDING, enums.OrderStage.CONFIRMED):
            raise exceptions.InvalidOrderOperation("Cannot cancel a completed or already cancelled order or shipped order or draft order")

        # Cancel anytime
        #if not self._all_required_activities_for_stage_done(enums.OrderStage.CONFIRMED):
        #    raise exceptions.InvalidOrderOperation(f"Order cannot mark as shipped, some activities in {enums.OrderStage.CONFIRMED} stage are still pending.")

        if not cancellation_reason:
            raise exceptions.InvalidOrderOperation("Cannot cancel without a cancellation reason.")
        self.order_stage = enums.OrderStage.CANCELLED
        self.cancellation_reason = cancellation_reason
        self._update_modified_date()

        event = events.CanceledOrderEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            order_stage=self.order_stage,
        )

        self.raise_event(event)
    
    def mark_as_completed(self):
        if self.order_stage != enums.OrderStage.SHIPPED:
            raise exceptions.InvalidOrderOperation("Only shipped order can mark as completed.")

        if not self._all_required_activities_for_stage_done(enums.OrderStage.SHIPPED):
            raise exceptions.InvalidOrderOperation(f"Cannot mark as completed, some activities in {enums.OrderStage.SHIPPED} stage are still pending.")

        if not self.payment_details or (self.payment_details and self.payment_details.status != enums.PaymentStatus.PAID):
            raise exceptions.InvalidOrderOperation(f"Cannot mark as completed with outstanding payments.")

        if self.payment_details.paid_amount < self.final_amount:
            raise exceptions.InvalidOrderOperation(f"Cannot mark as completed with outstanding payments. Paid amount {self.payment_details.paid_amount.currency} {self.payment_details.paid_amount.amount} is lesser than the expected amount {self.final_amount.currency} {self.final_amount.amount}")

        #if self.payment_details.method == enums.PaymentMethod.COD and not self.payment_details:
        #    raise exceptions.InvalidOrderOperation(f"Cannot mark as completed with outstanding payments for {enums.PaymentMethod.COD}.")

        self.order_stage = enums.OrderStage.COMPLETED
        self._update_modified_date()

        event = events.CompletedOrderEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            order_stage=self.order_stage,
            activity_status=self.activity_status
        )

        self.raise_event(event)

    def add_shipping_tracking_reference(self, shipping_reference: str):
        if self.order_stage != enums.OrderStage.SHIPPED:
            raise exceptions.InvalidOrderOperation("Only shipped order can add tracking reference.")
        if not shipping_reference.startswith("http"):
            raise exceptions.InvalidOrderOperation("The Shipping tracking reference url is invalid.")

        self.shipping_reference = shipping_reference
        self._update_modified_date()

    def _update_offer_details(self, offer_details: List[str]):
        if self.order_stage != enums.OrderStage.DRAFT:
            raise exceptions.InvalidOrderOperation("Only draft order can update offer details.")
        self.offer_details = offer_details

    def apply_valid_coupon(self, coupon: value_objects.Coupon):
        if not coupon:
            raise exceptions.InvalidOrderOperation("Coupon cannot be none.")
        if self.order_stage != enums.OrderStage.DRAFT:
            raise exceptions.InvalidOrderOperation("Only draft order can apply coupon.")
        if coupon in self.coupons:
            raise exceptions.InvalidOrderOperation(f"Coupon {coupon.coupon_code} already applied in the order.")

        self.coupons.append(coupon)
        self._update_modified_date()

        event = events.AppliedCouponEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            order_stage=self.order_stage,
            activity_status=self.activity_status
        )

        self.raise_event(event)

    def remove_coupon(self, coupon: value_objects.Coupon):
        if not coupon:
            raise exceptions.InvalidOrderOperation("Coupon cannot be none.")
        if self.order_stage != enums.OrderStage.DRAFT:
            raise exceptions.InvalidOrderOperation("Only draft order can remove coupon.")

        self.coupons.remove(coupon)
        self._update_modified_date()

        event = events.RemovedCouponEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            order_stage=self.order_stage,
            activity_status=self.activity_status
        )

        self.raise_event(event)

    def change_destination(self, destination: value_objects.Address):
        if not destination:
            raise exceptions.InvalidOrderOperation("Destination cannot be none.")
        if self.order_stage != enums.OrderStage.DRAFT:
            raise exceptions.InvalidOrderOperation("Only draft order can change destination.")
        self.destination = destination
        self._update_modified_date()

        event = events.ChangedDestinationEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            order_stage=self.order_stage,
            activity_status=self.activity_status
        )

        self.raise_event(event)
    
    def select_shipping_option(self, shipping_option: value_objects.ShippingDetails, shipping_options: List[value_objects.ShippingDetails]):
        if self.order_stage != enums.OrderStage.DRAFT:
            raise exceptions.InvalidOrderOperation("Only draft order can select shipping option.")
        for option in shipping_options:
            if option == shipping_option:
                self.update_shipping_details(option)

                event = events.SelectedShippingOptionEvent(
                    tenant_id=self.tenant_id,
                    order_id=self.order_id,
                    order_stage=self.order_stage,
                    activity_status=self.activity_status
                )

                self.raise_event(event)

                return self
        raise exceptions.InvalidOrderOperation(f"Shipping option not supported: {shipping_option}")

    def _update_totals(self):
        self.total_amount = value_objects.Money(
            amount=sum(line.total_price.amount for line in self.line_items),
            currency=self.currency
        )

    def update_total_discounts_fee(self, total_discounts: value_objects.Money):
        if self.order_stage != enums.OrderStage.DRAFT:
            raise exceptions.InvalidOrderOperation("Only draft order can update total discount fees.")
        self.total_discounts_fee = total_discounts

    def load_tenant_activities(self, activities: List[models.OrderActivity]):
        if self.order_stage != enums.OrderStage.DRAFT:
            raise exceptions.InvalidOrderOperation("Only draft order can load tenant activities.")

        if activities:
            self.activities = activities

    def mark_activity_done(self, current_step: str, 
        performed_by: str, user_input: Optional[Dict] = None,
        outcome: enums.StepOutcome = enums.StepOutcome.DONE):

        if not self.activities:
            return  # tenant doesnt require any other activity
            #raise exceptions.InvalidOrderOperation(f"No activity steps configured.")

        all_steps = [act.step for act in sorted(self.activities, key=lambda a: a["sequence"])]
        if not current_step in all_steps:
            return True # not applicable since the step is not define in the flow

        pending_steps = [act for act in sorted(self.activities, key=lambda a: a["sequence"]) if act.is_pending]
        if not pending_steps:
            self.activity_status = "NoPendingActions"
            self._update_modified_date()

        next_step = pending_steps[0]
        if next_step.step != current_step:
            raise exceptions.InvalidOrderOperation(f"Expected step {next_step.step}, got {current_step}")

        next_step.mark_as_done(performed_by, user_input, outcome)

        self.activity_status = next_step.activity_status
        self._update_modified_date()

        event = events.ActivityEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            order_stage=self.order_stage,
            activity_status=self.activity_status,
            step_name=self.next_step.step
        )

        self.raise_event(event)

    def _all_required_activities_for_stage_done(self, stage: enums.OrderStage) -> bool:
        # check if all activities for a given stage are done/approved or skipped
        stage_activities = [act for act in self.activities if act.stage == stage]
        if not stage_activities:
            return True # No activities config for this stage, fall back to allow transition

        for act in stage_activities:
            if act.is_pending():
                return False
        
        return True


    @property
    def sub_total(self):
        return self.total_amount.subtract(self.total_discounts_fee).add(self.shipping_details.cost if self.shipping_details else value_objects.Money(Decimal("0"), self.currency))

    def calculate_final_amount(self):
        if self.order_stage != enums.OrderStage.DRAFT:
            raise exceptions.InvalidOrderOperation("Only draft order can calculate final amount.")

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
        if not self.line_items:
            raise exceptions.InvalidOrderOperation("Currency is unknown because the order has no line items.")
        return self.line_items[0].product_price.currency

    @property
    def vendor_id(self) -> str:
        #assuming invariant
        if not self.line_items:
            raise exceptions.InvalidOrderOperation("Vendor is unknown because the order has no line items.")
        return self.line_items[0].vendor.vendor_id

    @property
    def vendor_name(self) -> str:
        #assuming invariant
        if not self.line_items:
            raise exceptions.InvalidOrderOperation("Vendor is unknown because the order has no line items.")
        return self.line_items[0].vendor.name

    @property
    def vendor_country(self) -> str:
        #assuming invariant
        if not self.line_items:
            raise exceptions.InvalidOrderOperation("Vendor is unknown because the order has no line items.")
        if not self.line_items[0].vendor.country:
            raise exceptions.InvalidOrderOperation("Vendor country is missing, its crucial in determining domestic shipment.")
        return self.line_items[0].vendor.country

    def __hash__(self):
        return hash(self.order_id)

    def __eq__(self, other):
        return isinstance(other, Order) and self.order_id == other.order_id
