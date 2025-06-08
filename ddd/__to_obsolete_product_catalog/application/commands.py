import uuid
from abc import ABC
from dataclasses import dataclass
from typing import Union
from datetime import datetime
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
class ApproveProductCommand(Command):
    product_id: uuid.uuid4

@dataclass
class CreateCategoryCommand(Command):
    id: uuid.uuid4
    name: str
    level: str
    parent_id: Union[uuid.uuid4, None] 
    vendor_name: str
    date_created: datetime
