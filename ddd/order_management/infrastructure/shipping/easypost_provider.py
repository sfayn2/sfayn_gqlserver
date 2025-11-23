from __future__ import annotations
import easypost
from typing import Any
from decimal import Decimal
from dataclasses import asdict
from ddd.order_management.application import dtos
from ddd.order_management.domain import enums
from .utils import kg_to_lb, kg_to_oz, cm_to_in

#Protocol: ports.ShippingProviderAbstract
class EasyPostShippingProvider:

    def __init__(self, api_key: str, endpoint: str ):
        self.client = easypost.EasyPostClient(api_key)

    def is_self_delivery(self) -> bool:
        return False

    def create_shipment(self, shipment, tenant_id: str) -> dtos.CreateShipmentResponseDTO:

        easypost_shipment = self.client.shipment.create(
            from_address=shipment.pickup_address,
            to_address=asdict(shipment.shipment_address),
            parcel=self._build_parcel_payload(shipment),
            metadata={
                "tenant_id": tenant_id,
                "shipment_id": shipment.shipment_id
            }
        )

        bought_shipment = self.client.shipment.buy(easypost_shipment.id, rate=easypost_shipment.lowest_rate())

        tracker = bought_shipment.get("tracker", {})
        tracking_code = tracker.get("tracking_code") or bought_shipment.get("tracking_code")

        label_url = bought_shipment.get("postage_label").get("label_url")


        rate_info = easypost_shipment.lowest_rate()
        total_amount = rate_info["amount"]
        currency = rate_info["currency"]

        #Option for pickup
        if shipment.shipment_method == enums.ShipmentMethod.PICKUP:
            self._schedule_pickup(
                easypost_shipment.id,
                shipment
            )


        return dtos.CreateShipmentResponseDTO(
            tracking_reference=tracking_code,
            total_amount=dtos.MoneyDTO(
                amount=total_amount,
                currency=currency
            ),
            label_url=label_url
        )
    
    def _build_parcel_payload(self, shipment):

        if shipment.package_weight_kg:
            total_weight = shipment.package_weight_kg.weight_to_oz()
        else:
            total_weight = sum(
                si.package
                for si in shipment.shipment_items.line_item.package
            )

        if shipment.package_length_cm and shipment.package_width_cm and shipment.package_height_cm:
            parcel = {
                "weight": kg_to_oz(total_weight),
                "length": cm_to_in(shipment.package_length_cm),
                "width": cm_to_in(shipment.package_width_cm),
                "height": cm_to_in(shipment.package_height_cm)
            }
        else:
            length, width, height = shipment.get_max_dimension()
            parcel = {
                "weight": kg_to_oz(total_weight),
                "length": cm_to_in(length),
                "width": cm_to_in(width),
                "height": cm_to_in(height)
            }

    def _schedule_pickup(self, easypost_shipment_id, shipment, carrier_account_id=None):

        pickup_params = {
            "address": shipment.pickup_address,
            "shipment": {"id": easypost_shipment_id},
            "min_datetime": shipment.pickup_window_start.strftime("%Y-%m-%d %H:%M:%S"),
            "max_datetime": shipment.pickup_window_end.strftime("%Y-%m-%d %H:%M:%S"),
            "is_account_address": False,
            "instructions": shipment.pickup_instructions
        }

        #Optional specify carrier account for pickup
        if carrier_account_id:
            pickup_params["carrier_accounts"] = [{"id": carrier_account_id}]

        # create pickup object
        pickup = self.client.pickup.create(**pickup_params)

        bought_pickup = self.client.pickup.buy(
            pickup.id,
            rate=pickup.lowest_rate()
        )

        return bought_pickup


