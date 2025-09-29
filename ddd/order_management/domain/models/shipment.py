from __future__ import annotations
from dataclasses import dataclass
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
class ShipmentItem:
    shipment_item_id: str
    line_item: LineItem
    quantity: int
    allocated_shipping_tax: value_objects.Money = field(default_factory=lambda: value_objects.Money.default())
    
    def __post_init__(self):
        if self.quantity > line_item.quantity:
            raise exceptions.DomainError("Cannot allocate more than ordered quantity")

@dataclass
class Shipment:
    shipment_id: str
    shipment_address: value_objects.Address
    shipment_provider: Optional[str] = None
    shipment_service_code: Optional[str] = None
    tracking_reference: Optional[str] = None
    shipment_amount: value_objects.Money = field(default_factory=lambda: value_objects.Money.default())
    shipment_tax_amount: value_objects.Money = field(default_factory=lambda: value_objects.Money.default())
    shipment_status: enums.ShipmentStatus = enums.ShipmentStatus.PENDING
    shipment_items: List[ShipmentItem] = field(default_factory=list)

    def add_line_item(self, shipment_item: ShipmentItem):
        self.shipment_items.append(shipment_item)

    @property
    def shipment_items_sku_qty(self):
        return {item.product_sku: item.quantity for item in self.shipment_items}


    def allocate_shipping_tax(self):
        total_line_subtotal = sum(
            sli.line_item.total_amount.amount * sli.quantity for sli in self.shipment_items
        )

        if total_line_subtotal == 0:
            return

        for sli in self.shipment_items:
            proportion = (sli.line_item.total_amount.amount * sli.quantity) / total_line_subtotal
            sli.allocated_shipping_tax = value_objects.Money(
                self.shipment_tax_amount.amount * proportion,
                self.shipment_tax_amount.currency
            )
