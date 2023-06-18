from typing import List
import decimal
from ..ordering_domain.aggregates_model.order_aggregate import (
    ordering,
    money
)
from ..ordering_domain.aggregates_model.buyer_aggregate import (
    buyer,
)
from ..infrastructure import unit_of_work


def place_order(
    tax_rate: decimal.Decimal,
    buyer_id: int,
    buyer_note: str,
    uow: unit_of_work.DjangoUnitOfWork, 
    line_items: List[ordering.LineItem]) -> None:

    with uow:
        buyer = buyer.Buyer()
        buyer.set_entity_id(buyer_id)
        buyer.set_buyer_note(buyer_note)

        order = ordering.Ordering(
            buyer
        )
        order.add_line_items(line_items)
        order.set_entity_id(
            uow.ordering.get_next_id()
        )
        order.set_tax_rate(tax_rate)
        order.set_as_waiting_for_payment()

        uow.ordering.add(order)
        uow.commit()

    #send event to payment service? -> send delivery 
