
import abc
from ..ordering_domain.aggregates_model.order_aggregate.ordering import Ordering
from order.models import Order, OrderItem

class AbstractOrderingRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, order: Ordering):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, entity_id) -> Ordering:
        raise NotImplementedError

    @abc.abstractmethod
    def get_next_id(self) -> int:
        raise NotImplementedError


class OrderingRepository(AbstractOrderingRepository):

    def add(self, order):
        pass
        #Order.objects.create()
        #for line_item in order.get_line_items():
        #    OrderItem.objects.create()

    def get_next_id(self):
        id = Order.objects.latest("id")
        return id + 1

    def get(self, entity_id):
        #still need to conver to domain structure
        return Order.objects.get(id=entity_id)


