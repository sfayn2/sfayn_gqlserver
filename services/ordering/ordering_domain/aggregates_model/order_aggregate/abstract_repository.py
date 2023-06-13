
import abc
from .order_aggregate.order import Order

class AbstractOrderRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, order: Order):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, order_id) -> Order:
        raise NotImplementedError

    @abc.abstractmethod
    def next_id(self):
        raise NotImplementedError



