from datetime import datetime
from typing import List
from ddd.order_management.application import ports
from ddd.order_management.domain import (
    domain_service,
    models,
    value_objects, 
    exceptions,
    enums
    )

class OrderService(domain_service.OrderServiceAbstract):

    def confirm_order(payment_details: value_objects.PaymentDetails,
                    order: models.Order) -> models.Order:
        if payment_details.order_id != order.order_id:
            raise exceptions.InvalidPaymentOperation("Payment Verification Order ID mismatch")

        if payment_details.paid_amount != order.final_amount:
            raise exceptions.InvalidPaymentOperation(f"Transaction Amount mismatch: expected {order.final_amount.amount} {order.final_amount.currency}")

        if payment_details.status != "COMPLETED":
            raise exceptions.InvalidPaymentOperation("Transaction not completed")
        
        order.confirm_order(True)
        order.update_payment_details(payment_details)

        return order

    def draft_order(
            customer_details: value_objects.CustomerDetails,
            shipping_address: value_objects.Address,
            line_items: List[models.LineItem],
            tax_service: ports.TaxStrategyAbstract
    ) -> models.Order:
        order = models.Order(
            order_status=enums.OrderStatus.DRAFT,
            date_created=datetime.now(),
            customer_details=customer_details,
            destination=shipping_address
        )

        order.generate_order_id()
        order.update_line_items(line_items)
        
        order.apply_taxes(tax_service.TAX_STRATEGIES)

        order.calculate_final_amount()
        
        return order


    def get_shipping_options(
            shipping_option_service: ports.ShippingOptionStrategyServiceAbstract, 
            order: models.Order) -> List[value_objects.ShippingDetails]:

        shipping_options = shipping_option_service.get_shipping_options(order=order)

        if not shipping_options:
            raise exceptions.InvalidShippingOption(f"No available shipping options.")

        return shipping_options
