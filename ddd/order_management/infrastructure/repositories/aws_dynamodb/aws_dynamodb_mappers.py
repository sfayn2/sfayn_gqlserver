from typing import Dict, Any, List
from datetime import datetime
from decimal import Decimal
from ddd.order_management.domain import models, value_objects, enums

class OrderDynamoMapper:
    @staticmethod
    def to_dynamo(order: models.Order) -> List[Dict[str, Any]]:
        """Convert Domain Aggregate into a list of Single Table Design DynamoDB items."""

        items: List[Dict[str, Any]] = []

        
        # 1. Order Header (Stored in Tenant Partition for tenant-wide listing)
        items.append({
            "pk": f"TENANT#{order.tenant_id}",
            "sk": f"ORDER#{order.order_id}",
            "order_id": order.order_id,
            "tenant_id": order.tenant_id,
            "external_ref": order.external_ref,
            "customer_id": order.customer_details.customer_id,
            "customer_name": order.customer_details.name,
            "customer_email": order.customer_details.email,
            "order_status": order.order_status.value,
            "payment_status": order.payment_status.value,
            "currency": order.currency,
            "date_created": order.date_created.isoformat() if order.date_created else None,
            "date_modified": order.date_modified.isoformat() if order.date_modified else None,
            "entity_type": "ORDER"
        })

        # 2. Line Items (Stored in Order Partition for efficient order retrieval)
        for li in order.line_items:
            items.append({
                "pk": f"ORDER#{order.order_id}",
                "sk": f"LINE#{li.product_sku}",
                "product_sku": li.product_sku,
                "product_name": li.product_name,
                # store numeric values as strings for DynamoDB single-table attribute typing
                "product_price": li.product_price.amount,
                "product_currency": li.product_price.currency,
                "order_quantity": li.order_quantity,
                "vendor_id": li.vendor_id,
                "package_weight_kg": li.package.weight_kg if li.package else None,
                "entity_type": "LINE_ITEM"
            })

        # 3. Shipments & Shipment Items (Stored in Order Partition)
        for s in order.shipments:
            # Shipment Header
            items.append({
                "pk": f"ORDER#{order.order_id}",
                "sk": f"SHIPMENT#{s.shipment_id}",
                "line1": s.shipment_address.line1 if s.shipment_address else None,
                "line2": s.shipment_address.line2 if s.shipment_address else None,
                "city": s.shipment_address.city if s.shipment_address else None,
                "status": s.shipment_status.value,
                "postal": s.shipment_address.postal if s.shipment_address else None,
                "country": s.shipment_address.country if s.shipment_address else None,
                "state": s.shipment_address.state if s.shipment_address else None,
                "provider": s.shipment_provider,
                "tracking": s.tracking_reference,
                "amount": s.shipment_amount.amount if s.shipment_amount else None,
                "entity_type": "SHIPMENT"
            })

            # Shipment Items (Hierarchical Sort Key)
            for si in s.shipment_items:
                items.append({
                    "pk": f"ORDER#{order.order_id}",
                    "sk": f"SHIPMENT#{s.shipment_id}#ITEM#{si.shipment_item_id}SKU#{si.line_item.product_sku}",
                    "shipment_item_id": si.shipment_item_id,
                    "line_item_sku": si.line_item.product_sku if hasattr(si.line_item, 'product_sku') else None,
                    "quantity": si.quantity,
                    "entity_type": "SHIPMENT_ITEM"
                })
        return items


    @staticmethod
    def to_domain(header_item: Dict[str, Any], related_items: List[Dict[str, Any]]) -> models.Order:
        """
        Reconstruct the Domain Aggregate from DynamoDB items.
        'header_item': The row with entity_type="ORDER"
        'related_items': All rows where pk="ORDER#<id>" (Lines, Shipments, ShipmentItems)
        """
        related_items = related_items or []
        
        # 1. Reconstruct Line Items
        # Map them first so we can reference them in ShipmentItems later
        line_item_map = {}
        for item in related_items:
            if item.get("entity_type") == "LINE_ITEM":
                sku = item["product_sku"]
                line_item_map[sku] = models.LineItem(
                    product_sku=sku,
                    product_name=item["product_name"],
                    product_price=value_objects.Money(
                        amount=Decimal(str(item["product_price"])), 
                        currency=item["product_currency"]
                    ),
                    order_quantity=int(item["order_quantity"]),
                    vendor_id=item["vendor_id"],
                    package=value_objects.Package(
                        weight_kg=Decimal(str(item["package_weight_kg"]))
                    ) if item.get("package_weight_kg") is not None else None
                )

        # 2. Group Shipment Items by Shipment ID
        # Based on your SK: SHIPMENT#{shipment_id}#ITEM#{item_id}SKU#{sku}
        shipment_items_by_ship_id: Dict[str, List[models.ShipmentItem]] = {}
        for item in related_items:
            if item.get("entity_type") == "SHIPMENT_ITEM":
                s_id = item["shipment_id"]
                sku = item["line_item_sku"]
                
                si = models.ShipmentItem(
                    shipment_item_id=item["shipment_item_id"],
                    quantity=int(item["quantity"]),
                    # Link to the actual LineItem object from our map
                    line_item=line_item_map[sku] 
                )
                
                if s_id not in shipment_items_by_ship_id:
                    shipment_items_by_ship_id[s_id] = []
                shipment_items_by_ship_id[s_id].append(si)

        # 3. Reconstruct Shipments
        shipments = []
        for item in related_items:
            if item.get("entity_type") == "SHIPMENT":
                s_id = item["sk"].replace("SHIPMENT#", "")

                if not (item.get("line1") and item.get("city") and item.get("country")):  
                    raise Exception("OrderDynamodbMapper: Incomplete address data for shipment reconstruction.")

                
                # Reconstruct Address Value Object
                addr = value_objects.Address(
                    line1=item["line1"],
                    city=item["city"],
                    country=item["country"],
                    line2=item["line2"],
                    postal=item["postal"],
                    state=item["state"],
                )

                shipments.append(models.Shipment(
                    shipment_id=s_id,
                    shipment_address=addr,
                    shipment_provider=item.get("provider"),
                    tracking_reference=item.get("tracking"),
                    shipment_status=enums.ShipmentStatus(item["status"]),
                    shipment_amount=value_objects.Money(
                        amount=Decimal(str(item["amount"])) if item.get("amount") is not None else Decimal("0.00"),
                        currency=item["currency"]
                    ),
                    # Attach the grouped shipment items
                    shipment_items=shipment_items_by_ship_id.get(s_id, [])
                ))

        # 4. Assemble the Order Aggregate
        return models.Order(
            order_id=header_item["order_id"],
            tenant_id=header_item["tenant_id"],
            external_ref=header_item["external_ref"],
            customer_details=value_objects.CustomerDetails(
                customer_id=header_item["customer_id"],
                name=header_item["customer_name"],
                email=header_item["customer_email"]
            ),
            order_status=enums.OrderStatus(header_item["order_status"]),
            payment_status=enums.PaymentStatus(header_item["payment_status"]),
            line_items=list(line_item_map.values()),
            shipments=shipments,
            # Handle ISO date strings back to datetime objects
            date_created=datetime.fromisoformat(header_item["date_created"]),
            date_modified=datetime.fromisoformat(header_item["date_modified"]),
            _version=header_item["version"]
        )
