from __future__ import annotations
from ddd.order_management.application import (
    ports, 
)
from ddd.order_management.domain import events

def handle_apply_applicable_offers(
        event: events.DomainEvent, 
        offer_service:  OfferStrategyServiceAbstract,
        uow: UnitOfWorkAbstract):

    try:
        with uow:

            order = uow.order.get(order_id=event.order_id)

            offers = offer_service.evaluate_applicable_offers(order)
            order.apply_applicable_offers(offers)

            uow.order.save(order)
            uow.commit()

    except exceptions.InvalidOrderOperation as e:
        #TODO logger.info?
        print(e)
    except Exception as e:
        # logger.exception?
        print(e)

