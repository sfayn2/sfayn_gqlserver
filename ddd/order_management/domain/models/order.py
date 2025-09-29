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
    payment_status: enums.PaymentStatus = enums.PaymentStatus.UNPAID

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

    def _get_shipment(self, shipment_id: str) -> Shipment:
        shipment = next((s for s in self.shipments if s.shipment_id == shipment_id), None)
        if not shipment:
            raise exceptions.DomainError(f"Shipment {shipment_id} not found in order {self.order_id}")
        return shipment

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
        self._update_modified_date()

        return shipment

        #self.update_shipping_progress()


    @property
    def total_line_item_qty(self) -> int:
        return sum(li.order_quantity for li in self.line_items)

    def ship_shipment(self, shipment_id: str):
        shipment = self._get_shipment(shipment_id)
        if shipment.shipment_status != enums.ShipmentStatus.PENDING:
            raise exceptions.DomainError("Only pending shipment can be mark as shipped")
        shipment.shipment_status = enums.ShipmentStatus.SHIPPED

        self.update_shipping_progress()
        event = events.ShippedShipmentEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            shipment_id=shipment_id,
        )
        self.raise_event(event)

    def deliver_shipment(self, shipment_id: str):
        shipment = self._get_shipment(shipment_id)
        if shipment.shipment_status != enums.ShipmentStatus.SHIPPED:
            raise exceptions.DomainError("Only shipped shipment can be delivered")
        shipment.shipment_status = enums.ShipmentStatus.DELIVERED

        self.update_shipping_progress()
        event = events.DeliveredShipmentEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            shipment_id=shipment_id,
        )
        self.raise_event(event)

    def cancel_shipment(self, shipment_id: str):
        shipment = self._get_shipment(shipment_id)
        if shipment.shipment_status in (enums.ShipmentStatus.SHIPPED, enums.ShipmentStatus.DELIVERED):
            raise exceptions.DomainError("Cannot cancel shipment after shipped/delivered")
        shipment.shipment_status = enums.ShipmentStatus.CANCELLED

        self.update_shipping_progress()
        event = events.CanceledShipmentEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            shipment_id=shipment_id,
        )
        order.raise_event(event)

    def assign_tracking_reference(self, shipment_id: str, tracking_reference: str):
        shipment = self._get_shipment(shipment_id)
        if shipment.shipment_status != enums.ShipmentStatus.SHIPPED:
            raise exceptions.DomainError("Tracking reference can only be assign before delivery.")

        shipment.tracking_reference = tracking_reference
        self._update_modified_date()
        event = events.TrackingReferenceAssignedEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            shipment_id=shipment_id,
        )
        self.raise_event(event)


    def cancel_order(self):
        if not self.order_status in (enums.OrderStatus.PENDING, enums.OrderStatus.CONFIRMED):
            raise exceptions.DomainError(f"Order in {self.order_status} cannot be cancelled.")

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

    #roll-up style
    def update_shipping_progress(self):
        if not self.shipments:
            return #remain CONFIRMED

        expected = {li.product_sku : li.order_quantity for li in self.line_items}
        shipped: dict[str, int] = {}
        delivered: dict[str, int] = {}

        for sm in self.shipments:
            if sm.shipment_status == enums.ShipmentStatus.SHIPPED:
                for sku, qty in sm.shipment_items_sku_qty.items():
                    shipped[sku] = shipped.get(sku, 0) + qty
            if sm.shipment_status == enums.ShipmentStatus.DELIVERED:
                for sku, qty in sm.shipment_items_sku_qty.items():
                    delivered[sku] = delivered.get(sku, 0) + qty

        all_shipped = all(shipped.get(sku, 0) >= qty for sku, qty in expected.items())
        some_shipped = any(shipped.get(sku, 0) > 0 for sku in expected)

        all_delivered = all(delivered.get(sku, 0) >= qty for sku, qty in expected.items())
        some_delivered = any(delivered.get(sku, 0) > 0 for sku in expected)

        if all_delivered:
            self.order_status = enums.OrderStatus.DELIVERED
        elif all_shipped:
            self.order_status = enums.OrderStatus.SHIPPED
        elif some_delivered:
            self.order_status = enums.OrderStatus.PARTIAL_DELIVERED
        elif some_shipped:
            self.order_status = enums.OrderStatus.PARTIAL_SHIPPED

        self._update_modified_date()

    
    def mark_as_completed(self):
        if self.order_status != enums.OrderStatus.DELIVERED:
            raise exceptions.DomainError("Only delivered order can mark as completed.")

        if self.payment_status != enums.PaymentStatus.PAID:
            raise exceptions.DomainError(f"Cannot mark as completed with outstanding payments.")

        self.order_status = enums.OrderStatus.COMPLETED
        self._update_modified_date()

        event = events.CompletedOrderEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            order_status=self.order_status,
        )

        self.raise_event(event)

