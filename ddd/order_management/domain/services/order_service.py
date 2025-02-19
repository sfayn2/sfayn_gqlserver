import uuid
from datetime import datetime
from typing import List
from ddd.order_management.domain import models, value_objects, enums, exceptions
from ddd.order_management.domain.services import tax_service, offer_service, payment_service

def confirm_order(payment_service: payment_service.PaymentService, 
                  order: models.Order, payment_details: value_objects.PaymentDetails):

        is_paid, message = payment_service.verify_payment(
            order_id=order.order_id,
            transaction_id=payment_details.transaction_id,
            expected_amount=payment_details.amount,
        )

        order.confirm_order(is_paid)

        return order


def place_order(
        customer_details: value_objects.CustomerDetails,
        shipping_address: value_objects.Address,
        shipping_details: value_objects.ShippingDetails,
        coupons: List[value_objects.Coupon],
        line_items: List[models.LineItem],
        tax_service: tax_service.TaxStrategyService,
        offer_service: offer_service.OfferStrategyService
) -> models.Order:

    order = models.Order(
        order_id=f"ORD-{uuid.uuid4().hex[:8].upper()}",
        order_status=enums.OrderStatus.DRAFT,
        date_created=datetime.now(),
        customer_details=customer_details,
        shipping_details=shipping_details,
        destination=shipping_address
    )

    order.update_line_items(line_items)
    for coupon in coupons:
        order.apply_coupon(coupon)
    offer_service.apply_offers(order)
    tax_service.apply_taxes(order)

    order.calculate_final_amount()
    
    order.place_order()

    return order
