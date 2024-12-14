from abc import ABC
from dataclasses import dataclass

class DomainEvent(ABC):
    pass

@dataclass
class ProductCreated(DomainEvent):
    product_id: str
    name: str
    price: float
    category: str