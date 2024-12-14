import uuid
from abc import ABC, abstractmethod
from ddd.product_catalog.domain import models

class ProductRepository(ABC):
    @abstractmethod
    def save(self, product_catalog: models.Product):
        raise NotImplementedError

    @abstractmethod
    def get(self, product_id: uuid.uuid4) -> models.Product:
        raise NotImplementedError