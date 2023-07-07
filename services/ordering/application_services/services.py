from typing import List
import decimal
from ..ordering_domain import domain_services
from ..infrastructure import unit_of_work


def place_order(
    tax_amount: decimal.Decimal,
    buyer_id: int,
    buyer_note: str,
    uow: unit_of_work.DjangoUnitOfWork, 
    line_items: List,
    currency) -> None:

    with uow:
        next_id = uow.ordering.get_next_id()
        #line_items = OrderMap.to_domain ? OrderingDTO
        order = domain_services.services.place_order(
            next_id,
            tax_amount,
            buyer_id,
            buyer_note,
            line_items,
            currency
        )

        uow.ordering.add(order)
        uow.commit()

    #send event to payment service? -> send delivery 

def fulfill_order(
    order_id: int,
    uow: unit_of_work.DjangoUnitOfWork
) -> None:

    with uow:

        order = uow.ordering.get(order_id)
        order.set_fulfillment_items()

        uow.ordering.sync_order(order)
        uow.commit()

