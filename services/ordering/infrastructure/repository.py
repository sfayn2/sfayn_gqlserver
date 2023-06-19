
import abc
from typing import TypeVar
from django.contrib.auth.models import User
from ..ordering_domain.aggregates_model.order_aggregate.ordering import Ordering
from ..ordering_domain.aggregates_model.buyer_aggregate.buyer import Buyer
from order.models import Order, OrderItem

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
        pass
        #Order.objects.create()
        #for line_item in order.get_line_items():
        #    OrderItem.objects.create()

    def get_next_id(self):
        id = Order.objects.latest("id")
        return id + 1

    def get(self, entity_id) -> Ordering:
        #still need to conver to domain structure
        return Order.objects.get(id=entity_id)


