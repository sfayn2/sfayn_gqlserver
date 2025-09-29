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

    date_modified: Optional[datetime] = None
    _events: List[events.DomainEvent] = field(default_factory=list, init=False)

    def raise_event(self, event: events.DomainEvent):
        self._events.append(event)

    def add_line_item(self, line_item: LineItem) -> None:
        if not line_item:
            raise exceptions.DomainError("Please provide line item to add.")
        
        #OMS side only
        if self.order_status != enums.OrderStatus.CONFIRMED:
            raise exceptions.DomainError("Only confirmed order can add line item.")

        if self.line_items:
            # this validation is only applicable for those w existing line items
            if line_item.product_sku in [item.product_sku for item in self.line_items]:
                raise exceptions.DomainError(f"Order {self.order_id} Line item with SKU {line_item.product_sku} already exists.")

        self.line_items.append(line_item)

    def _update_modified_date(self):
        self.date_modified = DomainClock.now()

    def add_shipment(self, shipment: Shipment) -> Shipment:
        if self.order_status != enums.OrderStatus.CONFIRMED:
            raise exceptions.DomainError("Only confirm order can add shipment.")

        order_skus = {li.product_sku for li in self.line_items}

        # Verify that every item in the new shipment exists in the order.
        for new_item in shipment.shipment_items:
            if new_item.product_sku not in order_skus:
                raise exceptions.DomainError(
                    f"Product SKU {new_item.product_sku} in the new shipment does not exist in the order."
                )

        # Calculate current and new quantities more concisely with generator expressions.
        allocated_qty = sum(item.order_quantity for s in self.shipments for item in s.shipment_items)
        new_allocate_qty = sum(item.order_quantity for item in shipment.shipment_items)

        if allocated_qty + new_allocate_qty > self.total_line_item_qty:
            raise exceptions.DomainError(
                f"Cannot add shipment. Total allocated quantity ({allocated_qty + new_allocate_qty}) "
                f"exceeds the order's total quantity ({self.total_line_item_qty})."
            )

        self.shipments.append(shipment)

        return shipment

    @property
    def total_line_item_qty(self) -> int:
        return sum(li.order_quantity for li in self.line_items)

    def _validate_shipment_items(self):
        # Verify that every item in the new shipment exists in the order & quantity matches.
        for li in self.line_items:
            for shipment in self.shipments:
                if shipment.shipment_items_sku_qty.get(li.product_sku):
                    if not shipment.shipment_items_sku_qty.get(li.product_sku) == li.order_quantity:
                        raise exceptions.DomainError(
                            f"Shipment for Product SKU {li.product_sku} does not match the required orders quantity."
                        )
                else:
                    raise exceptions.DomainError(
                        f"Order Item for Product SKU {li.product_sku} does not exists on any of shipment item/s."
                    )

    def mark_as_shipped(self):
        if self.order_status != enums.OrderStatus.CONFIRMED:
            raise exceptions.DomainError("Only confirm order can mark as shipped.")

        if not self.shipments:
            raise exceptions.DomainError("No shipments present")

        #all shipment status are Shipped
        if self.shipments and any(d.shipment_status != enums.ShipmentStatus.SHIPPED for d in self.shipments):
            raise exceptions.DomainError("Not all shipments are shipped")

        # Verify that every item in the new shipment exists in the order & quantity matches.
        self._validate_shipment_items()


        #if not self._all_required_workflows_for_stage_done(enums.OrderStatus.CONFIRMED):
        #    raise exceptions.DomainError(f"Order cannot mark as shipped, some workflows in {enums.OrderStatus.CONFIRMED} stage are still pending.")

        self.order_status = enums.OrderStatus.SHIPPED
        self._update_modified_date()

        event = events.ShippedOrderEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            order_status=self.order_status,
            workflow_status=self.workflow_status
        )

        self.raise_event(event)

    def cancel_order(self):
        if not self.order_status in (enums.OrderStatus.PENDING, enums.OrderStatus.CONFIRMED):
            raise exceptions.DomainError("Cannot cancel a completed or already cancelled order or shipped order or draft order")

        if self.shipments and any(d.shipment_status in [enums.ShipmentStatus.SHIPPED, enums.ShipmentStatus.DELIVERED] for d in self.shipments):
            raise exceptions.DomainError("Cannot cancel, Shipments has already been shipped or delivered.")

        #if not cancellation_reason:
        #    raise exceptions.DomainError("Cannot cancel without a cancellation reason.")
        self.order_status = enums.OrderStatus.CANCELLED
        self._update_modified_date()

        event = events.CanceledOrderEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            order_status=self.order_status,
        )

        self.raise_event(event)

    def mark_as_delivered(self):
        if self.order_status != enums.OrderStatus.SHIPPED:
            raise exceptions.DomainError("Only shipped order can mark as delivered.")

        if not self.shipments:
            raise exceptions.DomainError("Cannot mark as delivered w missing shipment item/s, Cancel instead.")

        #all shipment status are Shipped
        if self.shipments and any(d.shipment_status != enums.ShipmentStatus.DELIVERED for d in self.shipments):
            raise exceptions.DomainError("Cannot mark as delivered w pending shipment delivery.")

        # Verify that every item in the new shipment exists in the order & quantity matches.
        self._validate_shipment_items()

        self.order_status = enums.OrderStatus.DELIVERED
        self._update_modified_date()

        event = events.DeliveredOrderEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            order_status=self.order_status,
            workflow_status=self.workflow_status
        )

        self.raise_event(event)

    
    def mark_as_completed(self):
        if self.order_status != enums.OrderStatus.DELIVERED:
            raise exceptions.DomainError("Only delivered order can mark as completed.")

        #if not self._all_required_workflows_for_stage_done(enums.OrderStatus.SHIPPED):
        #    raise exceptions.DomainError(f"Cannot mark as completed, some workflows in {enums.OrderStatus.SHIPPED} stage are still pending.")

        if self.payment_status != enums.PaymentStatus.PAID:
            raise exceptions.DomainError(f"Cannot mark as completed with outstanding payments.")

        self.order_status = enums.OrderStatus.COMPLETED
        self._update_modified_date()

        event = events.CompletedOrderEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            order_status=self.order_status,
            workflow_status=self.workflow_status
        )

        self.raise_event(event)

