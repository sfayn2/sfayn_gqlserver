from __future__ import annotations
from ddd.order_management.application import (
    ports, 
)
from ddd.order_management.domain import events, exceptions

def handle_apply_applicable_offers(
        event: events.DomainEvent, 
        offer_service:  OfferStrategyServiceAbstract,
        vendor: VendorAbstract,
        uow: UnitOfWorkAbstract):

    try:

        order = uow.order.get(order_id=event.order_id)

        vendor_offers = vendor.get_offers(
            order.tenant_id,
            order.vendor_id
        )
        applicable_offers = offer_service.evaluate_applicable_offers(order, vendor_offers)

        order.apply_applicable_offers(applicable_offers)

        uow.order.save(order)


    except exceptions.InvalidOrderOperation as e:
        #TODO logger.info?
        print(e)
        raise e
    except Exception as e:
        # logger.exception?
        print(e)
        raise e

