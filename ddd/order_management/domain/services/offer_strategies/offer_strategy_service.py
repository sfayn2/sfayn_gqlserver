from typing import Dict, Callable, Any
from ddd.order_management.domain import (
    repositories,
    models,
    enums
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

    def __init__(self, vendor_repository: repositories.VendorAbstract, offers: OFFER_STRATEGIES = DEFAULT_OFFER_STRATEGIES):
        self.vendor_repository = vendor_repository
        self.offer_strategies = offers

    def apply_offers(self, order: models.Order):
        available_offers = self._fetch_valid_offers(order.vendor_name)
        offer_details = []
        for strategy in available_offers:
            res = strategy.apply(order)
            if res:
                offer_details.append(res)

        if offer_details:
            order.update_offer_details(offer_details)

    def _fetch_valid_offers(self, vendor_name: str):
        #The assumption is all Offers are auto applied (except those w Coupons)
        vendor_offers = self.vendor_repository.get_offers(vendor_name)
        valid_offers = []

        #sorted by "priority" in descending order
        sorted_vendor_offers = sorted(vendor_offers, key=lambda vo: vo.priority, reverse=True)

        for offer in sorted_vendor_offers:

            offer_strategy_class = self.offer_strategies.get(offer.offer_type)
            valid_offers.append(
                offer_strategy_class(offer)
            )

            if offer.stackable == False:
                #make sure offers already ordered based on highest priority, so checking stackable is enough
                return valid_offers

        return valid_offers
