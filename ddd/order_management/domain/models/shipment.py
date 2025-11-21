from __future__ import annotations
from decimal import Decimal
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
class ShipmentItem:
    line_item: models.LineItem
    quantity: int
    shipment_item_id: Optional[str] = None
    allocated_shipping_tax: value_objects.Money = field(default_factory=lambda: value_objects.Money.default())

    #TODO how to deal w this? 
    #def __post_init__(self):
    #    if self.quantity > line_item.quantity:
    #        raise exceptions.DomainError("Cannot allocate more than ordered quantity")

@dataclass
class Shipment:
    shipment_id: str

    shipment_address: value_objects.Address
    shipment_mode: Optional[enums.ShipmentMethod] = None # pickup, dropoff, warehouse
    shipment_provider: Optional[str] = None #easypost, fedex, etc

    # package
    package_weight_kg: Optional[Decimal] = None
    package_length_cm: Optional[Decimal] = None
    package_width_cm: Optional[Decimal] = None
    package_height_cm: Optional[Decimal] = None

    # pickup mode
    pickup_address: Optional[value_objects.Address] = None
    pickup_window_start: Optional[datetime] = None
    pickup_window_end: Optional[datetime] = None
    pickup_instructions: Optional[str] = None


    tracking_reference: Optional[str] = None
    label_url: Optional[str] = None


    shipment_amount: value_objects.Money = field(default_factory=lambda: value_objects.Money.default())
    shipment_tax_amount: value_objects.Money = field(default_factory=lambda: value_objects.Money.default())
    shipment_status: enums.ShipmentStatus = enums.ShipmentStatus.PENDING
    shipment_items: List[ShipmentItem] = field(default_factory=list)



    def add_line_item(self, shipment_item: ShipmentItem):
        self.shipment_items.append(shipment_item)

    @property
    def shipment_items_sku_qty(self):
        return {item.line_item.product_sku: item.line_item.order_quantity for item in self.shipment_items}

    def get_max_dimensions(self):
        for item in self.shipment_items:
            pkg = getattr(item, "package", None)
            if pkg and hasattr(pkg, "dimensions"):
                l, w, h = pkg.dimensions
                lengths.append(l)
                widths.append(w)
                heights.append(h)

        if lengths and widths and heights: 
            return max(lengths), max(widths), max(heights)

        raise exceptions.DomainError(f"Unable to determine package max dimension for shipment id {self.shipment_id}")



    #def allocate_shipping_tax(self):
    #    total_line_subtotal = sum(
    #        sli.line_item.total_amount.amount * sli.quantity for sli in self.shipment_items
    #    )

    #    if total_line_subtotal == 0:
    #        return

    #    for sli in self.shipment_items:
    #        proportion = (sli.line_item.total_amount.amount * sli.quantity) / total_line_subtotal
    #        sli.allocated_shipping_tax = value_objects.Money(
    #            self.shipment_tax_amount.amount * proportion,
    #            self.shipment_tax_amount.currency
    #        )
