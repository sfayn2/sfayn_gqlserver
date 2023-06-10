import abc
from dataclasses import dataclass

class ValueObject(abc.ABC):
    pass

@dataclass
class OrderItem(ValueObject):
    pass