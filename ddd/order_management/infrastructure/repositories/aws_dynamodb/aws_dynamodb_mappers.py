from typing import Dict, Any
from decimal import Decimal
from ddd.order_management.domain import models, value_objects, enums

class OrderDynamoMapper:
    @staticmethod
    def to_dynamo(order: models.Order) -> Dict[str, Any]:
        """Convert Domain Aggregate to DynamoDB Item."""
        # DynamoDB requires Decimal for numbers, and we flatten/nest as needed
        return {
            "PK": f"TENANT#{order.tenant_id}",
            "SK": f"ORDER#{order.order_id}",
            "order_id": order.order_id,
            "tenant_id": order.tenant_id,
            "external_ref": order.external_ref,
            "customer": {
                "id": order.customer_details.customer_id,
                "name": order.customer_details.name,
                "email": order.customer_details.email
            },
            "order_status": order.order_status.value,
            "payment_status": order.payment_status.value,
            "currency": order.currency,
            "line_items": [
                {
                    "sku": li.product_sku,
                    "name": li.product_name,
                    "price": Decimal(str(li.product_price.amount)),
                    "currency": li.product_price.currency,
                    "qty": li.order_quantity,
                    "weight": Decimal(str(li.package.weight_kg)) if li.package else None
                } for li in order.line_items
            ],
            "shipments": [
                {
                    "id": s.shipment_id,
                    "address": {
                        "line1": s.shipment_address.line1,
                        "city": s.shipment_address.city
                    },
                    "items": [
                        {"shipment_item_id": si.shipment_item_id, "qty": si.quantity}
                        for si in s.shipment_items
                    ]
                } for s in order.shipments
            ],
            "date_created": order.date_created.isoformat(),
            "date_modified": order.date_modified.isoformat(),
        }

    @staticmethod
    def to_domain(item: Dict[str, Any]) -> models.Order:
        """Convert DynamoDB Item back to Domain Aggregate."""
        return models.Order(
            order_id=item["order_id"],
            tenant_id=item["tenant_id"],
            external_ref=item["external_ref"],
            customer_details=value_objects.CustomerDetails(
                customer_id=item["customer"]["id"],
                name=item["customer"]["name"],
                email=item["customer"]["email"]
            ),
            order_status=enums.OrderStatus(item["order_status"]),
            payment_status=enums.PaymentStatus(item["payment_status"]),
            line_items=[
                models.LineItem(
                    product_sku=li["sku"],
                    product_name=li["name"],
                    product_price=value_objects.Money(amount=li["price"], currency=li["currency"]),
                    order_quantity=li["qty"],
                    package=value_objects.Package(weight_kg=li["weight"])
                ) for li in item.get("line_items", [])
            ],
            # ... repeat similar mapping for shipments ...
        )
