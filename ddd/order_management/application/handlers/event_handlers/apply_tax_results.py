from __future__ import annotations
from ddd.order_management.application import (
    ports, 
    shared
)
from ddd.order_management.domain import events, exceptions

def handle_apply_tax_results(
        event: events.DomainEvent, 
        tax_service:  TaxStrategyServiceAbstract,
        uow: UnitOfWorkAbstract):

    try:
        order = uow.order.get(order_id=event.order_id)

        tax_results = tax_service.calculate_all_taxes(order)
        order.apply_tax_results(tax_results)

        uow.order.save(order)

    except exceptions.InvalidOrderOperation as e:
        #TODO logger.info?
        print(e)
        raise e
    except Exception as e:
        # logger.exception?
        print(e)
        raise e

