from datetime import datetime
from typing import List, TYPE_CHECKING

from ddd.order_management.domain.services.order import ports

from ddd.order_management.domain import (
    models,
    value_objects, 
    exceptions,
    enums
    )

class OrderService(ports.OrderServiceAbstract):
    #Order life cycle

    def create_draft_order(
            self,
            customer_details: value_objects.CustomerDetails,
            shipping_address: value_objects.Address,
            line_items: List[models.LineItem],
            tenant_id: str
    ) -> models.Order:
        order = models.Order(
            date_created=datetime.now(),
            customer_details=customer_details,
            destination=shipping_address
        )

        order.generate_order_id()
        order.tenant_id = tenant_id
        order.mark_as_draft()
        for line_item in line_items:
            order.add_line_item(line_item)

        #order.update_line_items(line_items)
        
        return order

