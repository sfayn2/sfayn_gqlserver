
import abc
from typing import TypeVar
from django.contrib.auth.models import User
from ..ordering_domain.aggregates_model.order_aggregate.ordering import (
    Ordering, 
)
from .mapper import ( 
    map_django_to_ordering_domain, 
    add_ordering_from_domain,
    get_next_id
)

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
        add_ordering_from_domain(order)

    def get_next_id(self):
        return get_next_id()

    def get(self, entity_id) -> Ordering:
        return map_django_to_ordering_domain(entity_id)


