from abc import ABC, abstractmethod
from typing import List
from ddd.order_management.domain import value_objects, models, exceptions
from ddd.order_management.application import ports

class OrderServiceAbstract(ABC):
    @abstractmethod
    def confirm_order(payment_details: value_objects.PaymentDetails,
                    order: models.Order) -> models.Order:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def draft_order(
            customer_details: value_objects.CustomerDetails,
            shipping_address: value_objects.Address,
            line_items: List[models.LineItem],
    ) -> models.Order:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def get_shipping_options(
            shipping_option_service: ports.ShippingOptionStrategyServiceAbstract, 
            order: models.Order) -> List[value_objects.ShippingDetails]:
        raise NotImplementedError("Subclasses must implement this method")

#def place_order(
#        customer_details: value_objects.CustomerDetails,
#        shipping_address: value_objects.Address,
#        shipping_details: value_objects.ShippingDetails,
#        coupons: List[value_objects.Coupon],
#        line_items: List[models.LineItem],
#        offer_service: offer_service.OfferStrategyService
#) -> models.Order:
#
#    order = models.Order(
#        order_id=f"ORD-{uuid.uuid4().hex[:8].upper()}",
#        order_status=enums.OrderStatus.DRAFT,
#        date_created=datetime.now(),
#        customer_details=customer_details,
#        shipping_details=shipping_details,
#        destination=shipping_address
#    )
#
#    order.update_line_items(line_items)
#    for coupon in coupons:
#        order.apply_coupon(coupon)
#
#    order.apply_offers(offer_service)
#    order.apply_taxes(tax_service.TAX_STRATEGIES)
#
#    order.calculate_final_amount()
#    
#    order.place_order()
#
#    return order