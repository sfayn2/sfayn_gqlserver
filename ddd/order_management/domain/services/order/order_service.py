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

    def confirm_order(self, payment_details: value_objects.PaymentDetails,
                    order: models.Order) -> models.Order:
        
        if payment_details.payment_status == enums.PaymentStatus.PAID:
            order.confirm_order(True)
            order.update_payment_details(payment_details)
        else:
            raise exceptions.PaymentDetailsException(
                f"Unable to confirm Order {order.order_id}, Payment was not successful."
            )

        return order

    def create_draft_order(
            self,
            customer_details: value_objects.CustomerDetails,
            shipping_address: value_objects.Address,
            line_items: List[models.LineItem]
    ) -> models.Order:
        order = models.Order(
            date_created=datetime.now(),
            customer_details=customer_details,
            destination=shipping_address
        )

        order.generate_order_id()
        order.mark_as_draft()
        order.update_line_items(line_items)
        
        return order

    #def place_order(self, order: models.Order) -> models.Order:

    #    order.place_order()

    #    return order


