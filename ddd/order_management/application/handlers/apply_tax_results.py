from __future__ import annotations
from ddd.order_management.application import (
    ports, 
)
from ddd.order_management.domain import events

def handle_apply_tax_results(
        event: events.DomainEvent, 
        tax_service:  TaxStrategyServiceAbstract,
        uow: UnitOfWorkAbstract):

    try:
        with uow:

            order = uow.order.get(order_id=event.order_id)

            tax_results = tax_service.calculate_all_taxes(order)
            order.apply_tax_results(tax_results)

            uow.order.save(order)
            uow.commit()

    except exceptions.InvalidOrderOperation as e:
        #TODO logger.info?
        print(e)
    except Exception as e:
        # logger.exception?
        print(e)

