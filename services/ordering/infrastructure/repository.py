
import abc
from typing import TypeVar
from django.contrib.auth.models import User
from ..ordering_domain.aggregates_model.order_aggregate.ordering import (
    Ordering, 
    LineItem,
    Money
    )
from ..ordering_domain.aggregates_model.buyer_aggregate.buyer import Buyer
from order import models as django_models

T = TypeVar("T")

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, model: T):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, entity_id) -> T:
        raise NotImplementedError

    @abc.abstractmethod
    def get_next_id(self) -> int:
        raise NotImplementedError


class OrderingRepository(AbstractRepository):

    def add(self, order: Ordering):
        order1, is_created = django_models.Order.objects.get_or_create(
                    id=order.get_entity_id(),
                    default={
                        "discounts_fee": order.get_discounts_fee(),
                        "tax_amount": order.get_tax_amount(),
                        "sub_total": order.get_subtotal(),
                        "total": order.get_total(),
                        "currency": order.get_currency(),
                        "status": order.get_order_status(),
                        "buyer_id": order.get_buyer_id(),
                        "buyer_note": order.get_buyer_note(),
                    }
                )

        for line_item in order.get_line_items():
            django_models.OrderItem.objects.get_or_create(
                order_id=order.get_entity_id(),
                order_quantity=line_item.get_item_quantity(),
                product_variant=line_item.get_item_sku(),
                product_price=line_item.get_item_price(),
                discounts_fee=line_item.get_item_discounts_fee(),
                discounted_price=line_item.get_item_discounted_price(),
                total=line_item.get_item_total()

            )

    def get_next_id(self):
        id = django_models.Order.objects.latest("id")
        return id + 1

    def to_domain_buyer(self, from_django_order):
        return Buyer(
            buyer_id=from_django_order.buyer_id,
            buyer_note=from_django_order.buyer_note
        )

    def to_domain_line_item(self, from_django_order, from_django_order_items):
        to_domain_line_item = []
        for item in from_django_order_items:
            price_money = Money(item.price, from_django_order.currency)
            discounts_fee_money = Money(item.price, from_django_order.currency)
            to_domain_line_item.append(
                LineItem(item.sku, item.quantity, price_money, discounts_fee_money)
            )
        return to_domain_line_item

    def to_domain_ordering(self, from_django_order, from_django_order_items):
        to_domain_ordering = Ordering(
            entity_id=from_django_order.id,
            buyer=self.to_domain_buyer(from_django_order),
            line_items=self.to_domain_line_item(
                    from_django_order, 
                    from_django_order_items
                ),
            currency=from_django_order.currency,
            )
        return to_domain_ordering



    def get(self, entity_id) -> Ordering:
        from_django_order = django_models.Order.objects.get(id=entity_id)
        from_django_order_items = django_models.OrderItem.objects.filter(order_id=entity_id)

        return self.to_domain_ordering(
            from_django_order,
            from_django_order_items
        )


