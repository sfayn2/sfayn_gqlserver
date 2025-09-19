from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, List, Tuple
from ddd.order_management.domain import (
    enums, 
    exceptions, 
    events, 
    value_objects
)
from ddd.order_management.domain.services import DomainClock

@dataclass
class Order:
    tenant_id: str
    order_id: str

    customer_id: str
    customer_name: str
    customer_email: str

    currency: str = "USD"
    order_status: enums.OrderStatus = enums.OrderStatus.DRAFT

    line_items: List[LineItem] = field(default_factory=list)
    shipments: List[Shipment] = field(default_factory=list)

    workflows: List[WorkflowStep] = field(default_factory=list)
    workflow_status: str = "NoPendingActions"

    date_modified: Optional[datetime] = None
    _events: List[events.DomainEvent] = field(default_factory=list, init=False)

    def raise_event(self, event: events.DomainEvent):
        self._events.append(event)

    def add_line_item(self, line_item: LineItem) -> None:
        if not line_item:
            raise exceptions.InvalidOrderOperation("Please provide line item to add.")
        
        #OMS side only
        if self.order_status != enums.OrderStatus.PENDING:
            raise exceptions.InvalidOrderOperation("Only pending order can add line item.")

        if self.line_items:
            # this validation is only applicable for those w existing line items
            self._validate_line_item(line_item)
            if line_item.product_sku in [item.product_sku for item in self.line_items]:
                raise exceptions.InvalidOrderOperation(f"Order {self.order_id} Line item with SKU {line_item.product_sku} already exists.")

        self.line_items.append(line_item)

    def _update_modified_date(self):
        self.date_modified = DomainClock.now()

    def add_shipment(self, shipment: Shipment) -> Shipment:
        if self.order_status != enums.OrderStatus.CONFIRMED:
            raise exceptions.InvalidOrderOperation("Only confirm order can add shipment.")

        order_skus = {li.product_sku for li in self.line_items}

        # Verify that every item in the new shipment exists in the order.
        for new_item in shipment.shipment_items:
            if new_item.product_sku not in order_skus:
                raise exceptions.InvalidOrderOperation(
                    f"Product SKU {new_item.product_sku} in the new shipment does not exist in the order."
                )

        # Calculate current and new quantities more concisely with generator expressions.
        allocated_qty = sum(item.order_quantity for s in self.shipments for item in s.shipment_items)
        new_allocate_qty = sum(item.order_quantity for item in shipment.shipment_items)

        if allocated_qty + new_allocate_qty > self.total_line_item_qty:
            raise exceptions.InvalidOrderOperation(
                f"Cannot add shipment. Total allocated quantity ({allocated_qty + new_allocate_qty}) "
                f"exceeds the order's total quantity ({self.total_line_item_qty})."
            )

        self.shipments.append(shipment)

        return shipment

    @property
    def total_line_item_qty(self) -> int:
        return sum(li.order_quantity for li in self.line_items)

    def mark_as_shipped(self):
        if self.order_status != enums.OrderStatus.CONFIRMED:
            raise exceptions.InvalidOrderOperation("Only confirm order can mark as shipped.")

        #all shipment status are Shipped
        if self.shipments and any(d.status == enums.ShipmentStatus.PENDING for d in self.shipments):
            raise exceptions.InvalidOrderOperation("Order has a pending item for shipment")

        if not self._all_required_workflows_for_stage_done(enums.OrderStatus.CONFIRMED):
            raise exceptions.InvalidOrderOperation(f"Order cannot mark as shipped, some workflows in {enums.OrderStatus.CONFIRMED} stage are still pending.")

        self.order_status = enums.OrderStatus.SHIPPED
        self._update_modified_date()

        event = events.ShippedOrderEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            order_status=self.order_status,
            workflow_status=self.workflow_status
        )

        self.raise_event(event)

    def cancel_order(self, cancellation_reason: str):
        if not self.order_status in (enums.OrderStatus.PENDING, enums.OrderStatus.CONFIRMED):
            raise exceptions.InvalidOrderOperation("Cannot cancel a completed or already cancelled order or shipped order or draft order")

        # Cancel anytime
        #if not self._all_required_workflows_for_stage_done(enums.OrderStatus.CONFIRMED):
        #    raise exceptions.InvalidOrderOperation(f"Order cannot mark as shipped, some workflows in {enums.OrderStatus.CONFIRMED} stage are still pending.")

        if not cancellation_reason:
            raise exceptions.InvalidOrderOperation("Cannot cancel without a cancellation reason.")
        self.order_status = enums.OrderStatus.CANCELLED
        self._update_modified_date()

        event = events.CanceledOrderEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            order_status=self.order_status,
        )

        self.raise_event(event)
    
    def mark_as_completed(self):
        if self.order_status != enums.OrderStatus.SHIPPED:
            raise exceptions.InvalidOrderOperation("Only shipped order can mark as completed.")

        if not self._all_required_workflows_for_stage_done(enums.OrderStatus.SHIPPED):
            raise exceptions.InvalidOrderOperation(f"Cannot mark as completed, some workflows in {enums.OrderStatus.SHIPPED} stage are still pending.")

        if self.payment_status != enums.PaymentStatus.PAID:
            raise exceptions.InvalidOrderOperation(f"Cannot mark as completed with outstanding payments.")

        self.order_status = enums.OrderStatus.COMPLETED
        self._update_modified_date()

        event = events.CompletedOrderEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            order_status=self.order_status,
            workflow_status=self.workflow_status
        )

        self.raise_event(event)


    def load_tenant_workflow(self, workflows: List[Workflow]):
        if self.order_status != enums.OrderStatus.DRAFT:
            raise exceptions.InvalidOrderOperation("Only draft order can load tenant workflows.")

        if workflows:
            self.workflows = workflows

            workflows_sorted = [flw for flw in sorted(self.workflows, key=lambda a: a["sequence"])]

            seen_stages = []
            for flw in workflows_sorted:
                if flw.order_status not in seen_stages:
                    seen_stages.append(flw.order_status)

            # full expected stage order
            expected_stages = [
                enums.OrderStatus.DRAFT,
                enums.OrderStatus.PENDING,
                enums.OrderStatus.CONFIRMED,
                enums.OrderStatus.SHIPPED,
                enums.OrderStatus.COMPLETED,
            ]

            if seen_stages != expected_stages:
                raise exceptions.InvalidOrderOperation(
                    f"Tenant workflows stages invalid. Expected {expected_stages}, got {seen_stages}"
                )

    def find_step(self, step_name: str):
        #find escalate step
        step = next(
            (a for a in self.workflows is a.step_name == step_name),
            None
        )
        if not step or step.is_pending():
            raise exceptions.InvalidOrderOperation(f"{step_name} is missing or still pending.")

        return step

    def mark_workflow_done(self, current_step: str, 
        performed_by: str, user_input: Optional[dict] = None,
        outcome: enums.StepOutcome = enums.StepOutcome.DONE):

        if not self.workflows:
            return  # tenant doesnt require any other workflow
            #raise exceptions.InvalidOrderOperation(f"No workflow steps configured.")

        all_steps = [flw.step for flw in sorted(self.workflows, key=lambda a: a["sequence"])]
        if current_step not in all_steps:
            raise exceptions.InvalidOrderOperation(f"Incomplete step, missing {current_step}")

        pending_steps = [flw for flw in sorted(self.workflows, key=lambda a: a["sequence"]) if act.is_pending]
        if not pending_steps:
            self.workflow_status = "NoPendingActions"
            self._update_modified_date()

        next_step = pending_steps[0]
        if next_step.step != current_step:
            raise exceptions.InvalidOrderOperation(f"Expected step {next_step.step}, got {current_step}")

        next_step.mark_as_done(performed_by, user_input, outcome)

        self.workflow_status = next_step.workflow_status
        self._update_modified_date()

        event = events.workflowEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            order_status=self.order_status,
            workflow_status=self.workflow_status,
            step_name=self.next_step.step
        )

        self.raise_event(event)

    def _all_required_workflows_for_stage_done(self, stage: enums.OrderStatus) -> bool:
        # check if all workflows for a given stage are done/approved or skipped
        stage_workflows = [flw for flw in self.workflow if flw.stage == stage]
        if not stage_workflows:
            return True # No workflows config for this stage, fall back to allow transition

        for flw in stage_workflows:
            if flw.is_pending():
                return False
        
        return True