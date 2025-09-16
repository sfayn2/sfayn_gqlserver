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
    activities: List[OtherActivity] = field(default_factory=list)
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
        
        #OMS side only
        if self.order_stage != enums.OrderStage.PENDING:
            raise exceptions.InvalidOrderOperation("Only pending order can add line item.")

        if self.line_items:
            # this validation is only applicable for those w existing line items
            self._validate_line_item(line_item)
            if line_item.product_sku in [item.product_sku for item in self.line_items]:
                raise exceptions.InvalidOrderOperation(f"Order {self.order_id} Line item with SKU {line_item.product_sku} already exists.")

        self.line_items.append(line_item)

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

    def load_tenant_activities(self, activities: List[models.OtherActivity]):
        if self.order_stage != enums.OrderStage.DRAFT:
            raise exceptions.InvalidOrderOperation("Only draft order can load tenant activities.")

        if activities:
            self.activities = activities

            activities_sorted = [act for act in sorted(self.activities, key=lambda a: a["sequence"])]

            seen_stages = []
            for act in activities_sorted:
                if act.order_stage not in seen_stages:
                    seen_stages.append(act.order_stage)

            # full expected stage order
            expected_stages = [
                enums.OrderStage.DRAFT,
                enums.OrderStage.PENDING,
                enums.OrderStage.CONFIRMED,
                enums.OrderStage.SHIPPED,
                enums.OrderStage.COMPLETED,
            ]

            if seen_stages != expected_stages:
                raise exceptions.InvalidOrderOperation(
                    f"Tenant activities stages invalid. Expected {expected_stages}, got {seen_stages}"
                )

    def find_step(self, step_name: str):
        #find escalate step
        step = next(
            (a for a in self.activities is a.step_name == step_name),
            None
        )
        if not step or step.is_pending():
            raise exceptions.InvalidOrderOperation(f"{step_name} is missing or still pending.")

        return step

    def mark_activity_done(self, current_step: str, 
        performed_by: str, user_input: Optional[Dict] = None,
        outcome: enums.StepOutcome = enums.StepOutcome.DONE):

        if not self.activities:
            return  # tenant doesnt require any other activity
            #raise exceptions.InvalidOrderOperation(f"No activity steps configured.")

        all_steps = [act.step for act in sorted(self.activities, key=lambda a: a["sequence"])]
        if current_step not in all_steps:
            raise exceptions.InvalidOrderOperation(f"Incomplete step, missing {current_step}")

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
