import decimal
from typing import List
from ..aggregates_model.order_aggregate.ordering import (
      Ordering,
      LineItem
)
from ..aggregates_model.buyer_aggregate.buyer import (
      Buyer
)


def place_order(
        next_id: int,
        tax_rate: decimal.Decimal,
        buyer_id: int,
        buyer_note: str,
        line_items: List[LineItem]) -> None:

    buyer = Buyer()
    buyer.set_entity_id(buyer_id)
    buyer.set_buyer_note(buyer_note)

    order = Ordering(
        buyer
    )
    order.add_line_items(line_items)
    order.set_entity_id(
        next_id
    )
    order.set_tax_rate(tax_rate)
    order.set_as_waiting_for_payment()
