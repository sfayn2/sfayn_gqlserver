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
        if payment_details.order_id != order.order_id:
            raise exceptions.InvalidOrderOperation("Payment Verification Order ID mismatch")

        if payment_details.paid_amount != order.final_amount:
            raise exceptions.InvalidOrderOperation(f"Transaction Amount mismatch: expected {order.final_amount.amount} {order.final_amount.currency}")

        if payment_details.status != "COMPLETED":
            raise exceptions.InvalidOrderOperation("Transaction not completed")
        
        order.confirm_order(True)
        order.update_payment_details(payment_details)

        return order

    def create_draft_order(
            self,
            customer_details: value_objects.CustomerDetails,
            shipping_address: value_objects.Address,
            line_items: List[models.LineItem]
    ) -> models.Order:
        order = models.Order(
            order_status=enums.OrderStatus.DRAFT,
            date_created=datetime.now(),
            customer_details=customer_details,
            destination=shipping_address
        )

        order.generate_order_id()
        order.update_line_items(line_items)

        order.calculate_final_amount()
        
        return order

    #def place_order(self, order: models.Order) -> models.Order:

    #    order.place_order()

    #    return order


