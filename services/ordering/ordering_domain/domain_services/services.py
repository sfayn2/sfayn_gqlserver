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
        tax_amount: decimal.Decimal,
        buyer_id: int,
        buyer_note: str,
        line_items: List[LineItem],
        currency: str) -> None:

    buyer = Buyer(
            buyer_id, 
            buyer_note
        )

    order = Ordering(
                next_id, 
                buyer, 
                tax_amount, 
                line_items,
                currency
                )

    return order
