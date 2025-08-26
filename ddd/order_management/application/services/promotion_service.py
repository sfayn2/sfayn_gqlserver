from __future__ import annotations
from typing import Dict, Callable, Any, List, Type

from ddd.order_management.domain.services.offer_strategies import (
    ports
)


# ================
# Offer Strategy Service
# ==================

class PromotionService:

    def __init__(self, offers: List[ports.OfferStrategyAbstract]):
        self.offers = offers

    def evaluate_applicable_offers(
                self, 
                order: models.Order, 
                vendor_offers: List[dtos.VendorOfferSnapshotDTO]
            ) -> List[ports.OfferStrategyAbstract]:

        #The assumption is all Offers are auto applied (except those w Coupons)
        #vendor_offers = self.vendor_repository.get_offers(order.vendor_id)
        valid_offers = []

        #sorted by "priority" in descending order
        sorted_vendor_offers = sorted(vendor_offers, key=lambda vo: vo.priority, reverse=True)

        for offer in sorted_vendor_offers:

            key = (offer.method, offer.provider.lower())
            strategy_factories = self.offers.get(key, [])
            for factory in strategy_factories:
                strategy_ins = factory(
                    offer.tenant_id, 
                    offer
                )
                valid_offers.append(strategy_ins)


            if offer.stackable == False:
                #make sure offers already ordered based on highest priority, so checking stackable is enough
                break
                #return valid_offers

        final_offers = []
        for offer in valid_offers:
            if offer.is_eligible(order):
                final_offers.append(offer)


        return final_offers
