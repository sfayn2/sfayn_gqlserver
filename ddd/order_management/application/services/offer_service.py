from __future__ import annotations
from typing import Dict, Callable, Any, List, Type

from ddd.order_management.domain.services.offer_strategies import (
    ports
)


# ================
# Offer Strategy Service
# ==================

class OfferService:

    def __init__(self, offers: List[ports.OfferStrategyAbstract]):
        self.offers = offers

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
            for strategy_cls in self.offers:
                valid_offers.append(
                    strategy_cls(offer, order)
                )

            if offer.stackable == False:
                #make sure offers already ordered based on highest priority, so checking stackable is enough
                break
                #return valid_offers

        final_offers = []
        for strategy in valid_offers:
            final_offers.append(strategy)


        return final_offers
