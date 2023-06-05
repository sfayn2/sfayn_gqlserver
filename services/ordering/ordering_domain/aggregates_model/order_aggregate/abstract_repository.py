
import abc
from order_aggregate import order

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, order: order.Ordering):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, order_id) -> order.Ordering:
        raise NotImplementedError



class OrderingRepository(AbstractRepository):
    pass
