from order import models as django_models
from ..ordering_domain.aggregates_model.order_aggregate.ordering import (
    Ordering, 
    LineItem,
    Money
    )
from ..ordering_domain.aggregates_model.buyer_aggregate.buyer import Buyer


def map_django_to_ordering_domain(entity_id):
    from_django_order = django_models.Order.objects.get(id=entity_id)
    from_django_order_items = django_models.OrderItem.objects.filter(order_id=entity_id)

    _buyer = Buyer(
        buyer_id=from_django_order.buyer_id,
        buyer_note=from_django_order.buyer_note
    )

    ordering = Ordering(
        entity_id=from_django_order.id,
        buyer=_buyer,
        currency=from_django_order.currency,
        )

    for item in from_django_order_items:
        price_money = Money(item.price, from_django_order.currency)
        discounts_fee_money = Money(item.price, from_django_order.currency)

        ordering.add_line_item(
            LineItem(item.sku, item.quantity, price_money, discounts_fee_money)
        )

    return ordering


def add_ordering_from_domain(order: Ordering):
    django_models.Order.objects.get_or_create(
                id=order.get_entity_id(),
                default={
                    "discounts_fee": order.get_discounts_fee(),
                    "tax_amount": order.get_tax_amount(),
                    "sub_total": order.get_subtotal(),
                    "total": order.get_total(),
                    "currency": order.get_currency(),
                    "status": order.get_order_status(),
                    "buyer_id": order._buyer.get_buyer_id(),
                    "buyer_note": order._buyer.get_buyer_note(),
                }
            )

    for line_item in order.get_line_items():
        django_models.OrderItem.objects.get_or_create(
            order_id=order.get_entity_id(),
            **line_item.as_dict()
        )

    
def get_next_id():
    id = django_models.Order.objects.latest("id")
    return id + 1

