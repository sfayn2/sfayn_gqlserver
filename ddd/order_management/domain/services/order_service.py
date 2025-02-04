from typing import List
from ddd.order_management.domain import models, value_objects
from ddd.order_management.domain.services import tax_service, offer_service

def draft_order(
    customer_details: value_objects.CustomerDetails,
    destination: value_objects.Address,
    line_items: List[models.LineItem]
) -> models.Order:

    order = models.Order.create_draft_order(
        destination=destination,
        customer_details=customer_details,
        line_items=line_items
    )

    return order


def place_order(
        order:  models.Order,
        customer_details: value_objects.CustomerDetails,
        shipping_address: value_objects.Address,
        shipping_details: value_objects.ShippingDetails,
        coupons: List[value_objects.Coupon],
        line_items: List[models.LineItem],
        tax_service: tax_service.TaxStrategyService,
        offer_service: offer_service.OfferStrategyService
) -> models.Order:

    order.update_customer_details(customer_details)
    order.update_destination(shipping_address)
    order.update_shipping_details(shipping_details)
    order.update_line_items(line_items)

    for coupon in coupons:
        order.apply_coupon(coupon)
    offer_service.apply_offers(order)

    tax_service.apply_taxes(order)

    order.calculate_final_amount()
    
    order.place_order()


    return order
