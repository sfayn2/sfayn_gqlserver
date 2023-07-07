
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
    def sync_order(self, model: T):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, entity_id) -> T:
        raise NotImplementedError

    @abc.abstractmethod
    def get_next_id(self) -> int:
        raise NotImplementedError


class OrderingRepository(AbstractRepository):

    def add(self, order: Ordering):
        self._order = order

        django_models.Order.objects.get_or_create(
                    id=self._order.get_entity_id(),
                    default=self._order.as_dict()
                )

        for line_item in self._order.get_line_items():
            django_models.OrderItem.objects.get_or_create(
                order_id=self._order.get_entity_id(),
                **line_item.as_dict()
            )

    def sync_order(self, order: Ordering):
        self._order = order

    def get_next_id(self):
        id = django_models.Order.objects.latest("id")
        return id + 1

    def get(self, entity_id) -> Ordering:
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


