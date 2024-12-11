from abc import ABC
from dataclasses import dataclass
from domain import enums
import uuid

class Command(ABC):
    pass


@dataclass
class CreateProductCommand(Command):
    name: str
    price: float
    category: str

@dataclass
class ChangeStatusCommand(Command):
    product_id: uuid.uuid4
    new_status: enums.ProductStatus