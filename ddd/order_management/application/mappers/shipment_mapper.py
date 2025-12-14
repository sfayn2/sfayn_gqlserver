from __future__ import annotations
from ddd.order_management.application import dtos
from ddd.order_management.domain import models, value_objects

class ShipmentMapper:


    @staticmethod
    def to_response_dto(shipment: models.Shipment) -> dtos.ShipmentResponseDTO:
        return dtos.ShipmentResponseDTO(
            shipment_id=shipment.shipment_id,
            shipment_address=dtos.AddressResponseDTO(
                line1=shipment.shipment_address.line1,
                city=shipment.shipment_address.city,
                country=shipment.shipment_address.country,
                line2=shipment.shipment_address.line2,
                state=shipment.shipment_address.state,
                postal=shipment.shipment_address.postal
            ) if shipment.shipment_address else None,
            shipment_provider=shipment.shipment_provider,
            shipment_mode=shipment.shipment_mode,
            package_weight_kg=shipment.package_weight_kg,
            package_length_cm=shipment.package_length_cm,
            package_width_cm=shipment.package_width_cm,
            package_height_cm=shipment.package_height_cm,
            pickup_address=dtos.AddressResponseDTO(
                line1=shipment.pickup_address.line1,
                city=shipment.pickup_address.city,
                country=shipment.pickup_address.country,
                line2=shipment.pickup_address.line2,
                state=shipment.pickup_address.state,
                postal=shipment.pickup_address.postal
            ) if shipment.pickup_address else None,
            pickup_window_start=shipment.pickup_window_start,
            pickup_window_end=shipment.pickup_window_end,
            pickup_instructions=shipment.pickup_instructions,
            tracking_reference=shipment.tracking_reference,
            label_url=shipment.label_url,
            shipment_amount=dtos.MoneyResponseDTO(
                amount=shipment.shipment_amount.amount,
                currency=shipment.shipment_amount.currency
            ) if shipment.shipment_amount else None,
            shipment_status=shipment.shipment_status,
            shipment_items=[
                dtos.ShipmentItemResponseDTO(
                    line_item=dtos.LineItemResponseDTO(
                            product_sku=si.line_item.product_sku,
                            product_name=si.line_item.product_name,
                            order_quantity=si.line_item.order_quantity,
                            vendor_id=si.line_item.vendor_id,
                            package=dtos.PackageResponseDTO(
                                weight_kg=si.line_item.package.weight_kg
                            ) if si.line_item.package else None,
                            product_price=dtos.MoneyResponseDTO(
                                amount=si.line_item.product_price.amount,
                                currency=si.line_item.product_price.currency
                            )
                    ),
                    quantity=si.quantity,
                    shipment_item_id=si.shipment_item_id
                )
                for si in shipment.shipment_items or []
            ]
        )
