import uuid
from abc import ABC, abstractmethod
from domain import models

class ProductCatalogRepository(ABC):
    @abstractmethod
    def save(self, product_catalog: models.ProductCatalog):
        raise NotImplementedError

    @abstractmethod
    def get(self, product_id: uuid.uuid4) -> models.ProductCatalog:
        raise NotImplementedError