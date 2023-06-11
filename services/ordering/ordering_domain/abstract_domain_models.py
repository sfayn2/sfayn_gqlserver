import abc
from dataclasses import dataclass

class Entity(abc.ABC):

    def __init__(self, *args, entity_id: None, **kwargs):
        self.entity_id = entity_id
        super().__init__(*args, **kwargs)

    def __eq__(self, other):
        if self.__class__ == type(other):
            return self.entity_id == other.entity_id
        return False

    def __hash__(self):
        return hash(self.entity_id)


@dataclass(frozen=True)
class ValueObject(abc.ABC):
    pass


class AggregateRoot(Entity):
    pass