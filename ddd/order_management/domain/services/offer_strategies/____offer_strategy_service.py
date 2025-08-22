from typing import Dict, Callable, Any, List
from ddd.order_management.domain import (
    repositories,
    models,
    enums,
    value_objects
    )

from ddd.order_management.domain.services.offer_strategies import (
    percentage_discount,
    percentage_discount_by_coupon,
    free_gifts,
    free_shipping,
    ports
)

# ==============
# Offer Strategy Mapper
# ===============

# when adding new offer need to map the strategy
DEFAULT_OFFER_STRATEGIES = {
    enums.OfferType.PERCENTAGE_DISCOUNT: percentage_discount.PercentageDiscountStrategy,
    enums.OfferType.FREE_GIFT: free_gifts.FreeGiftOfferStrategy,
    enums.OfferType.COUPON_PERCENTAGE_DISCOUNT: percentage_discount_by_coupon.PercentageDiscountCouponOfferStrategy,
    enums.OfferType.FREE_SHIPPING: free_shipping.FreeShippingOfferStrategy
}
OFFER_STRATEGIES = Dict[enums.OfferType, ports.OfferStrategyAbstract]

# ================
# Offer Strategy Service
# ==================

class OfferStrategyService(ports.OfferStrategyServiceAbstract):        

    def __init__(self, offers: OFFER_STRATEGIES = DEFAULT_OFFER_STRATEGIES):
        #self.vendor_repository = vendor_repository
        self.offer_strategies = offers

    def evaluate_applicable_offers(
                self, 
                order: models.Order, 
                vendor_offers: List[value_objects.OfferStrategy]
            ) -> List[ports.OfferStrategyAbstract]:

        #The assumption is all Offers are auto applied (except those w Coupons)
        #vendor_offers = self.vendor_repository.get_offers(order.vendor_id)
        valid_offers = []

        #sorted by "priority" in descending order
        sorted_vendor_offers = sorted(vendor_offers, key=lambda vo: vo.priority, reverse=True)

        for offer in sorted_vendor_offers:

            offer_strategy_class = self.offer_strategies.get(offer.offer_type)
            valid_offers.append(
                offer_strategy_class(offer, order)
            )

            if offer.stackable == False:
                #make sure offers already ordered based on highest priority, so checking stackable is enough
                break
                #return valid_offers

        final_offers = []
        for strategy in valid_offers:
            final_offers.append(strategy)


        return final_offers
