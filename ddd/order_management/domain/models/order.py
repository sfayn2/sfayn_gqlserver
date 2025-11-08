from __future__ import annotations
import uuid
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, List, Tuple
from ddd.order_management.domain import (
    enums, 
    exceptions, 
    events, 
    value_objects,
    models
)
from ddd.order_management.domain.services import DomainClock

@dataclass
class Order:
    tenant_id: str

    customer_details: value_objects.CustomerDetails

    order_id: str
    currency: str
    order_status: enums.OrderStatus = enums.OrderStatus.DRAFT
    payment_status: enums.PaymentStatus = enums.PaymentStatus.UNPAID

    line_items: List[models.LineItem] = field(default_factory=list)
    shipments: List[models.Shipment] = field(default_factory=list)

    date_created: Optional[datetime] = None
    date_modified: Optional[datetime] = None
    _events: List[events.DomainEvent] = field(default_factory=list, init=False)

    def raise_event(self, event: events.DomainEvent):
        self._events.append(event)

    def add_line_item(self, line_item: models.LineItem) -> None:
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

    def get_line_item(self, product_sku: str, vendor_id: str) -> models.LineItem:
        for li in self.line_items:
            if li.product_sku == product_sku and li.vendor_id == vendor_id:
                return li
        raise exceptions.DomainError(f"Vendor {vendor_id} Line item w SKU {product_sku} not found in order {self.order_id}")


    def get_shipment(self, shipment_id: str) -> models.Shipment:
        shipment = next((s for s in self.shipments if s.shipment_id == shipment_id), None)
        if not shipment:
            raise exceptions.DomainError(f"Shipment {shipment_id} not found in order {self.order_id}")
        return shipment

    def _update_modified_date(self):
        self.date_modified = DomainClock.now()

    def create_shipment(
        self,
        shipment_address: value_objects.Address,
        shipment_items: list[models.ShipmentItem],
    ) -> models.Shipment:

        shipment = models.Shipment(
            shipment_id=str(uuid.uuid4()),
            shipment_address=shipment_address,
            shipment_items=[]
        )

        for item_data in shipment_items:
            line_item = self.get_line_item(item_data.line_item.product_sku, item_data.line_item.vendor_id)
            shipment_item = models.ShipmentItem(
                shipment_item_id=str(uuid.uuid4()),
                line_item=line_item,
                quantity=item_data.quantity
            )
            shipment.add_line_item(shipment_item)

        self.add_shipment(shipment)
        self.update_shipping_progress()
        return shipment

    @staticmethod
    def create_order(tenant_id:str, customer_details: value_objects.CustomerDetails, line_items: List[models.LineItem]):

        if not line_items:
            raise exceptions.DomainError("Cannot create an order with no line items.")

        new_order_id: str = f"ORD-{uuid.uuid4()}"

        order = Order(
                order_id=new_order_id,
                currency="SGD", #TODO
                tenant_id=tenant_id,
                customer_details=customer_details,
                date_created=DomainClock.now(),
            )

        for line_item in line_items:
            order.add_line_item(line_item)

        order.order_status = enums.OrderStatus.CONFIRMED #its always confirm order?

        return order

    def add_shipment(self, shipment: models.Shipment) -> models.Shipment:
        if self.order_status != enums.OrderStatus.CONFIRMED:
            raise exceptions.DomainError("Only confirm order can add shipment.")

        order_skus = {li.product_sku for li in self.line_items}

        # Verify that every item in the new shipment exists in the order.
        for new_item in shipment.shipment_items:
            if new_item.line_item.product_sku not in order_skus:
                raise exceptions.DomainError(
                    f"Product SKU {new_item.line_item.product_sku} in the new shipment does not exist in the order."
                )

        # Calculate current and new quantities more concisely with generator expressions.
        allocated_qty = sum(item.quantity for s in self.shipments for item in s.shipment_items)
        new_allocate_qty = sum(item.quantity for item in shipment.shipment_items)

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

    def apply_shipment_dispatch(self, shipment_id: str, tracking_reference: str, shipment_amount: value_objects.Money, label_url: str):
        shipment = self.get_shipment(shipment_id)
        if shipment.shipment_status != enums.ShipmentStatus.CONFIRMED:
            raise exceptions.DomainError("Only confirmed shipment can be dispatch")
        shipment.shipment_amount = shipment_amount
        shipment.tracking_reference = tracking_reference
        shipment.label_url = label_url

        shipment.shipment_status = enums.ShipmentStatus.IN_TRANSIT


    def confirm_shipment(self, shipment_id: str):
        shipment = self.get_shipment(shipment_id)
        if shipment.shipment_status != enums.ShipmentStatus.PENDING:
            raise exceptions.DomainError("Only pending shipment can be confirm")
        shipment.shipment_status = enums.ShipmentStatus.CONFIRMED


        self.update_shipping_progress()
        event = events.ConfirmedShipmentEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            order_status=self.order_status,
            shipment_id=shipment_id,
        )
        self.raise_event(event)

        return shipment

    def deliver_shipment(self, shipment_id: str):
        shipment = self.get_shipment(shipment_id)
        if shipment.shipment_status != enums.ShipmentStatus.SHIPPED:
            raise exceptions.DomainError("Only shipped shipment can be delivered")
        shipment.shipment_status = enums.ShipmentStatus.DELIVERED

        self.update_shipping_progress()
        event = events.DeliveredShipmentEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            order_status=self.order_status,
            shipment_id=shipment_id,
        )
        self.raise_event(event)

    def cancel_shipment(self, shipment_id: str):
        shipment = self.get_shipment(shipment_id)
        if shipment.shipment_status in (enums.ShipmentStatus.IN_TRANSIT, enums.ShipmentStatus.SHIPPED, enums.ShipmentStatus.DELIVERED):
            raise exceptions.DomainError("Cannot cancel shipment after in_transit/shipped/delivered")
        shipment.shipment_status = enums.ShipmentStatus.CANCELLED

        self.update_shipping_progress()
        event = events.CanceledShipmentEvent(
            tenant_id=self.tenant_id,
            order_id=self.order_id,
            order_status=self.order_status,
            shipment_id=shipment_id,
        )
        self.raise_event(event)

    #def assign_tracking_reference(self, shipment_id: str, tracking_reference: str):
    #    shipment = self.get_shipment(shipment_id)
    #    if shipment.shipment_status not in (enums.ShipmentStatus.PENDING, enums.ShipmentStatus.SHIPPED):
    #        raise exceptions.DomainError("Tracking reference can only be assign before delivery.")

    #    shipment.tracking_reference = tracking_reference
    #    self._update_modified_date()
    #    #event = events.TrackingReferenceAssignedEvent(
    #    #    tenant_id=self.tenant_id,
    #    #    order_id=self.order_id,
    #    #    shipment_id=shipment_id,
    #    #)
    #    #self.raise_event(event)


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
    def update_shipping_progress(self) -> None:
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

