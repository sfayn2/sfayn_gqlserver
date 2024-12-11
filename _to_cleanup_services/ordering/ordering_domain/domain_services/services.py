import decimal
from typing import List
from ..aggregates_model.order_aggregate.ordering import (
      Ordering,
      LineItem,
)
from ..aggregates_model.buyer_aggregate.buyer import (
      Buyer
)

def fulfill_order(
        order: Ordering
):
    order.set_fulfillment_items()
    return order
    


def place_order(
        next_id: int,
        tax_amount: decimal.Decimal,
        buyer_id: int,
        buyer_note: str,

        line_items: List[LineItem],
        currency: str,
        payment_status: bool) -> None:

      buyer = Buyer(
            buyer_id, 
            buyer_note
        )

      order = Ordering(
                next_id, 
                buyer, 
                tax_amount, 
                line_items,
                currency,
                payment_status
            )


      return order
