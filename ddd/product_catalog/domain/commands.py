import uuid
from abc import ABC
from dataclasses import dataclass
from ddd.product_catalog.domain import enums

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

@dataclass
class ActivateProductCommand(Command):
    product_id: uuid.uuid4